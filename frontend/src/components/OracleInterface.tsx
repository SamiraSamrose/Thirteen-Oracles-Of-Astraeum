### File: frontend/src/components/OracleInterface.tsx
/**
 * frontend/src/components/OracleInterface.tsx
 * STEP: Oracle Interaction Component
 * Handles puzzles, battles, and dialogue with oracles.
 */
import React from 'react'
import { useGameStore } from '../store'
import PuzzleRenderer from './PuzzleRenderer'
import CombatView from './CombatView'
import './OracleInterface.css'

const OracleInterface: React.FC = () => {
  const { selectedOracle, currentPhase, setCurrentPhase } = useGameStore()

  if (!selectedOracle) {
    return null
  }

  return (
    <div className="oracle-interface">
      <div className="oracle-header">
        <h2>{selectedOracle.title}</h2>
        <p>{selectedOracle.domain}</p>
      </div>

      <div className="oracle-content">
        {currentPhase === 'puzzle' && <PuzzleRenderer />}
        {currentPhase === 'battle' && <CombatView />}
        {currentPhase === 'confrontation' && (
          <div className="confrontation">
            <p>Final confrontation with {selectedOracle.name}...</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default OracleInterface