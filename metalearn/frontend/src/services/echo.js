import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

const isSecure = window.location.protocol === 'https:';

const echo = new Echo({
  broadcaster: 'reverb',
  key: 'metalearn-key',
  wsHost: window.location.hostname,
  wsPort: 8080,
  wssPort: 8080,
  forceTLS: isSecure,
  enabledTransports: ['ws', 'wss'],
});

export default echo;
