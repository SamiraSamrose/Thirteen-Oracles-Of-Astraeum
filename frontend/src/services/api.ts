### File: frontend/src/services/api.ts

/**
 * frontend/src/services/api.ts
 * STEP: REST API Client
 * Axios-based HTTP client for backend communication.
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

// API methods
export const gameAPI = {
  createGame: (difficulty: string = 'normal') =>
    api.post('/game/create', { difficulty }),
  
  getGame: (gameId: number) =>
    api.get(`/game/${gameId}`),
  
  saveGame: (gameId: number) =>
    api.post(`/game/${gameId}/save`),
  
  getInventory: (gameId: number) =>
    api.get(`/game/${gameId}/inventory`),
  
  useInsightToken: (gameId: number, question: string) =>
    api.post(`/game/${gameId}/insight`, { question }),
}

export const oracleAPI = {
  challengeOracle: (gameId: number, oracleName: string) =>
    api.post('/oracle/challenge', { oracle_name: oracleName }, { params: { game_id: gameId } }),
  
  solvePuzzle: (gameId: number, oracleStateId: number, solution: string) =>
    api.post(`/oracle/${gameId}/puzzle/solve`, { oracle_state_id: oracleStateId, solution }),
  
  startBattle: (gameId: number, oracleId: number) =>
    api.post(`/oracle/${gameId}/battle/start`, null, { params: { oracle_id: oracleId } }),
  
  executeBattleAction: (gameId: number, oracleId: number, action: string) =>
    api.post(`/oracle/${gameId}/battle/action`, { action }, { params: { oracle_id: oracleId } }),
  
  defeatOracle: (gameId: number, oracleId: number) =>
    api.post(`/oracle/${gameId}/defeat/${oracleId}`),
}