import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const FEATURES = [
  {
    icon: '🤖',
    title: 'Adaptive Learning',
    desc: 'Jalur belajar dikalibrasi AI secara real-time sesuai kecepatan kognitif individu',
    color: 'from-indigo-500/20 to-indigo-600/10',
    border: 'border-indigo-500/20',
    glow: 'rgba(99,102,241,0.15)',
  },
  {
    icon: '🎮',
    title: 'Gamification',
    desc: 'Kumpulkan XP, raih lencana adaptif, dan naikkan level. Belajar terasa seperti bermain.',
    color: 'from-purple-500/20 to-purple-600/10',
    border: 'border-purple-500/20',
    glow: 'rgba(168,85,247,0.15)',
  },
  {
    icon: '💬',
    title: 'Pause & Ask AI',
    desc: 'Tanya AI kapan saja tanpa mengganggu alur belajarmu. Jawaban kontekstual instan.',
    color: 'from-pink-500/20 to-pink-600/10',
    border: 'border-pink-500/20',
    glow: 'rgba(236,72,153,0.15)',
  },
  {
    icon: '🧠',
    title: 'Project Memory',
    desc: 'AI mengingat konteks belajarmu lintas sesi. Tidak ada perkenalan ulang setiap kali login.',
    color: 'from-emerald-500/20 to-emerald-600/10',
    border: 'border-emerald-500/20',
    glow: 'rgba(16,185,129,0.15)',
  },
  {
    icon: '🗺️',
    title: 'Knowledge Map',
    desc: 'Peta belajar berbentuk konstelasi bintang interaktif. Jelajahi topik secara non-linear.',
    color: 'from-yellow-500/20 to-yellow-600/10',
    border: 'border-yellow-500/20',
    glow: 'rgba(234,179,8,0.15)',
  },
  {
    icon: '📊',
    title: 'Metacognitive Dashboard',
    desc: 'Peta panas kebingungan, saran strategi belajar, dan rekap kompetensi personal.',
    color: 'from-cyan-500/20 to-cyan-600/10',
    border: 'border-cyan-500/20',
    glow: 'rgba(6,182,212,0.15)',
  },
];

