import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { scanner } from '../services/api';

const STEP_ICONS = ['🔍', '🎨', '⏱️'];

const STEP_VALIDATORS = {
  multiple_select: (answers) => answers.interests.length >= 2,
  single_select: (answers) => !!answers.learning_style,
  duration: () => true,
};

export default function Scanner() {
  const [questions, setQuestions] = useState([]);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({ interests: [], learning_style: null, goals: '', session_duration: 30 });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const navigate = useNavigate();
  const navigateTimer = useRef(null);

  useEffect(() => {
    scanner.getQuestions()
      .then((res) => setQuestions(res.data.questions))
      .catch(() => {})
      .finally(() => setLoading(false));
    return () => {
      if (navigateTimer.current) clearTimeout(navigateTimer.current);
    };
  }, []);

  const toggleInterest = (id) => {
    setAnswers((a) => ({
      ...a,
      interests: a.interests.includes(id) ? a.interests.filter((i) => i !== id) : [...a.interests, id],
    }));
  };

  const handleSubmit = async () => {
    if (answers.interests.length < 2 || !answers.learning_style) return;
    setSubmitting(true);
    try {
      await scanner.submit({
        interest_ids: answers.interests,
        learning_style_id: answers.learning_style,
        goals: answers.goals,
        session_duration: answers.session_duration,
      });
      setSubmitted(true);
      navigateTimer.current = setTimeout(() => navigate('/knowledge-map'), 2000);
    } catch {
      setSubmitting(false);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Menyiapkan kuis minat...</p>
      </div>
    </div>
  );

  if (submitted) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center slide-up">
        <div className="text-7xl mb-6 float-animation">🎉</div>
        <h2 className="text-3xl font-black gradient-text mb-3">Profil Tersimpan!</h2>
        <p className="text-gray-400 mb-2">AI sedang menyusun jalur belajar personalmu...</p>
        <div className="flex items-center justify-center gap-2 text-indigo-400">
          <div className="w-4 h-4 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm">Membuka Knowledge Map</span>
        </div>
      </div>
    </div>
  );

  const q = questions[step];
  const progress = ((step + 1) / questions.length) * 100;
  const canNext = q ? (STEP_VALIDATORS[q.type] || (() => true))(answers) : true;

  return (
    <div className="max-w-2xl mx-auto py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="text-4xl mb-3">{STEP_ICONS[step] || '📋'}</div>
        <h1 className="text-2xl font-black gradient-text mb-1">Pemindaian Minat Belajar</h1>
        <p className="text-sm text-gray-500">Bantu AI memahami dirimu agar belajar lebih personal</p>
      </div>

      {/* Progress */}
      <div className="mb-8">
        <div className="flex justify-between text-xs text-gray-500 mb-2">
          <span>Langkah {step + 1} dari {questions.length}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-white/5 rounded-full h-2">
          <div
            className="xp-bar h-2 rounded-full progress-bar"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Step dots */}
        <div className="flex justify-center gap-2 mt-4">
          {questions.map((_, i) => (
            <button
              key={i}
              onClick={() => i < step && setStep(i)}
              className={`transition-all duration-300 rounded-full ${
                i === step ? 'w-8 h-2.5 bg-indigo-400' :
                i < step ? 'w-2.5 h-2.5 bg-indigo-500/60 cursor-pointer hover:bg-indigo-400' :
                'w-2.5 h-2.5 bg-white/10'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Question Card */}
      {q && (
        <div className="glass-strong rounded-2xl p-8 border border-white/10 slide-up">
          <h2 className="text-xl font-bold text-white mb-2">{q.question}</h2>
          {q.description && (
            <p className="text-sm text-gray-400 mb-6">{q.description}</p>
          )}
          {!q.description && <div className="mb-6" />}

          {q.type === 'multiple_select' && (
            <>
              <p className="text-xs text-gray-500 mb-4">Pilih minimal 2 topik yang kamu sukai</p>
              <div className="grid grid-cols-2 gap-3">
                {q.options.map((opt) => {
                  const selected = answers.interests.includes(opt.id);
                  return (
                    <button
                      key={opt.id}
                      onClick={() => toggleInterest(opt.id)}
                      className={`p-4 rounded-xl border text-left transition-all duration-200 card-hover ${
                        selected
                          ? 'bg-indigo-500/20 border-indigo-400/50 shadow-lg shadow-indigo-500/20'
                          : 'glass border-white/10 hover:border-white/20'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 mt-0.5 transition-all ${selected ? 'border-indigo-400 bg-indigo-400' : 'border-white/30'}`}>
                          {selected && <span className="text-xs">✓</span>}
                        </div>
                        <div>
                          <span className="block text-sm font-semibold text-white">{opt.label}</span>
                          {opt.description && <span className="block text-xs text-gray-400 mt-0.5">{opt.description}</span>}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
              {answers.interests.length > 0 && (
                <p className="text-xs text-indigo-400 mt-3">
                  ✓ {answers.interests.length} topik dipilih{answers.interests.length < 2 ? ' (minimal 2)' : ''}
                </p>
              )}
            </>
          )}

          {q.type === 'single_select' && (
            <div className="space-y-3">
              {q.options.map((opt) => {
                const selected = answers[q.id] === opt.id || answers.learning_style === opt.id;
                return (
                  <button
                    key={opt.id}
                    onClick={() => setAnswers({ ...answers, [q.id]: opt.id, learning_style: opt.id })}
                    className={`w-full p-4 rounded-xl border text-left transition-all duration-200 ${
                      selected
                        ? 'bg-indigo-500/20 border-indigo-400/50 shadow-lg shadow-indigo-500/20'
                        : 'glass border-white/10 hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all ${selected ? 'border-indigo-400 bg-indigo-400' : 'border-white/30'}`}>
                        {selected && <span className="text-xs">✓</span>}
                      </div>
                      <div>
                        <span className="block text-sm font-semibold text-white">{opt.label}</span>
                        {opt.description && <span className="block text-xs text-gray-400 mt-0.5">{opt.description}</span>}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}

          {q.type === 'duration' && (
            <div className="space-y-4">
              <div className="text-center">
                <div className="text-5xl font-black gradient-text mb-2">{answers.session_duration}</div>
                <div className="text-gray-400 text-sm">menit per sesi</div>
              </div>
              <input
                type="range"
                min={15}
                max={90}
                step={5}
                value={answers.session_duration}
                onChange={(e) => setAnswers({ ...answers, session_duration: parseInt(e.target.value) })}
                className="w-full accent-indigo-500"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>15 menit</span>
                <span>90 menit</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setStep(Math.max(0, step - 1))}
          disabled={step === 0}
          className="px-5 py-2.5 rounded-xl glass border border-white/10 text-gray-400 hover:text-white transition disabled:opacity-30"
        >
          ← Sebelumnya
        </button>

        {step < questions.length - 1 ? (
          <button
            onClick={() => canNext && setStep(step + 1)}
            disabled={!canNext}
            className="btn-primary px-6 py-2.5 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Selanjutnya →
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={submitting || answers.interests.length < 2 || !answers.learning_style}
            className="btn-primary px-6 py-2.5 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {submitting ? (
              <span className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Menyimpan...
              </span>
            ) : (
              '🚀 Mulai Belajar!'
            )}
          </button>
        )}
      </div>
    </div>
  );
}
