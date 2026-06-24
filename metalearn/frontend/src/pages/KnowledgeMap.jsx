import { useState, useEffect } from 'react';
import StarMap from '../components/StarMap';
import { topics } from '../services/api';

export default function KnowledgeMap() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    topics
      .knowledgeMap()
      .then((res) => setData(res.data))
      .catch(() => setError('Gagal memuat peta pengetahuan'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Memuat peta pengetahuan...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-20">
        <p className="text-red-400 mb-4">{error}</p>
        <button
          onClick={() => { setLoading(true); setError(''); topics.knowledgeMap().then(r => setData(r.data)).catch(() => setError('Gagal')).finally(() => setLoading(false)); }}
          className="px-4 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-600 transition text-sm"
        >
          Coba Lagi
        </button>
      </div>
    );
  }

  const masteryMap = {};
  data?.topics?.forEach((t) => {
    masteryMap[t.name] = t.mastery;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">Peta Pengetahuan</h2>
          <p className="text-gray-400 text-sm mt-1">
            Jelajahi topik sebagai konstelasi bintang. Seret untuk navigasi, klik untuk memulai.
          </p>
        </div>
        <div className="hidden md:flex items-center gap-4 text-xs text-gray-400">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-indigo-500 inline-block" /> Topik
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-indigo-400 inline-block opacity-70" /> Jalur Belajar
          </span>
          <span className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-white inline-block" /> Pusat
          </span>
        </div>
      </div>

      <div className="relative rounded-2xl bg-gradient-to-b from-indigo-950/60 via-purple-950/40 to-slate-950/60 border border-white/10 overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10" style={{ minHeight: '600px' }}>
          <StarMap topics={data?.topics || []} masteryScores={masteryMap} />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        {data?.topics?.map((topic) => (
          <div
            key={topic.id}
            className="p-3 rounded-xl bg-white/5 border border-white/10 text-center hover:bg-white/10 transition cursor-pointer"
            onClick={() => {
              const firstPath = topic.learning_paths?.[0];
              if (firstPath) window.location.href = `/missions/${firstPath.id}`;
            }}
          >
            <div
              className="w-8 h-8 rounded-full mx-auto mb-2 flex items-center justify-center text-xs font-bold"
              style={{ backgroundColor: topic.color_hex + '30', color: topic.color_hex }}
            >
              {topic.name[0]}
            </div>
            <p className="text-xs font-medium truncate">{topic.name}</p>
            <p className="text-xs text-gray-500">{topic.mastery}%</p>
          </div>
        ))}
      </div>
    </div>
  );
}
