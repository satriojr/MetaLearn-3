import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '', password_confirmation: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.password_confirmation) {
      setError('Password tidak sama. Periksa kembali.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      await register(form);
      navigate('/scanner');
    } catch (err) {
      const msgs = err.response?.data?.errors;
      setError(msgs ? Object.values(msgs).flat().join(' ') : (err.response?.data?.message || 'Pendaftaran gagal.'));
    } finally {
      setLoading(false);
    }
  };

  const strength = () => {
    const p = form.password;
    if (!p) return 0;
    let score = 0;
    if (p.length >= 8) score++;
    if (/[A-Z]/.test(p)) score++;
    if (/[0-9]/.test(p)) score++;
    if (/[^A-Za-z0-9]/.test(p)) score++;
    return score;
  };

  const strengthColors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500'];
  const strengthLabels = ['Lemah', 'Cukup', 'Baik', 'Kuat'];
  const s = strength();

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-2xl font-black mx-auto mb-4 glow-indigo">
            M
          </div>
          <h1 className="text-3xl font-black gradient-text mb-2">Buat Akun Baru</h1>
          <p className="text-gray-400 text-sm">Mulai perjalanan belajar adaptifmu hari ini</p>
        </div>

        <div className="glass-strong rounded-2xl p-8 border border-white/10 slide-up">
          {error && (
            <div className="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
              ⚠️ {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Nama Lengkap</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="Nama kamu"
                required
                className="w-full px-4 py-3 rounded-xl glass border border-white/10 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="nama@email.com"
                required
                className="w-full px-4 py-3 rounded-xl glass border border-white/10 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="Minimal 8 karakter"
                required
                minLength={8}
                className="w-full px-4 py-3 rounded-xl glass border border-white/10 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 transition"
              />
              {form.password && (
                <div className="mt-2">
                  <div className="flex gap-1 mb-1">
                    {[1,2,3,4].map((i) => (
                      <div key={i} className={`h-1 flex-1 rounded-full transition-all ${i <= s ? strengthColors[s-1] : 'bg-white/10'}`} />
                    ))}
                  </div>
                  <span className="text-xs text-gray-500">Kekuatan: <span className="text-white">{strengthLabels[s-1] || '—'}</span></span>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Konfirmasi Password</label>
              <input
                type="password"
                value={form.password_confirmation}
                onChange={(e) => setForm({ ...form, password_confirmation: e.target.value })}
                placeholder="Ulangi password"
                required
                className={`w-full px-4 py-3 rounded-xl glass border text-white placeholder-gray-600 focus:outline-none transition ${
                  form.password_confirmation && form.password !== form.password_confirmation
                    ? 'border-red-500/50 bg-red-500/5'
                    : 'border-white/10 focus:border-indigo-500/50'
                }`}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-4 text-base disabled:opacity-50 mt-2"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Mendaftarkan...
                </span>
              ) : (
                '🎓 Daftar & Mulai Belajar'
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-white/5 text-center text-sm text-gray-500">
            Sudah punya akun?{' '}
            <Link to="/login" className="text-indigo-400 hover:text-indigo-300 font-medium transition">
              Masuk sekarang →
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
