import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { missions, ai } from '../services/api';

export default function Quiz() {
  const { missionId } = useParams();
  const navigate = useNavigate();
  const [mission, setMission] = useState(null);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [pauseAsk, setPauseAsk] = useState({ open: false, question: '', answer: '', loading: false });
  const [traces, setTraces] = useState([]);
  const questionStartTime = useRef(Date.now());
  const pauseCount = useRef(0);

  useEffect(() => {
    missions.start(missionId)
      .then((res) => setMission(res.data.mission))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [missionId]);

  // Reset timer when question changes
  useEffect(() => {
    questionStartTime.current = Date.now();
  }, [currentQ]);

  const recordTrace = (questionId, actionType, extra = {}) => {
    const duration_ms = Date.now() - questionStartTime.current;
    setTraces((t) => [...t, {
      question_id: questionId,
      action_type: actionType,
      duration_ms,
      payload: extra,
    }]);
  };

  const handleAnswer = (questionId, value) => {
    const prev = answers[questionId];
    if (prev !== value) {
      recordTrace(questionId, prev ? 'revise' : 'click', { selected: value });
    }
    setAnswers({ ...answers, [questionId]: value });
  };

  const handleSubmit = async () => {
    const q = questions[currentQ];
    if (q) recordTrace(q.id, 'submit');
    setSubmitting(true);
    try {
      const res = await missions.submit(missionId, { answers, traces });
      setResult(res.data);
    } catch {
      setSubmitting(false);
    }
  };

  const handlePauseAsk = async () => {
    if (!pauseAsk.question.trim()) return;
    const q = questions[currentQ];
    if (q) {
      pauseCount.current++;
      recordTrace(q.id, 'pause', { question: pauseAsk.question, count: pauseCount.current });
    }
    setPauseAsk((p) => ({ ...p, loading: true }));
    try {
      const res = await ai.pauseAsk({
        question: pauseAsk.question,
        mission_id: parseInt(missionId),
        question_context: q?.question_text,
      });
      setPauseAsk((p) => ({ ...p, answer: res.data.answer, loading: false }));
    } catch {
      setPauseAsk((p) => ({ ...p, answer: 'Maaf, gagal memproses pertanyaan. Coba lagi.', loading: false }));
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Memuat misi...</p>
      </div>
    </div>
  );

  if (!mission) return (
    <div className="text-center py-20">
      <div className="text-5xl mb-4">😕</div>
      <p className="text-gray-400">Misi tidak ditemukan.</p>
    </div>
  );

  if (result) {
    const pct = result.score_pct;
    const isGreat = pct >= 80;
    const isOk = pct >= 50;
    return (
      <div className="max-w-2xl mx-auto text-center py-10 slide-up">
        <div className="glass-strong rounded-3xl p-10 border border-white/10">
          <div className="text-7xl mb-6 float-animation">
            {isGreat ? '🎉' : isOk ? '👍' : '💪'}
          </div>
          <h2 className="text-3xl font-black mb-2">Misi Selesai!</h2>
          <p className="text-gray-400 mb-6">Berikut hasil belajarmu</p>

          {/* Score ring */}
          <div className="relative w-32 h-32 mx-auto mb-6">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="3.5" />
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke={isGreat ? '#4ade80' : isOk ? '#facc15' : '#f87171'}
                strokeWidth="3.5"
                strokeDasharray={`${pct}, 100`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-2xl font-black ${isGreat ? 'text-green-400' : isOk ? 'text-yellow-400' : 'text-red-400'}`}>{pct}%</span>
              <span className="text-xs text-gray-500">Skor</span>
            </div>
          </div>

          <div className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-yellow-500/10 border border-yellow-500/30 mb-6">
            <span className="text-2xl">⚡</span>
            <span className="text-2xl font-black text-yellow-400">+{result.xp_earned} XP</span>
          </div>

          {result.gamification?.leveled_up && (
            <div className="mb-4 p-4 rounded-2xl bg-green-500/10 border border-green-500/30 text-green-300 slide-up">
              <div className="text-2xl mb-1">🎊</div>
              <div className="font-bold">Naik Level!</div>
              <div className="text-sm opacity-80">Kamu sekarang Level {result.gamification.level?.number} — {result.gamification.level?.title}</div>
            </div>
          )}

          {result.gamification?.new_badges?.length > 0 && (
            <div className="mb-4 p-4 rounded-2xl bg-purple-500/10 border border-purple-500/30 text-purple-300 slide-up">
              <div className="text-2xl mb-1">🏅</div>
              <div className="font-bold">Lencana Baru!</div>
              <div className="text-sm opacity-80">{result.gamification.new_badges.map((b) => b.name).join(', ')}</div>
            </div>
          )}

          {pct < 80 && (
            <div className="mb-4 p-4 rounded-2xl bg-orange-500/10 border border-orange-500/30 text-orange-300 text-sm">
              💡 Penguasaan belum 80%. AI akan menyarankan misi remedial untukmu.
            </div>
          )}

          <div className="flex gap-3 justify-center mt-6">
            <button onClick={() => navigate('/knowledge-map')} className="px-6 py-3 rounded-xl glass border border-white/10 hover:bg-white/10 transition font-medium">
              🗺️ Kembali ke Peta
            </button>
            <button onClick={() => navigate('/dashboard')} className="btn-primary px-6 py-3">
              📊 Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  const questions = mission.questions || [];
  const q = questions[currentQ];
  if (!q) return <div className="text-center py-20 text-gray-400">Tidak ada soal.</div>;

  const totalAnswered = Object.keys(answers).length;
  const progress = ((currentQ + 1) / questions.length) * 100;

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-white">{mission.title}</h2>
          <div className="flex items-center gap-3 mt-1">
            <span className="text-xs text-gray-400">Soal {currentQ + 1} dari {questions.length}</span>
            <span className="text-xs text-gray-600">|</span>
            <span className="text-xs text-indigo-400">{totalAnswered} dijawab</span>
          </div>
        </div>
        <button
          onClick={() => setPauseAsk((p) => ({ ...p, open: !p.open, answer: '' }))}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium transition-all ${
            pauseAsk.open
              ? 'bg-purple-500/20 border-purple-400/50 text-purple-300'
              : 'glass border-white/10 text-gray-400 hover:text-white hover:border-purple-500/30'
          }`}
        >
          <span>⏸️</span>
          <span className="hidden sm:inline">{pauseAsk.open ? 'Tutup AI' : 'Pause & Ask AI'}</span>
          <span className="sm:hidden">AI</span>
        </button>
      </div>

      {/* Progress */}
      <div className="w-full bg-white/5 rounded-full h-1.5 mb-8">
        <div className="xp-bar h-1.5 rounded-full progress-bar" style={{ width: `${progress}%` }} />
      </div>

      {/* Pause & Ask AI Panel */}
      {pauseAsk.open && (
        <div className="mb-6 p-6 rounded-2xl bg-purple-900/20 border border-purple-500/30 slide-up">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">🤖</div>
            <div>
              <h3 className="font-semibold text-purple-300">MetaLearn AI</h3>
              <p className="text-xs text-gray-500">Tanya apa saja tentang materi ini</p>
            </div>
          </div>

          {pauseAsk.answer && (
            <div className="mb-4 p-4 rounded-xl bg-white/5 border border-white/5 text-sm text-gray-200 leading-relaxed">
              {pauseAsk.answer}
            </div>
          )}

          <textarea
            value={pauseAsk.question}
            onChange={(e) => setPauseAsk((p) => ({ ...p, question: e.target.value }))}
            onKeyDown={(e) => { if (e.key === 'Enter' && e.ctrlKey) handlePauseAsk(); }}
            placeholder={`Tanya tentang "${q.question_text?.slice(0, 40)}..."  (Ctrl+Enter untuk kirim)`}
            className="w-full px-4 py-3 rounded-xl glass border border-white/10 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-purple-500/50 resize-none mb-3"
            rows={3}
          />
          <div className="flex justify-between items-center">
            <span className="text-xs text-gray-600">Progres belajarmu tetap tersimpan</span>
            <button
              onClick={handlePauseAsk}
              disabled={pauseAsk.loading || !pauseAsk.question.trim()}
              className="px-5 py-2 rounded-xl bg-purple-500 hover:bg-purple-600 text-sm font-medium disabled:opacity-40 transition"
            >
              {pauseAsk.loading ? (
                <span className="flex items-center gap-2">
                  <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Memproses...
                </span>
              ) : (
                '💬 Tanya'
              )}
            </button>
          </div>
        </div>
      )}

      {/* Question Card */}
      <div className="glass-strong rounded-2xl p-8 border border-white/10 mb-6 slide-up">
        <div className="flex items-start gap-3 mb-6">
          <div className="w-8 h-8 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-sm font-bold text-indigo-300 flex-shrink-0">
            {currentQ + 1}
          </div>
          <p className="text-base sm:text-lg text-white leading-relaxed">{q.question_text}</p>
        </div>

        {q.type === 'multiple_choice' && q.options?.map((opt) => {
          const selected = answers[q.id] === opt.option_text;
          return (
            <button
              key={opt.id}
              onClick={() => handleAnswer(q.id, opt.option_text)}
              className={`w-full p-4 mb-2 rounded-xl border text-left transition-all duration-200 group ${
                selected
                  ? 'bg-indigo-500/20 border-indigo-400/50 shadow-lg shadow-indigo-500/10'
                  : 'glass border-white/10 hover:border-indigo-500/30 hover:bg-indigo-500/5'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all ${
                  selected ? 'border-indigo-400 bg-indigo-400' : 'border-white/30 group-hover:border-indigo-400/50'
                }`}>
                  {selected && <span className="text-xs text-white">✓</span>}
                </div>
                <span className={`text-sm ${selected ? 'text-white font-medium' : 'text-gray-300'}`}>
                  {opt.option_text}
                </span>
              </div>
            </button>
          );
        })}

        {q.type !== 'multiple_choice' && (
          <textarea
            value={answers[q.id] || ''}
            onChange={(e) => handleAnswer(q.id, e.target.value)}
            placeholder="Tulis jawabanmu di sini..."
            className="w-full px-4 py-4 rounded-xl glass border border-white/10 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 resize-none"
            rows={5}
          />
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={() => setCurrentQ(Math.max(0, currentQ - 1))}
          disabled={currentQ === 0}
          className="px-5 py-2.5 rounded-xl glass border border-white/10 text-gray-400 hover:text-white transition disabled:opacity-30"
        >
          ← Sebelumnya
        </button>

        <div className="flex items-center gap-2">
          {questions.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrentQ(i)}
              className={`w-2.5 h-2.5 rounded-full transition-all ${
                i === currentQ ? 'w-6 bg-indigo-400' :
                answers[questions[i]?.id] ? 'bg-green-500/60' :
                'bg-white/20 hover:bg-white/40'
              }`}
            />
          ))}
        </div>

        {currentQ < questions.length - 1 ? (
          <button
            onClick={() => setCurrentQ(currentQ + 1)}
            className="btn-primary px-6 py-2.5"
          >
            Selanjutnya →
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="px-6 py-2.5 rounded-xl bg-green-500 hover:bg-green-600 text-white font-semibold transition disabled:opacity-50"
          >
            {submitting ? (
              <span className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Mengirim...
              </span>
            ) : (
              '✅ Kumpulkan'
            )}
          </button>
        )}
      </div>
    </div>
  );
}
