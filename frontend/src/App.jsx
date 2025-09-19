import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import { useAuthStore } from './stores/authStore'
import { useEffect } from 'react'

// Components
import Navbar from './components/Layout/Navbar'
import LoginPage from './components/Auth/LoginPage'
import RegisterPage from './components/Auth/RegisterPage'
import Dashboard from './components/Dashboard/Dashboard'
import ScenarioList from './components/Scenarios/ScenarioList'
import ScenarioDetail from './components/Scenarios/ScenarioDetail'
import DiagramBuilder from './components/DiagramBuilder/DiagramBuilder'
import ScoreHistory from './components/Scoring/ScoreHistory'
import LearningPaths from './components/Learning/LearningPaths'
import Profile from './components/Profile/Profile'
import LoadingSpinner from './components/Common/LoadingSpinner'

function App() {
  const { user, isLoading, checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, pt: 8 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scenarios" element={<ScenarioList />} />
          <Route path="/scenarios/:id" element={<ScenarioDetail />} />
          <Route path="/diagram/:diagramId?" element={<DiagramBuilder />} />
          <Route path="/scores" element={<ScoreHistory />} />
          <Route path="/learning" element={<LearningPaths />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/login" element={<Navigate to="/" replace />} />
          <Route path="/register" element={<Navigate to="/" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Box>
    </Box>
  )
}

export default App