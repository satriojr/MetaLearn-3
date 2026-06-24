import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Scanner from './pages/Scanner'
import Topics from './pages/Topics'
import KnowledgeMap from './pages/KnowledgeMap'
import Missions from './pages/Missions'
import Quiz from './pages/Quiz'
import Dashboard from './pages/Dashboard'
import Leaderboard from './pages/Leaderboard'
import MetacognitiveDashboard from './pages/MetacognitiveDashboard'
import TeacherDashboard from './pages/TeacherDashboard'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-gray-400 text-sm">Memuat...</p>
      </div>
    </div>
  )
  if (!user) return <Navigate to="/login" replace />
  return children
}

function TeacherRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  if (!user) return <Navigate to="/login" replace />
  if (user.role !== 'guru' && user.role_id !== 2) return <Navigate to="/dashboard" replace />
  return children
}

function ScannerGuard({ children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  if (!user) return <Navigate to="/login" replace />
  if (user.interests?.length > 0) return <Navigate to="/knowledge-map" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/scanner" element={<ScannerGuard><Scanner /></ScannerGuard>} />
        <Route path="/topics" element={<ProtectedRoute><Topics /></ProtectedRoute>} />
        <Route path="/knowledge-map" element={<ProtectedRoute><KnowledgeMap /></ProtectedRoute>} />
        <Route path="/missions/:pathId" element={<ProtectedRoute><Missions /></ProtectedRoute>} />
        <Route path="/quiz/:missionId" element={<ProtectedRoute><Quiz /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/leaderboard" element={<ProtectedRoute><Leaderboard /></ProtectedRoute>} />
        <Route path="/metacognitive" element={<ProtectedRoute><MetacognitiveDashboard /></ProtectedRoute>} />
        <Route path="/teacher" element={<TeacherRoute><TeacherDashboard /></TeacherRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
