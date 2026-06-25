import { useState, useEffect } from 'react';
import { dashboard } from '../services/api';

function ConfusionHeatmap({ zones }) {
  if (!zones || zones.length === 0) {
    return (
      <div className="text-center py-6 text-gray-500 text-sm">
        <div className="text-3xl mb-2">✨</div>
        Tidak ada zona kebingungan terdeteksi. Bagus!
      </div>
    );
  }
  const maxCount = Math.max(...zones.map(z => z.count || 1));
  return (
    <div className="space-y-3">
      {zones.map((zone, i) => {
        const intensity = (zone.count || 1) / maxCount;
        const heat = intensity > 0.7 ? 'bg-red-500' : intensity > 0.4 ? 'bg-orange-500' : 'bg-yellow-500';
        return (
          <div key={i}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-300">{zone.name || zone}</span>
              <span className="text-gray-500 text-xs">{zone.count ? `${zone.count} kebingungan` : 'Terdeteksi'}</span>
            </div>
            <div className="w-full bg-white/5 rounded-full h-2.5">
              <div
                className={`${heat} h-2.5 rounded-full progress-bar opacity-80`}
                style={{ width: `${Math.max(10, intensity * 100)}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}

const LEARNING_STYLE_TIPS = {
  visual: [
    'Gunakan diagram, peta konsep, dan infografis saat belajar',
    'Tandai poin penting dengan warna berbeda',
    'Buat flowchart untuk memahami proses kompleks',
  ],
  auditory: [
    'Ucapkan ulang materi dengan keras setelah membaca',
    'Diskusikan materi dengan teman sebaya',
    'Gunakan mnemonik dan irama untuk mengingat',
  ],
  kinesthetic: [
    'Praktikkan dengan latihan soal langsung',
    'Belajar dalam sesi pendek dengan istirahat aktif',
    'Buat catatan dengan tulisan tangan sendiri',
  ],
  reading_writing: [
    'Buat ringkasan tertulis dari setiap topik',
    'Tulis ulang catatan dalam kata-katamu sendiri',
    'Buat daftar poin utama sebelum mengerjakan latihan',
  ],
  visual_kinesthetic: [
    'Kombinasikan diagram dengan latihan langsung',
    'Gambar sketsa konsep lalu langsung terapkan',
    'Gunakan simulasi dan model visual interaktif',
  ],
};

export default function MetacognitiveDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboard.student()
      .then((res) => setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Memuat analisis metakognitif...</p>
      </div>
    </div>
  );

  const mastery = data?.mastery || {};
  const profile = data?.profile || {};
  const masteryScores = mastery.mastery_scores || {};
  const confusionZones = mastery.confusion_zones || [];
  const learningStyleCode = profile.learning_style?.code || 'visual';
  const totalTraces = mastery.total_traces || 0;
  const completedMissions = mastery.total_missions_completed || 0;

  const tips = LEARNING_STYLE_TIPS[learningStyleCode] || LEARNING_STYLE_TIPS.visual;
  const masteryEntries = Object.entries(masteryScores);
  const strongTopics = masteryEntries.filter(([, s]) => s >= 70);
  const weakTopics = masteryEntries.filter(([, s]) => s < 70);

  const avgMastery = masteryEntries.length > 0
    ? Math.round(masteryEntries.reduce((a, [, s]) => a + s, 0) / masteryEntries.length)
    : 0;

  return (
    <div className="max-w-4xl mx-auto pb-20 space-y-6 slide-up">
      {/* Header */}
      <div className="text-center pt-4 mb-8">
        <div className="text-5xl mb-3 float-animation">🪞</div>
        <h1 className="text-3xl font-black gradient-text mb-2">Metacognitive Dashboard</h1>
        <p className="text-gray-400 text-sm max-w-lg mx-auto">
          Pahami cara belajarmu sendiri. Data ini membantu AI merancang jalur yang lebih baik untukmu.
        </p>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Rata-rata Penguasaan', value: `${avgMastery}%`, icon: '🎯', color: 'from-cyan-500/15 to-cyan-600/5 border-cyan-500/20 text-cyan-300' },
          { label: 'Misi Diselesaikan', value: completedMissions, icon: '✅', color: 'from-green-500/15 to-green-600/5 border-green-500/20 text-green-300' },
          { label: 'Total Interaksi', value: totalTraces, icon: '🖱️', color: 'from-purple-500/15 to-purple-600/5 border-purple-500/20 text-purple-300' },
          { label: 'Topik Dikuasai', value: strongTopics.length, icon: '⭐', color: 'from-yellow-500/15 to-yellow-600/5 border-yellow-500/20 text-yellow-300' },
        ].map((m) => (
          <div key={m.label} className={`p-4 rounded-2xl bg-gradient-to-br border card-hover ${m.color}`}>
            <div className="text-2xl mb-2">{m.icon}</div>
            <div className="text-2xl font-black mb-1">{m.value}</div>
            <div className="text-xs text-gray-500">{m.label}</div>
          </div>
        ))}
      </div>

      {/* Confusion Heatmap + Mastery */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-2xl p-6 border border-white/10">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-8 h-8 rounded-xl bg-orange-500/20 flex items-center justify-center">🌡️</div>
            <div>
              <h3 className="font-bold text-white">Peta Panas Kebingungan</h3>
              <p className="text-xs text-gray-500">Area yang sering membuatmu berhenti</p>
            </div>
          </div>
          <ConfusionHeatmap zones={confusionZones} />
        </div>

        <div className="glass rounded-2xl p-6 border border-white/10">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-8 h-8 rounded-xl bg-indigo-500/20 flex items-center justify-center">📊</div>
            <div>
              <h3 className="font-bold text-white">Skor Penguasaan Topik</h3>
              <p className="text-xs text-gray-500">Progress per area materi</p>
            </div>
          </div>
          {masteryEntries.length === 0 ? (
            <div className="text-center py-6 text-gray-500 text-sm">
              <div className="text-3xl mb-2">📚</div>
              Belum ada data. Selesaikan beberapa misi!
            </div>
          ) : (
            <div className="space-y-4">
              {masteryEntries.map(([topic, score]) => {
                const color = score >= 80 ? '#4ade80' : score >= 50 ? '#facc15' : '#f87171';
                const label = score >= 80 ? 'Dikuasai' : score >= 50 ? 'Berkembang' : 'Perlu Perhatian';
                return (
                  <div key={topic}>
                    <div className="flex justify-between text-sm mb-1.5">
                      <span className="text-gray-300 font-medium">{topic}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full" style={{ backgroundColor: `${color}20`, color }}>
                        {label} · {score}%
                      </span>
                    </div>
                    <div className="w-full bg-white/5 rounded-full h-2">
                      <div
                        className="h-2 rounded-full progress-bar"
                        style={{ width: `${score}%`, background: `linear-gradient(90deg, ${color}88, ${color})` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Gaya Belajar + Tips */}
      <div className="glass rounded-2xl p-6 border border-white/10">
        <div className="flex items-center gap-3 mb-5">
          <div className="w-8 h-8 rounded-xl bg-purple-500/20 flex items-center justify-center">💡</div>
          <div>
            <h3 className="font-bold text-white">Saran Strategi Belajar Personal</h3>
            <p className="text-xs text-gray-500">
              Berdasarkan gaya belajar: <span className="text-purple-300 capitalize">{(profile.learning_style?.name || 'Visual').replace(/_/g, ' ')}</span>
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {tips.map((tip, i) => (
            <div key={i} className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
              <div className="text-xl mb-2">{['🎨', '📣', '🏋️'][i] || '💡'}</div>
              <p className="text-sm text-gray-300">{tip}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Strong vs Weak areas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass rounded-2xl p-6 border border-green-500/20">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">💪</span>
            <h3 className="font-bold text-white">Area Kekuatan</h3>
          </div>
          {strongTopics.length === 0 ? (
            <p className="text-sm text-gray-500">Terus belajar untuk mengembangkan area kekuatanmu!</p>
          ) : (
            <div className="space-y-2">
              {strongTopics.map(([topic, score]) => (
                <div key={topic} className="flex items-center justify-between px-3 py-2 rounded-xl bg-green-500/10 border border-green-500/20">
                  <span className="text-sm text-gray-300">{topic}</span>
                  <span className="text-sm font-bold text-green-400">{score}%</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="glass rounded-2xl p-6 border border-red-500/20">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">🎯</span>
            <h3 className="font-bold text-white">Area untuk Ditingkatkan</h3>
          </div>
          {weakTopics.length === 0 ? (
            <p className="text-sm text-gray-500">Semua topik sudah bagus! Pertahankan ya.</p>
          ) : (
            <div className="space-y-2">
              {weakTopics.map(([topic, score]) => (
                <div key={topic} className="flex items-center justify-between px-3 py-2 rounded-xl bg-red-500/10 border border-red-500/20">
                  <span className="text-sm text-gray-300">{topic}</span>
                  <span className="text-sm font-bold text-red-400">{score}%</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Memory Context */}
      {data?.memory_context && Object.keys(data.memory_context).length > 0 && (
        <div className="glass rounded-2xl p-6 border border-cyan-500/20">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">🧠</span>
            <div>
              <h3 className="font-bold text-white">Konteks Memori AI</h3>
              <p className="text-xs text-gray-500">Apa yang AI ketahui tentang perjalanan belajarmu</p>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {data.memory_context.session_count !== undefined && (
              <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-center">
                <div className="text-xl font-black text-cyan-400">{data.memory_context.session_count}</div>
                <div className="text-xs text-gray-500">Total Sesi</div>
              </div>
            )}
            {data.memory_context.ai_flags?.pause_ask_frequency && (
              <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 text-center">
                <div className="text-sm font-bold text-purple-400 capitalize">{data.memory_context.ai_flags.pause_ask_frequency}</div>
                <div className="text-xs text-gray-500">Frekuensi Tanya AI</div>
              </div>
            )}
            {data.memory_context.gamification?.streak_days !== undefined && (
              <div className="p-3 rounded-xl bg-orange-500/10 border border-orange-500/20 text-center">
                <div className="text-xl font-black text-orange-400">{data.memory_context.gamification.streak_days}</div>
                <div className="text-xs text-gray-500">Streak Hari</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
