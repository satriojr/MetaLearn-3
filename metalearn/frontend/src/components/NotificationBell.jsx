import { useState, useRef, useEffect } from 'react';
import { useNotifications } from '../context/NotificationContext';

const TYPE_ICONS = {
  badge_earned: '🏅',
  mission_completed: '✅',
  level_up: '⬆️',
  system: '🔔',
};

export default function NotificationBell() {
  const { notifications, unreadCount, markAsRead, markAllAsRead, fetchNotifications } =
    useNotifications();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleBellClick = () => {
    setOpen((prev) => !prev);
    if (!open) fetchNotifications();
  };

  const timeAgo = (dateStr) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'baru saja';
    if (mins < 60) return `${mins}m lalu`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}j lalu`;
    return `${Math.floor(hours / 24)}h lalu`;
  };

  return (
    <div ref={ref} className="relative">
      <button
        onClick={handleBellClick}
        className="relative p-2 rounded-xl glass text-gray-400 hover:text-white hover:bg-white/10 transition"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center bg-red-500 text-white text-xs font-bold rounded-full shadow-lg">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-80 max-h-96 overflow-y-auto rounded-2xl glass-strong border border-white/10 shadow-2xl shadow-black/30 z-50">
          <div className="sticky top-0 glass-strong border-b border-white/10 px-4 py-3 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white">Notifikasi</h3>
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="text-xs text-indigo-400 hover:text-indigo-300 transition"
              >
                Tandai semua dibaca
              </button>
            )}
          </div>

          {notifications.length === 0 ? (
            <div className="px-4 py-8 text-center text-gray-500 text-sm">
              Belum ada notifikasi
            </div>
          ) : (
            notifications.slice(0, 20).map((n) => {
              const isUnread = !n.read_at;
              const icon = TYPE_ICONS[n.type] || TYPE_ICONS.system;
              return (
                <button
                  key={n.id}
                  onClick={() => {
                    if (isUnread) markAsRead(n.id);
                  }}
                  className={`w-full text-left px-4 py-3 flex gap-3 transition hover:bg-white/5 ${
                    isUnread ? 'bg-indigo-500/5 border-l-2 border-indigo-500' : 'opacity-70'
                  }`}
                >
                  <span className="text-lg mt-0.5">{icon}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-white truncate">{n.data?.title || 'Notifikasi'}</p>
                    <p className="text-xs text-gray-400 mt-0.5 line-clamp-2">
                      {n.data?.body || ''}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">{timeAgo(n.created_at)}</p>
                  </div>
                </button>
              );
            })
          )}
        </div>
      )}
    </div>
  );
}
