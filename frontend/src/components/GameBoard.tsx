### File: frontend/src/components/GameBoard.tsx

/**
 * frontend/src/components/GameBoard.tsx
 * STEP: Main Game Board Component
 * Orchestrates game UI, oracle selection, battles, puzzles.
 */
import React, { useEffect, useState } from 'react'
import { useGameStore } from '../store'
import { gameAPI } from '../services/api'
import { wsService } from '../services/websocket'
import MapViewer from './MapViewer'
import OracleInterface from './OracleInterface'
import InventoryPanel from './InventoryPanel'
import './GameBoard.css'

const GameBoard: React.FC = () => {
  const {
    gameId,
    setGameId,
    playerId,
    gameState,
    setGameState,
    currentPhase,
    setCurrentPhase,
    showInventory,
    setShowInventory,
    notification,
    setNotification,
  } = useGameStore()

  const [loading, setLoading] = useState(true)

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = async () => {
    try {
      if (!gameId) {
        const response = await gameAPI.createGame('normal')
        const newGameId = response.data.game_id
        setGameId(newGameId)
        loadGameState(newGameId)
      } else {
        loadGameState(gameId)
      }

      if (playerId && gameId) {
        wsService.connect(gameId, playerId)
        setupWebSocketHandlers()
      }
    } catch (error) {
      console.error('Failed to initialize game:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadGameState = async (id: number) => {
    try {
      const response = await gameAPI.getGame(id)
      setGameState(response.data)
    } catch (error) {
      console.error('Failed to load game state:', error)
    }
  }

  const setupWebSocketHandlers = () => {
    wsService.on('player_action', (data) => {
      console.log('Player action:', data)
    })

    wsService.on('oracle_defeated', (data) => {
      setNotification(`Oracle ${data.oracle_name} has been defeated!`)
      setTimeout(() => setNotification(null), 5000)
    })

    wsService.on('game_event', (data) => {
      console.log('Game event:', data)
    })
  }

  if (loading) {
    return <div className="game-loading">Initializing Astraeum...</div>
  }

  return (
    <div className="game-board">
      <header className="game-header">
        <h1 className="game-title">Thirteen Oracles of Astraeum</h1>
        <div className="game-stats">
          <span>Stage: {gameState?.current_stage}/13</span>
          <span>Oracles Defeated: {gameState?.oracles_defeated}/13</span>
          <span>Gold: {gameState?.resources.gold}</span>
          <span>Insight Tokens: {gameState?.resources.insight_tokens}</span>
        </div>
        <button onClick={() => setShowInventory(!showInventory)} className="inventory-btn">
          Inventory
        </button>
      </header>

      {notification && (
        <div className="notification">{notification}</div>
      )}

      <main className="game-main">
        {currentPhase === 'menu' && <MapViewer />}
        {(currentPhase === 'puzzle' || currentPhase === 'battle' || currentPhase === 'confrontation') && (
          <OracleInterface />
        )}
      </main>

      {showInventory && <InventoryPanel />}
    </div>
  )
}

export default GameBoard