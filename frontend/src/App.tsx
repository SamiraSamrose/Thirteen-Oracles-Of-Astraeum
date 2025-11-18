### File: frontend/src/App.tsx

/**
 * frontend/src/App.tsx
 * STEP: Main Application Component
 * Manages authentication, game state, routing, WebSocket connection.
 */
import React, { useEffect, useState } from 'react'
import { useGameStore } from './store'
import { api } from './services/api'
import { WebSocketService } from './services/websocket'
import GameBoard from './components/GameBoard'
import LoginScreen from './components/LoginScreen'
import './App.css'

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const { gameId, playerId, setGameId, setPlayerId } = useGameStore()

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const response = await api.get('/auth/me')
        setPlayerId(response.data.id)
        setIsAuthenticated(true)
      } catch (error) {
        localStorage.removeItem('token')
      }
    }
    setIsLoading(false)
  }

  const handleLogin = async (username: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { username, password })
      localStorage.setItem('token', response.data.access_token)
      setPlayerId(response.data.player_id)
      setIsAuthenticated(true)
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  const handleRegister = async (username: string, email: string, password: string) => {
    try {
      const response = await api.post('/auth/register', { username, email, password })
      localStorage.setItem('token', response.data.access_token)
      setPlayerId(response.data.player_id)
      setIsAuthenticated(true)
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  if (isLoading) {
    return <div className="loading">Loading Astraeum...</div>
  }

  if (!isAuthenticated) {
    return <LoginScreen onLogin={handleLogin} onRegister={handleRegister} />
  }

  return <GameBoard />
}

export default App
