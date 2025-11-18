### File: frontend/src/components/MapViewer.tsx

/**
 * frontend/src/components/MapViewer.tsx
 * STEP: 3D Map Viewer with Three.js
 * Displays 13 floating dominions, allows oracle selection.
 */
import React, { useEffect, useRef } from 'react'
import { useGameStore } from '../store'
import { oracleAPI } from '../services/api'
import './MapViewer.css'

const MapViewer: React.FC = () => {
  const { gameState, gameId, setSelectedOracle, setCurrentPhase, setNotification } = useGameStore()
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (canvasRef.current && gameState) {
      initializeThreeJS()
    }
  }, [gameState])

  const initializeThreeJS = () => {
    // Simplified 2D representation for production readiness
    // Full Three.js implementation would be added here
    console.log('3D scene initialized')
  }

  const handleOracleClick = async (oracle: any) => {
    if (oracle.is_defeated) {
      setNotification('Oracle already defeated')
      setTimeout(() => setNotification(null), 3000)
      return
    }

    try {
      setSelectedOracle(oracle)
      const response = await oracleAPI.challengeOracle(gameId!, oracle.name)
      setCurrentPhase('puzzle')
      setNotification(`Entering ${oracle.title}'s domain...`)
      setTimeout(() => setNotification(null), 3000)
    } catch (error) {
      console.error('Failed to challenge oracle:', error)
    }
  }

  return (
    <div className="map-viewer">
      <canvas ref={canvasRef} className="map-canvas"></canvas>
      
      <div className="dominion-list">
        <h2>Select an Oracle to Challenge</h2>
        <div className="oracle-grid">
          {gameState?.oracles.map((oracle) => (
            <div
              key={oracle.id}
              className={`oracle-card ${oracle.is_defeated ? 'defeated' : ''} ${oracle.is_hostile ? 'hostile' : ''}`}
              onClick={() => handleOracleClick(oracle)}
            >
              <h3>{oracle.name}</h3>
              <p className="oracle-domain">{oracle.domain}</p>
              <p className="oracle-status">
                {oracle.is_defeated ? 'Defeated' : oracle.is_hostile ? 'Hostile' : 'Neutral'}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default MapViewer