### File: frontend/src/components/ArmyPanel.tsx

/**
 * frontend/src/components/ArmyPanel.tsx
 * STEP: Army Management Component
 * Displays army composition, deployment options, unit details.
 */
import React from 'react'
import { useGameStore } from '../store'
import './ArmyPanel.css'

interface ArmyPanelProps {
  armies: any[]
}

const ArmyPanel: React.FC<ArmyPanelProps> = ({ armies }) => {
  const handleDeploy = (armyId: number) => {
    console.log('Deploy army:', armyId)
  }

  return (
    <div className="army-panel">
      <h3>Your Armies</h3>
      <div className="army-grid">
        {armies.map((army, index) => (
          <div key={index} className={`army-unit-card ${army.is_deployed ? 'deployed' : ''}`}>
            <div className="unit-header">
              <h4>{army.unit_name}</h4>
              <span className={`unit-status ${army.is_deployed ? 'active' : 'reserve'}`}>
                {army.is_deployed ? 'DEPLOYED' : 'RESERVE'}
              </span>
            </div>
            
            <div className="unit-stats">
              <div className="stat-row">
                <span>Quantity:</span>
                <span className="stat-value">{army.quantity}</span>
              </div>
              <div className="stat-row">
                <span>Health:</span>
                <span className="stat-value">{army.total_health}/{army.quantity * 100}</span>
              </div>
              <div className="stat-row">
                <span>Morale:</span>
                <div className="morale-bar">
                  <div 
                    className="morale-fill" 
                    style={{ width: `${army.morale * 100}%` }}
                  />
                </div>
              </div>
              <div className="stat-row">
                <span>Level:</span>
                <span className="stat-value">{army.experience_level}</span>
              </div>
            </div>
            
            {!army.is_deployed && (
              <button onClick={() => handleDeploy(index)} className="deploy-btn">
                Deploy
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ArmyPanel