const STATS = [
  { value: '72nd', label: 'Posisi Indonesia di PISA 2022', icon: '📉' },
  { value: '31.3%', label: 'Peningkatan partisipasi dengan gamifikasi', icon: '📈' },
  { value: '≥80%', label: 'Threshold penguasaan untuk lanjut topik', icon: '🎯' },
  { value: '10K+', label: 'Target pengguna konkuren', icon: '👥' },
];

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="pb-20">
      {/* Hero Section */}
      <section className="relative text-center pt-16 pb-24 overflow-hidden">
        {/* Decorative rings */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-[600px] h-[600px] rounded-full border border-indigo-500/10 star-spin" />
          <div className="absolute w-[400px] h-[400px] rounded-full border border-purple-500/10 star-spin" style={{ animationDirection: 'reverse', animationDuration: '15s' }} />
        </div>

        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-indigo-500/30 text-indigo-300 text-sm font-medium mb-8 slide-up">
          <span className="w-2 h-2 rounded-full bg-indigo-400 pulse-slow" />
          Samsung Solve for Tomorrow 2026 · Tim NexaNode
        </div>

        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black mb-6 leading-tight slide-up" style={{ animationDelay: '0.1s' }}>
          Belajar Lebih Cerdas
          <br />
          <span className="gradient-text">dengan AI Adaptif</span>
        </h1>

        <p className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed slide-up" style={{ animationDelay: '0.2s' }}>
          MetaLearn adalah platform pembelajaran berbasis AI yang menyesuaikan jalur belajar 
          secara real-time sesuai kecepatan kognitif setiap siswa. Bukan kurikulum seragam — 
          tapi pendidikan yang <em className="text-indigo-300 not-italic">diciptakan untukmu</em>.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 slide-up" style={{ animationDelay: '0.3s' }}>
          {user ? (
            <Link to="/knowledge-map" className="btn-primary text-base px-8 py-4 glow-indigo">
              🗺️ Buka Peta Belajar
            </Link>
          ) : (
            <>
              <Link to="/register" className="btn-primary text-base px-8 py-4 glow-indigo">
                🚀 Mulai Gratis Sekarang
              </Link>
              <Link to="/login" className="px-8 py-4 rounded-xl glass text-gray-300 hover:text-white hover:bg-white/10 transition text-base font-medium border border-white/10">
                Sudah punya akun? Masuk →
              </Link>
            </>
          )}
        </div>

        {/* Scroll indicator */}
        <div className="mt-16 flex flex-col items-center gap-2 text-gray-600 text-xs">
          <div className="w-5 h-8 rounded-full border-2 border-gray-700 flex items-start justify-center pt-1.5">
            <div className="w-1 h-2 bg-gray-600 rounded-full float-animation" />
          </div>
          <span>Scroll untuk lihat lebih</span>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-20">
        {STATS.map((stat) => (
          <div key={stat.label} className="glass rounded-2xl p-5 text-center card-hover border border-white/5">
            <div className="text-3xl mb-2">{stat.icon}</div>
            <div className="text-2xl font-black gradient-text mb-1">{stat.value}</div>
            <div className="text-xs text-gray-500">{stat.label}</div>
          </div>
        ))}
      </section>

      {/* Features Grid */}
      <section className="mb-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-black mb-4">
            Teknologi yang <span className="gradient-text">Bekerja Untukmu</span>
          </h2>
          <p className="text-gray-400 max-w-xl mx-auto">
            Setiap fitur dirancang berdasarkan riset psikologi kognitif dan teknologi AI terkini
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((f, idx) => (
            <div
              key={f.title}
              className={`p-6 rounded-2xl bg-gradient-to-br ${f.color} border ${f.border} card-hover cursor-default slide-up`}
              style={{ animationDelay: `${idx * 0.1}s`, boxShadow: `0 0 40px ${f.glow}` }}
            >
              <div className="text-4xl mb-4">{f.icon}</div>
              <h3 className="text-lg font-bold mb-2 text-white">{f.title}</h3>
              <p className="text-sm text-gray-400 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mb-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-black mb-4">
            Bagaimana <span className="gradient-text">MetaLearn Bekerja?</span>
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-0">
          {[
            { step: '01', title: 'Scan Minat', desc: 'Kuis interaktif singkat memetakan minat dan gaya belajarmu', icon: '🔍' },
            { step: '02', title: 'AI Merancang Jalur', desc: 'AI menyusun learning path personal berdasarkan profilmu', icon: '🧭' },
            { step: '03', title: 'Belajar Adaptif', desc: 'Materi mengalir dinamis sesuai kecepatan pemahamanmu', icon: '⚡' },
            { step: '04', title: 'AI Mengingat Segalanya', desc: 'Memori persisten membuat AI mengenalmu di setiap sesi', icon: '🧠' },
          ].map((item, idx) => (
            <div key={item.step} className="relative flex flex-col md:flex-row items-start md:items-center">
              <div className="flex-1 p-6 text-center md:text-left">
                <div className="text-5xl font-black text-indigo-500/20 mb-2">{item.step}</div>
                <div className="text-2xl mb-2">{item.icon}</div>
                <h3 className="font-bold mb-1 text-white">{item.title}</h3>
                <p className="text-sm text-gray-400">{item.desc}</p>
              </div>
              {idx < 3 && (
                <div className="hidden md:block text-gray-700 text-2xl px-2">→</div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      {!user && (
        <section className="animated-border rounded-3xl p-12 text-center" style={{ background: 'linear-gradient(135deg, rgba(99,102,241,0.1), rgba(168,85,247,0.1))' }}>
          <h2 className="text-3xl sm:text-4xl font-black mb-4">
            Siap Mengubah Cara Belajarmu?
          </h2>
          <p className="text-gray-400 mb-8 max-w-lg mx-auto">
            Bergabung bersama ribuan siswa yang telah merasakan perbedaan belajar dengan AI adaptif
          </p>
          <Link to="/register" className="btn-primary text-base px-10 py-4 glow-indigo inline-block">
            🎓 Daftar Sekarang — Gratis!
          </Link>
        </section>
      )}
    </div>
  );
}
