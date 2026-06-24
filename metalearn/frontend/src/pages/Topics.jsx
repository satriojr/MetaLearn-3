import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { topics } from '../services/api';

export default function Topics() {
  const [topicList, setTopicList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    topics.list()
      .then((res) => setTopicList(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-20 text-gray-400">Memuat peta belajar...</div>;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-2">Peta Pengetahuan</h2>
      <p className="text-gray-400 mb-8">Jelajahi topik dan jalur belajar yang tersedia</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {topicList.map((topic) => (
          <div key={topic.id} className="rounded-xl bg-white/5 border border-white/10 overflow-hidden">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center text-lg" style={{ backgroundColor: topic.color_hex + '30' }}>
                  <span style={{ color: topic.color_hex }}>{topic.icon}</span>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{topic.name}</h3>
                  <span className="text-xs text-gray-400">{topic.category}</span>
                </div>
              </div>
              <p className="text-sm text-gray-400 mb-4">{topic.description}</p>
              <div className="space-y-2">
                {topic.learning_paths?.slice(0, 3).map((path) => (
                  <Link
                    key={path.id}
                    to={`/missions/${path.id}`}
                    className="block p-3 rounded-lg bg-white/5 hover:bg-white/10 transition text-sm"
                  >
                    <div className="flex items-center justify-between">
                      <span>{path.name}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        path.difficulty_level === 'beginner' ? 'bg-green-500/20 text-green-300' :
                        path.difficulty_level === 'intermediate' ? 'bg-yellow-500/20 text-yellow-300' :
                        'bg-red-500/20 text-red-300'
                      }`}>
                        {path.difficulty_level}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
