import { useState, useEffect } from 'react';
import { gamification } from '../services/api';

export default function Leaderboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    gamification.leaderboard()
      .then((res) => setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Memuat papan peringkat...</p>
      </div>
    </div>
  );

  const top3 = data.slice(0, 3);
  const rest = data.slice(3);

  const rankConfig = [
    { emoji: '🥇', bg: 'from-yellow-500/30 to-yellow-600/10', border: 'border-yellow-500/40', text: 'text-yellow-300', glow: 'shadow-yellow-500/20' },
    { emoji: '🥈', bg: 'from-gray-400/20 to-gray-500/5', border: 'border-gray-400/30', text: 'text-gray-300', glow: 'shadow-gray-400/20' },
    { emoji: '🥉', bg: 'from-orange-500/20 to-orange-600/5', border: 'border-orange-500/30', text: 'text-orange-300', glow: 'shadow-orange-500/20' },
  ];

  return (
    <div className="max-w-3xl mx-auto pb-20 slide-up">
      {/* Header */}
      <div className="text-center mb-10">
        <div className="text-5xl mb-4 float-animation">🏆</div>
        <h1 className="text-4xl font-black gradient-text mb-2">Papan Peringkat</h1>
        <p className="text-gray-400 text-sm">Kompetisi sehat antar pelajar. Belajar lebih — naik lebih tinggi!</p>
      </div>

      {/* Top 3 Podium */}
      {top3.length > 0 && (
        <div className="grid grid-cols-3 gap-4 mb-8 items-end">
          {/* 2nd place */}
          {top3[1] && (
            <div className={`p-5 rounded-2xl bg-gradient-to-br ${rankConfig[1].bg} border ${rankConfig[1].border} text-center card-hover shadow-lg ${rankConfig[1].glow}`} style={{ minHeight: '160px' }}>
              <div className="text-3xl mb-2">{rankConfig[1].emoji}</div>
              <div className={`text-xl font-black mb-1 ${rankConfig[1].text}`}>#{top3[1].rank}</div>
              <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-lg font-bold mx-auto mb-2">
                {top3[1].user.name?.[0]?.toUpperCase()}
              </div>
              <div className="text-sm font-semibold text-white truncate">{top3[1].user.name}</div>
              <div className="text-xs text-gray-500">Level {top3[1].level}</div>
              <div className="text-sm font-bold text-yellow-400 mt-1">{top3[1].xp.toLocaleString()} XP</div>
            </div>
          )}

          {/* 1st place */}
          {top3[0] && (
            <div className={`p-5 rounded-2xl bg-gradient-to-br ${rankConfig[0].bg} border ${rankConfig[0].border} text-center card-hover shadow-xl ${rankConfig[0].glow} scale-105`}>
              <div className="text-4xl mb-2 float-animation">{rankConfig[0].emoji}</div>
              <div className={`text-2xl font-black mb-1 ${rankConfig[0].text}`}>#{top3[0].rank}</div>
              <div className="w-14 h-14 rounded-full bg-yellow-500/20 border-2 border-yellow-500/40 flex items-center justify-center text-xl font-bold mx-auto mb-2">
                {top3[0].user.name?.[0]?.toUpperCase()}
              </div>
              <div className="text-sm font-bold text-white truncate">{top3[0].user.name}</div>
              <div className="text-xs text-gray-400">Level {top3[0].level}</div>
              <div className="text-base font-black text-yellow-400 mt-1">{top3[0].xp.toLocaleString()} XP</div>
            </div>
          )}

          {/* 3rd place */}
          {top3[2] && (
            <div className={`p-5 rounded-2xl bg-gradient-to-br ${rankConfig[2].bg} border ${rankConfig[2].border} text-center card-hover shadow-lg ${rankConfig[2].glow}`} style={{ minHeight: '150px' }}>
              <div className="text-3xl mb-2">{rankConfig[2].emoji}</div>
              <div className={`text-xl font-black mb-1 ${rankConfig[2].text}`}>#{top3[2].rank}</div>
              <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-lg font-bold mx-auto mb-2">
                {top3[2].user.name?.[0]?.toUpperCase()}
              </div>
              <div className="text-sm font-semibold text-white truncate">{top3[2].user.name}</div>
              <div className="text-xs text-gray-500">Level {top3[2].level}</div>
              <div className="text-sm font-bold text-yellow-400 mt-1">{top3[2].xp.toLocaleString()} XP</div>
            </div>
          )}
        </div>
      )}

      {/* Rest of leaderboard */}
      {rest.length > 0 && (
        <div className="glass rounded-2xl border border-white/10 overflow-hidden">
          <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between">
            <h3 className="font-bold text-white">Seluruh Pelajar</h3>
            <span className="text-xs text-gray-500">{data.length} Pelajar</span>
          </div>
          <div className="divide-y divide-white/5">
            {rest.map((entry) => (
              <div key={entry.rank} className="flex items-center justify-between px-6 py-4 hover:bg-white/5 transition">
                <div className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center text-sm text-gray-400 font-bold">
                    #{entry.rank}
                  </div>
                  <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500/30 to-purple-600/30 flex items-center justify-center text-sm font-bold text-white">
                    {entry.user.name?.[0]?.toUpperCase()}
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">{entry.user.name}</div>
                    <div className="text-xs text-gray-500">Level {entry.level}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-bold text-yellow-400">{entry.xp.toLocaleString()} XP</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.length === 0 && (
        <div className="text-center py-16">
          <div className="text-6xl mb-4">🌟</div>
          <h3 className="text-xl font-bold text-white mb-2">Belum Ada Pelajar</h3>
          <p className="text-gray-400 text-sm">Jadilah yang pertama menghiasi papan peringkat!</p>
        </div>
      )}
    </div>
  );
}
