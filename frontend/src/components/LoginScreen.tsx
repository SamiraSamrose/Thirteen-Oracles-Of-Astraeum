### File: frontend/src/components/LoginScreen.tsx

/**
 * frontend/src/components/LoginScreen.tsx
 * STEP: Login/Registration UI Component
 * Handles user authentication with styled forms.
 */
import React, { useState } from 'react'
import './LoginScreen.css'

interface LoginScreenProps {
  onLogin: (username: string, password: string) => Promise<void>
  onRegister: (username: string, email: string, password: string) => Promise<void>
}

const LoginScreen: React.FC<LoginScreenProps> = ({ onLogin, onRegister }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isLogin) {
        await onLogin(username, password)
      } else {
        await onRegister(username, email, password)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-background"></div>
      <div className="login-card">
        <h1 className="login-title">Thirteen Oracles of Astraeum</h1>
        <p className="login-subtitle">Enter the fractured realm of ancient Greece</p>
        
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="login-input"
          />
          
          {!isLogin && (
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="login-input"
            />
          )}
          
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="login-input"
          />
          
          {error && <div className="login-error">{error}</div>}
          
          <button type="submit" disabled={loading} className="login-button">
            {loading ? 'Loading...' : isLogin ? 'Enter Astraeum' : 'Create Account'}
          </button>
        </form>
        
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="login-toggle"
        >
          {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
        </button>
      </div>
    </div>
  )
}

export default LoginScreen