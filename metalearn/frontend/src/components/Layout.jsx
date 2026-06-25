import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, useEffect } from 'react';
import NotificationBell from './NotificationBell';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/knowledge-map', label: 'Peta Belajar', icon: '🗺️' },
  { to: '/leaderboard', label: 'Peringkat', icon: '🏆' },
  { to: '/metacognitive', label: 'Analitik', icon: '🪞' },
  { to: '/chat', label: 'Chat AI', icon: '🤖' },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen" style={{ background: 'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.25) 0%, transparent 70%), linear-gradient(180deg, #060b1a 0%, #0d1225 50%, #060b1a 100%)' }}>
      {/* Animated background particles */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl float-animation" />
        <div className="absolute top-3/4 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl float-animation" style={{ animationDelay: '3s' }} />
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-pink-500/5 rounded-full blur-3xl float-animation" style={{ animationDelay: '1.5s' }} />
      </div>

      <header className={`sticky top-0 z-50 transition-all duration-300 ${scrolled ? 'glass-strong shadow-xl shadow-black/20' : 'border-b border-transparent'}`}>
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-sm font-bold shadow-lg group-hover:scale-110 transition-transform">
              M
            </div>
            <span className="text-xl font-bold gradient-text hidden sm:block">MetaLearn</span>
          </Link>

          {user && (
            <nav className="hidden md:flex items-center gap-1">
              {NAV_ITEMS.map((item) => (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive(item.to)
                      ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </nav>
          )}

          <div className="flex items-center gap-3">
            {user ? (
              <>
                <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl glass">
                  <div className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-xs font-bold">
                    {user.name?.[0]?.toUpperCase()}
                  </div>
                  <span className="text-sm text-gray-300 font-medium">{user.name}</span>
                </div>
                {user.role === 'guru' && (
                  <Link to="/teacher" className="hidden sm:block px-3 py-1.5 text-xs rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/30 transition">
                    🎓 Guru
                  </Link>
                )}
                <NotificationBell />
                <button
                  onClick={handleLogout}
                  className="px-3 py-1.5 text-xs rounded-xl glass text-gray-400 hover:text-white hover:bg-white/10 transition"
                >
                  Keluar
                </button>
                {/* Mobile menu toggle */}
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="md:hidden p-2 rounded-lg glass"
                >
                  <div className="w-4 h-4 flex flex-col justify-center gap-1">
                    <span className={`block h-0.5 bg-white transition-all ${mobileMenuOpen ? 'rotate-45 translate-y-1.5' : ''}`} />
                    <span className={`block h-0.5 bg-white transition-all ${mobileMenuOpen ? 'opacity-0' : ''}`} />
                    <span className={`block h-0.5 bg-white transition-all ${mobileMenuOpen ? '-rotate-45 -translate-y-1.5' : ''}`} />
                  </div>
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="px-4 py-2 text-sm rounded-xl glass text-gray-300 hover:text-white transition">
                  Masuk
                </Link>
                <Link to="/register" className="btn-primary text-sm px-4 py-2">
                  Daftar Gratis
                </Link>
              </>
            )}
          </div>
        </div>

        {/* Mobile nav */}
        {user && mobileMenuOpen && (
          <div className="md:hidden border-t border-white/10 glass-strong px-4 py-3">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm mb-1 transition-all ${
                  isActive(item.to)
                    ? 'bg-indigo-500/20 text-indigo-300'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        )}
      </header>

      <main className="container mx-auto px-4 py-6 relative z-10">
        <Outlet />
      </main>

      {/* Bottom nav for mobile */}
      {user && (
        <nav className="md:hidden fixed bottom-0 inset-x-0 z-50 glass-strong border-t border-white/10 px-4 py-2 flex justify-around">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`flex flex-col items-center gap-1 py-2 px-3 rounded-xl transition-all ${
                isActive(item.to) ? 'text-indigo-300' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="text-xs font-medium">{item.label.split(' ')[0]}</span>
            </Link>
          ))}
        </nav>
      )}
    </div>
  );
}
