import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { learningPaths } from '../services/api';

const DIFFICULTY_CONFIG = {
  beginner:     { label: 'Pemula',   color: 'bg-green-500/20 text-green-300 border-green-500/30',     icon: '🌱' },
  intermediate: { label: 'Menengah', color: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30', icon: '⚡' },
  advanced:     { label: 'Lanjutan', color: 'bg-red-500/20 text-red-300 border-red-500/30',           icon: '🔥' },
};

const TYPE_CONFIG = {
  quiz:        { label: 'Kuis',        icon: '📝' },
  interactive: { label: 'Interaktif', icon: '🎮' },
  essay:       { label: 'Esai',        icon: '✍️' },
};

export default function Missions() {
  const { pathId } = useParams();
  const [path, setPath] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!pathId) {
      setLoading(false);
      return;
    }
    learningPaths.show(pathId)
      .then((res) => setPath(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [pathId]);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Memuat misi...</p>
      </div>
    </div>
  );

  if (!path) return (
    <div className="text-center py-20">
      <div className="text-5xl mb-4">🔍</div>
      <p className="text-gray-400">Jalur belajar tidak ditemukan.</p>
      <Link to="/knowledge-map" className="mt-4 inline-block text-indigo-400 hover:text-indigo-300 transition">
        ← Kembali ke Peta
      </Link>
    </div>
  );

  const diff = DIFFICULTY_CONFIG[path.difficulty_level] || DIFFICULTY_CONFIG.beginner;
  const totalXP = path.missions?.reduce((sum, m) => sum + (m.xp_reward || 0), 0) || 0;
  const totalMinutes = path.missions?.reduce((sum, m) => sum + (m.estimated_minutes || 0), 0) || 0;

  return (
    <div className="max-w-2xl mx-auto pb-20 slide-up">
      {/* Back button */}
      <Link
        to="/knowledge-map"
        className="inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white transition mb-6"
      >
        ← Kembali ke Peta Belajar
      </Link>

      {/* Header */}
      <div className="glass-strong rounded-2xl p-6 border border-white/10 mb-6">
        <div className="flex items-start gap-4">
          <div className="w-14 h-14 rounded-2xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-2xl flex-shrink-0">
            🧭
          </div>
          <div className="flex-1">
            <h1 className="text-2xl font-black text-white mb-1">{path.name}</h1>
            <p className="text-gray-400 text-sm mb-3">{path.description || `Bagian dari topik ${path.topic?.name}`}</p>
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-xs px-3 py-1 rounded-full border font-medium ${diff.color}`}>
                {diff.icon} {diff.label}
              </span>
              <span className="text-xs px-3 py-1 rounded-full glass border border-white/10 text-gray-400">
                📚 {path.topic?.name}
              </span>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3 mt-5 pt-5 border-t border-white/5">
          <div className="text-center">
            <div className="text-lg font-black text-white">{path.missions?.length || 0}</div>
            <div className="text-xs text-gray-500">Misi</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-black text-yellow-400">{totalXP} XP</div>
            <div className="text-xs text-gray-500">Total XP</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-black text-cyan-400">{totalMinutes} min</div>
            <div className="text-xs text-gray-500">Durasi</div>
          </div>
        </div>
      </div>

      {/* Missions list */}
      <h2 className="text-lg font-bold text-white mb-4">Daftar Misi</h2>

      {path.missions?.length === 0 ? (
        <div className="text-center py-12 glass rounded-2xl border border-white/10">
          <div className="text-4xl mb-3">📭</div>
          <p className="text-gray-500 text-sm">Belum ada misi di jalur ini.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {path.missions?.map((mission, idx) => {
            const typeConfig = TYPE_CONFIG[mission.type] || TYPE_CONFIG.quiz;
            return (
              <Link
                key={mission.id}
                to={`/quiz/${mission.id}`}
                className="group block p-5 rounded-2xl glass border border-white/10 hover:border-indigo-500/30 hover:bg-indigo-500/5 transition-all card-hover"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-600/20 border border-indigo-500/20 flex items-center justify-center text-sm font-black text-indigo-300 flex-shrink-0 group-hover:border-indigo-400/50 transition">
                    {idx + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-white group-hover:text-indigo-200 transition">{mission.title}</h3>
                    <div className="flex items-center gap-3 mt-1">
                      <span className="text-xs text-gray-500">
                        {typeConfig.icon} {typeConfig.label}
                      </span>
                      <span className="text-gray-700">·</span>
                      <span className="text-xs text-gray-500">⏱️ {mission.estimated_minutes} menit</span>
                      <span className="text-gray-700">·</span>
                      <span className="text-xs text-yellow-500">⚡ {mission.xp_reward} XP</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      (mission.difficulty || 1) <= 1 ? 'bg-green-500/20 text-green-300' :
                      (mission.difficulty || 1) <= 2 ? 'bg-yellow-500/20 text-yellow-300' :
                      'bg-red-500/20 text-red-300'
                    }`}>
                      {'★'.repeat(Math.max(1, Math.min(3, mission.difficulty || 1)))}
                    </span>
                    <span className="text-indigo-400 group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}

      {/* Start All Button */}
      {path.missions?.length > 0 && (
        <div className="mt-6">
          <Link
            to={`/quiz/${path.missions[0].id}`}
            className="btn-primary w-full text-center py-4 text-base block glow-indigo"
          >
            🚀 Mulai dari Misi Pertama
          </Link>
        </div>
      )}
    </div>
  );
}
