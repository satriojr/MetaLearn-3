import { useState, useEffect } from 'react';
import { dashboard } from '../services/api';

export default function TeacherDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('xp');

  useEffect(() => {
    dashboard.teacher()
      .then((res) => setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Memuat data kelas...</p>
      </div>
    </div>
  );

  const stats = data?.class_stats || {};
  const allStudents = data?.students || [];
  const stagnantStudents = allStudents.filter((s) => (s.missions_completed || 0) === 0);
  const students = allStudents
    .filter((s) => s.name?.toLowerCase().includes(search.toLowerCase()) || s.email?.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'xp') return (b.xp || 0) - (a.xp || 0);
      if (sortBy === 'missions') return (b.missions_completed || 0) - (a.missions_completed || 0);
      if (sortBy === 'level') return (b.level || 1) - (a.level || 1);
      if (sortBy === 'name') return a.name?.localeCompare(b.name);
      return 0;
    });

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Belum aktif';
    return new Date(dateStr).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 space-y-6 slide-up">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-white">
            🎓 Dashboard <span className="gradient-text">Guru</span>
          </h1>
          <p className="text-gray-400 text-sm mt-1">Pantau perkembangan seluruh siswa di kelasmu secara real-time</p>
        </div>
        <button
          disabled
          className="px-5 py-2.5 text-sm rounded-xl glass border border-white/5 text-gray-500 cursor-not-allowed"
          title="Fitur ekspor sedang dalam pengembangan"
        >
          📥 Ekspor Data
        </button>
      </div>

      {/* Class Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Siswa', value: stats.total_students || 0, icon: '👥', color: 'from-blue-500/15 to-blue-600/5 border-blue-500/20 text-blue-300' },
          { label: 'Rata-rata XP', value: (stats.average_xp || 0).toLocaleString(), icon: '⚡', color: 'from-yellow-500/15 to-yellow-600/5 border-yellow-500/20 text-yellow-300' },
          { label: 'Rata-rata Misi', value: stats.average_missions || 0, icon: '✅', color: 'from-green-500/15 to-green-600/5 border-green-500/20 text-green-300' },
          { label: 'Perlu Perhatian', value: stagnantStudents.length, icon: '⚠️', color: 'from-red-500/15 to-red-600/5 border-red-500/20 text-red-300' },
        ].map((m) => (
          <div key={m.label} className={`p-5 rounded-2xl bg-gradient-to-br border card-hover ${m.color}`}>
            <div className="text-2xl mb-2">{m.icon}</div>
            <div className="text-2xl font-black mb-1">{m.value}</div>
            <div className="text-xs text-gray-500">{m.label}</div>
          </div>
        ))}
      </div>

      {/* Top Student Spotlight */}
      {stats.top_student && (
        <div className="glass rounded-2xl p-6 border border-yellow-500/20">
          <div className="flex items-center gap-4">
            <div className="text-3xl">🏆</div>
            <div className="flex-1">
              <h3 className="font-bold text-white mb-0.5">Siswa Terbaik Kelas</h3>
              <p className="text-2xl font-black text-yellow-400">{stats.top_student.name}</p>
              <p className="text-sm text-gray-500">
                Level {stats.top_student.level} · {stats.top_student.xp?.toLocaleString()} XP · {stats.top_student.missions_completed} misi selesai
              </p>
            </div>
            <div className="w-16 h-16 rounded-2xl bg-yellow-500/20 border-2 border-yellow-500/40 flex items-center justify-center text-2xl font-black text-yellow-400">
              {stats.top_student.name?.[0]?.toUpperCase()}
            </div>
          </div>
        </div>
      )}

      {/* Stagnant Alert */}
      {stagnantStudents.length > 0 && (
        <div className="glass rounded-2xl p-5 border border-orange-500/30">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div className="flex-1">
              <h3 className="font-bold text-orange-300 mb-2">Siswa yang Perlu Perhatian</h3>
              <p className="text-sm text-gray-400 mb-3">{stagnantStudents.length} siswa belum menyelesaikan misi apapun.</p>
              <div className="flex flex-wrap gap-2">
                {stagnantStudents.map((s) => (
                  <span key={s.id} className="px-3 py-1 rounded-lg bg-orange-500/10 border border-orange-500/20 text-sm text-orange-300">
                    {s.name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Student Table */}
      <div className="glass rounded-2xl border border-white/10 overflow-hidden">
        {/* Table controls */}
        <div className="px-6 py-4 border-b border-white/5 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">🔍</span>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Cari siswa..."
              className="w-full pl-9 pr-4 py-2 rounded-xl glass border border-white/10 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 transition"
            />
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 rounded-xl glass border border-white/10 text-gray-300 text-sm focus:outline-none bg-transparent"
          >
            <option value="xp" className="bg-gray-900">Urutkan: XP</option>
            <option value="missions" className="bg-gray-900">Urutkan: Misi</option>
            <option value="level" className="bg-gray-900">Urutkan: Level</option>
            <option value="name" className="bg-gray-900">Urutkan: Nama</option>
          </select>
        </div>

        {/* Table header */}
        <div className="hidden sm:grid grid-cols-6 px-6 py-3 text-xs font-semibold text-gray-600 border-b border-white/5 uppercase tracking-wide">
          <span className="col-span-2">Siswa</span>
          <span className="text-center">Level</span>
          <span className="text-center">XP</span>
          <span className="text-center">Misi Selesai</span>
          <span className="text-right">Terakhir Aktif</span>
        </div>

        {/* Table rows */}
        <div className="divide-y divide-white/5">
          {students.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              {search ? 'Tidak ada siswa yang cocok dengan pencarian.' : 'Belum ada siswa terdaftar.'}
            </div>
          ) : (
            students.map((student) => {
              const isAboveAvg = student.xp >= stats.average_xp;
              const isStagnant = student.missions_completed === 0;
              return (
                <div key={student.id} className={`px-6 py-4 hover:bg-white/5 transition ${isStagnant ? 'border-l-2 border-orange-500/50' : ''}`}>
                  <div className="hidden sm:grid grid-cols-6 items-center">
                    <div className="col-span-2 flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500/30 to-purple-600/30 flex items-center justify-center text-sm font-bold text-white flex-shrink-0">
                        {student.name?.[0]?.toUpperCase()}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-white">{student.name}</div>
                        <div className="text-xs text-gray-500">{student.email}</div>
                      </div>
                    </div>
                    <div className="text-center">
                      <span className="px-2.5 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 text-xs font-bold">
                        Lv. {student.level || 1}
                      </span>
                    </div>
                    <div className="text-center">
                      <span className={`text-sm font-bold ${isAboveAvg ? 'text-green-400' : 'text-gray-400'}`}>
                        {(student.xp || 0).toLocaleString()}
                      </span>
                      {isAboveAvg && <span className="ml-1 text-xs text-green-500">↑</span>}
                    </div>
                    <div className="text-center">
                      <span className={`text-sm font-bold ${isStagnant ? 'text-orange-400' : 'text-white'}`}>
                        {student.missions_completed || 0}
                      </span>
                      {isStagnant && <span className="ml-1 text-xs text-orange-500">!</span>}
                    </div>
                    <div className="text-right text-xs text-gray-500">
                      {formatDate(student.last_active)}
                    </div>
                  </div>

                  {/* Mobile view */}
                  <div className="sm:hidden flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500/30 to-purple-600/30 flex items-center justify-center text-sm font-bold text-white">
                        {student.name?.[0]?.toUpperCase()}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-white">{student.name}</div>
                        <div className="text-xs text-gray-500">Lv.{student.level || 1} · {student.missions_completed || 0} misi</div>
                      </div>
                    </div>
                    <div className="text-sm font-bold text-yellow-400">{(student.xp || 0).toLocaleString()} XP</div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
