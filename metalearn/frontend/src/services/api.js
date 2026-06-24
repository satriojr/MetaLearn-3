import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  profile: () => api.get('/auth/profile'),
};

export const topics = {
  list: () => api.get('/topics'),
  show: (id) => api.get(`/topics/${id}`),
  knowledgeMap: () => api.get('/knowledge-map'),
};

export const learningPaths = {
  list: () => api.get('/learning-paths'),
  show: (id) => api.get(`/learning-paths/${id}`),
};

export const missions = {
  show: (id) => api.get(`/missions/${id}`),
  start: (id) => api.post(`/missions/${id}/start`),
  submit: (id, data) => api.post(`/missions/${id}/submit`, data),
};

export const scanner = {
  getQuestions: () => api.get('/scanner/questions'),
  submit: (data) => api.post('/scanner/submit', data),
};

export const ai = {
  pauseAsk: (data) => api.post('/ai/pause-ask', data),
};

export const gamification = {
  stats: () => api.get('/gamification/stats'),
  leaderboard: (topicId) => api.get(`/gamification/leaderboard${topicId ? `?topic_id=${topicId}` : ''}`),
};

export const dashboard = {
  student: () => api.get('/dashboard/student'),
  teacher: () => api.get('/dashboard/teacher'),
  report: () => api.get('/dashboard/report'),
};

export const memory = {
  show: () => api.get('/memory'),
  destroy: () => api.delete('/memory'),
};

export default api;
