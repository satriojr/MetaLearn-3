import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(form.email, form.password);
      if (user?.interests?.length === 0) {
        navigate('/scanner');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Email atau password salah.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-2xl font-black mx-auto mb-4 glow-indigo">
            M
          </div>
          <h1 className="text-3xl font-black gradient-text mb-2">Selamat Datang</h1>
          <p className="text-gray-400 text-sm">Masuk untuk melanjutkan perjalanan belajarmu</p>
        </div>

        <div className="glass-strong rounded-2xl p-8 border border-white/10 slide-up">
          {error && (
            <div className="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
              ⚠️ {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="nama@email.com"
                required
                className="w-full px-4 py-3 rounded-xl glass border border-white/10 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 focus:bg-indigo-500/5 transition"
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium text-gray-300">Password</label>
              </div>
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="••••••••"
                required
                className="w-full px-4 py-3 rounded-xl glass border border-white/10 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 focus:bg-indigo-500/5 transition"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-4 text-base disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Memproses...
                </span>
              ) : (
                '🚀 Masuk'
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-white/5 text-center text-sm text-gray-500">
            Belum punya akun?{' '}
            <Link to="/register" className="text-indigo-400 hover:text-indigo-300 font-medium transition">
              Daftar sekarang →
            </Link>
          </div>
        </div>

        {/* Dev hint */}
        <div className="mt-4 p-3 rounded-xl border border-yellow-500/20 bg-yellow-500/5 text-xs text-gray-500">
          <strong className="text-yellow-400">Dev:</strong> student@metalearn.dev / password123
        </div>
      </div>
    </div>
  );
}
