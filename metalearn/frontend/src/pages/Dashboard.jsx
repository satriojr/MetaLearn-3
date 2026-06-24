import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { dashboard, gamification } from '../services/api';

function StatCard({ value, label, icon, color = 'indigo', trend }) {
  const colorMap = {
    indigo: 'from-indigo-500/15 to-indigo-600/5 border-indigo-500/20 text-indigo-300',
    yellow: 'from-yellow-500/15 to-yellow-600/5 border-yellow-500/20 text-yellow-300',
    green: 'from-green-500/15 to-green-600/5 border-green-500/20 text-green-300',
    purple: 'from-purple-500/15 to-purple-600/5 border-purple-500/20 text-purple-300',
    pink: 'from-pink-500/15 to-pink-600/5 border-pink-500/20 text-pink-300',
  };
  return (
    <div className={`p-5 rounded-2xl bg-gradient-to-br border card-hover ${colorMap[color]}`}>
      <div className="flex items-start justify-between mb-3">
        <span className="text-2xl">{icon}</span>
        {trend !== undefined && (
          <span className={`text-xs px-2 py-0.5 rounded-full ${trend >= 0 ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>
      <div className="text-3xl font-black mb-1">{value}</div>
      <div className="text-xs text-gray-500">{label}</div>
    </div>
  );
}

function MasteryBar({ topic, score }) {
  const getColor = (s) => s >= 80 ? '#4ade80' : s >= 50 ? '#facc15' : '#f87171';
  return (
    <div>
      <div className="flex justify-between text-sm mb-1.5">
        <span className="text-gray-300 font-medium">{topic}</span>
        <span className="font-bold" style={{ color: getColor(score) }}>{score}%</span>
      </div>
      <div className="w-full bg-white/5 rounded-full h-2">
        <div
          className="h-2 rounded-full progress-bar transition-all"
          style={{ width: `${score}%`, background: `linear-gradient(90deg, ${getColor(score)}88, ${getColor(score)})` }}
        />
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(true);
  const [showReport, setShowReport] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      dashboard.student(),
      gamification.leaderboard(),
    ])
      .then(([dashRes, lbRes]) => {
        setData(dashRes.data);
        setLeaderboard(lbRes.data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const loadReport = async () => {
    setGeneratingReport(true);
    setShowReport(true);
    try {
      const res = await dashboard.report();
      setReport(res.data.report);
    } catch {
      setReport('Gagal memuat laporan. Pastikan koneksi internet stabil.');
    } finally {
      setGeneratingReport(false);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Memuat dashboard...</p>
      </div>
    </div>
  );

  if (!data) return (
    <div className="text-center py-20">
      <div className="text-5xl mb-4">😕</div>
      <p className="text-gray-400">Gagal memuat data. Coba muat ulang halaman.</p>
    </div>
  );

  const g = data.gamification || {};
  const m = data.mastery || {};
  const profile = data.profile || {};
  const recentActivity = data.recent_activity || [];
  const masteryEntries = Object.entries(m.mastery_scores || {});
  const currentXp = g.xp || 0;
  const nextLevelXp = g.next_level_xp;
  const xpPct = nextLevelXp ? Math.min(100, Math.round((currentXp / nextLevelXp) * 100)) : 100;

  return (
    <div className="space-y-6 pb-20 slide-up">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white">
            Halo, <span className="gradient-text">{profile.name?.split(' ')[0] || 'Pelajar'}</span> 👋
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            {recentActivity.length > 0
              ? `Terakhir aktif belajar — teruskan momentummu!`
              : 'Mulai perjalanan belajarmu hari ini!'}
          </p>
        </div>
        <div className="flex gap-3">
          <Link to="/knowledge-map" className="btn-primary px-5 py-2.5 text-sm">
            🗺️ Lanjut Belajar
          </Link>
          <button
            onClick={loadReport}
            disabled={generatingReport}
            className="px-5 py-2.5 text-sm rounded-xl glass border border-purple-500/30 text-purple-300 hover:bg-purple-500/10 transition"
          >
            {generatingReport ? '⏳ Generating...' : '📝 Laporan AI'}
          </button>
        </div>
      </div>

      {/* Level XP Bar */}
      <div className="glass-strong rounded-2xl p-5 border border-white/10">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-lg font-black glow-indigo">
              {g.level?.number || 1}
            </div>
            <div>
              <div className="font-bold text-white">{g.level?.title || 'Pemula'}</div>
              <div className="text-xs text-gray-500">Level {g.level?.number || 1}</div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-lg font-black text-yellow-400">{currentXp.toLocaleString()} XP</div>
            {nextLevelXp && (
              <div className="text-xs text-gray-500">Target: {nextLevelXp.toLocaleString()} XP</div>
            )}
          </div>
        </div>
        <div className="w-full bg-white/5 rounded-full h-3">
          <div className="xp-bar h-3 rounded-full progress-bar relative" style={{ width: `${xpPct}%` }}>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 bg-white rounded-full shadow-lg" />
          </div>
        </div>
        <div className="flex justify-between text-xs text-gray-600 mt-1">
          <span>0 XP</span>
          <span>{xpPct}% menuju level berikutnya</span>
          <span>{nextLevelXp?.toLocaleString()} XP</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard value={g.level?.number || 1} label="Level Saat Ini" icon="⭐" color="indigo" />
        <StatCard value={`${currentXp.toLocaleString()}`} label="Total XP" icon="⚡" color="yellow" />
        <StatCard value={g.completed_missions || 0} label="Misi Selesai" icon="✅" color="green" />
        <StatCard value={g.badges?.length || 0} label="Lencana" icon="🏅" color="purple" />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Mastery Scores */}
        <div className="glass rounded-2xl p-6 border border-white/10">
          <div className="flex items-center justify-between mb-5">
            <h3 className="font-bold text-white">🧠 Skor Penguasaan</h3>
            <Link to="/metacognitive" className="text-xs text-indigo-400 hover:text-indigo-300 transition">
              Lihat Selengkapnya →
            </Link>
          </div>
          {masteryEntries.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-4xl mb-3">📚</div>
              <p className="text-sm text-gray-500">Belum ada data. Mulai belajar untuk melihat perkembanganmu!</p>
              <Link to="/knowledge-map" className="inline-block mt-3 text-xs text-indigo-400 hover:text-indigo-300">
                Mulai Sekarang →
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {masteryEntries.map(([topic, score]) => (
                <MasteryBar key={topic} topic={topic} score={score} />
              ))}
            </div>
          )}

          {m.confusion_zones?.length > 0 && (
            <div className="mt-4 p-3 rounded-xl bg-orange-500/10 border border-orange-500/20 text-xs text-orange-300">
              ⚠️ Area kebingungan: {m.confusion_zones.join(', ')}
            </div>
          )}
        </div>

        {/* Leaderboard */}
        <div className="glass rounded-2xl p-6 border border-white/10">
          <div className="flex items-center justify-between mb-5">
            <h3 className="font-bold text-white">🏆 Papan Peringkat</h3>
            <Link to="/leaderboard" className="text-xs text-indigo-400 hover:text-indigo-300 transition">
              Lihat Semua →
            </Link>
          </div>
          {leaderboard.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-4xl mb-3">🌟</div>
              <p className="text-sm text-gray-500">Belum ada data. Jadilah yang pertama!</p>
            </div>
          ) : (
            <div className="space-y-2">
              {leaderboard.slice(0, 8).map((entry) => (
                <div
                  key={entry.rank}
                  className={`flex items-center justify-between px-3 py-2.5 rounded-xl transition ${
                    entry.rank <= 3 ? 'bg-yellow-500/10 border border-yellow-500/20' : 'hover:bg-white/5'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
                      entry.rank === 1 ? 'bg-yellow-500/30 text-yellow-300' :
                      entry.rank === 2 ? 'bg-gray-400/20 text-gray-300' :
                      entry.rank === 3 ? 'bg-orange-500/20 text-orange-300' :
                      'bg-white/5 text-gray-500'
                    }`}>
                      {entry.rank <= 3 ? ['🥇','🥈','🥉'][entry.rank-1] : `#${entry.rank}`}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-white">{entry.user.name}</div>
                      <div className="text-xs text-gray-500">Level {entry.level}</div>
                    </div>
                  </div>
                  <div className="text-sm font-bold text-yellow-400">{entry.xp.toLocaleString()} XP</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Badges */}
      {g.badges?.length > 0 && (
        <div className="glass rounded-2xl p-6 border border-white/10">
          <h3 className="font-bold text-white mb-4">🏅 Lencana Diraih</h3>
          <div className="flex flex-wrap gap-3">
            {g.badges.map((badge) => (
              <div
                key={badge.id}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-yellow-500/10 border border-yellow-500/20 card-hover cursor-default"
                title={badge.description}
              >
                <span>🏅</span>
                <div>
                  <div className="text-sm font-medium text-yellow-300">{badge.name}</div>
                  {badge.description && <div className="text-xs text-gray-500">{badge.description}</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Activity */}
      {recentActivity.length > 0 && (
        <div className="glass rounded-2xl p-6 border border-white/10">
          <h3 className="font-bold text-white mb-4">⚡ Aktivitas Terbaru</h3>
          <div className="space-y-3">
            {recentActivity.map((act, idx) => (
              <div key={idx} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-sm ${
                    act.status === 'completed' ? 'bg-green-500/20' : 'bg-yellow-500/20'
                  }`}>
                    {act.status === 'completed' ? '✅' : '🔄'}
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">{act.mission?.title || 'Misi'}</div>
                    <div className="text-xs text-gray-500">
                      {act.completed_at ? new Date(act.completed_at).toLocaleDateString('id-ID') : '—'}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  {act.score > 0 && <div className="text-sm font-bold text-indigo-300">{act.score}%</div>}
                  {act.xp_earned > 0 && <div className="text-xs text-yellow-400">+{act.xp_earned} XP</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Report */}
      {showReport && (
        <div className="glass rounded-2xl p-6 border border-purple-500/20 slide-up">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">🤖</div>
            <h3 className="font-bold text-white">Laporan Perkembangan AI</h3>
          </div>
          {generatingReport ? (
            <div className="flex items-center gap-3 py-6 text-gray-400">
              <div className="w-5 h-5 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
              <span>AI sedang menganalisis data belajarmu...</span>
            </div>
          ) : (
            <div className="prose prose-invert max-w-none text-sm leading-relaxed whitespace-pre-wrap text-gray-300">
              {report}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
