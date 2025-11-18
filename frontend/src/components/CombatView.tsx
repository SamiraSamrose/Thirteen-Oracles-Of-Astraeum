### File: frontend/src/components/CombatView.tsx

/**
 * frontend/src/components/CombatView.tsx
 * STEP: Battle Visualization Component
 * Displays combat state and handles battle actions.
 */
import React, { useState, useEffect } from 'react'
import { useGameStore } from '../store'
import { oracleAPI } from '../services/api'
import './CombatView.css'

const CombatView: React.FC = () => {
  const { battleState, setBattleState, gameId, selectedOracle, setCurrentPhase, setNotification } = useGameStore()
  const [selectedAction, setSelectedAction] = useState<string>('attack')

  useEffect(() => {
    if (!battleState && selectedOracle) {
      startBattle()
    }
  }, [])

  const startBattle = async () => {
    try {
      const response = await oracleAPI.startBattle(gameId!, selectedOracle!.id)
      setBattleState(response.data.battle_state)
    } catch (error) {
      console.error('Failed to start battle:', error)
    }
  }

  const executeBattleAction = async () => {
    try {
      const response = await oracleAPI.executeBattleAction(
        gameId!,
        selectedOracle!.id,
        selectedAction
      )
      setBattleState(response.data)

      if (response.data.status === 'victory') {
        setNotification('Victory! Oracle defeated!')
        await oracleAPI.defeatOracle(gameId!, selectedOracle!.id)
        setTimeout(() => {
          setCurrentPhase('menu')
        }, 3000)
      } else if (response.data.status === 'defeat') {
        setNotification('Defeat! Your army has fallen...')
        setTimeout(() => {
          setCurrentPhase('menu')
        }, 3000)
      }
    } catch (error) {
      console.error('Battle action failed:', error)
    }
  }

  if (!battleState) {
    return <div className="combat-loading">Preparing battle...</div>
  }

  return (
    <div className="combat-view">
      <div className="combat-header">
        <h3>Battle vs {selectedOracle?.name}</h3>
        <p>Turn: {battleState.turn}</p>
      </div>

      <div className="combat-arena">
        <div className="combatant player-side">
          <h4>Your Army</h4>
          <div className="health-bar">
            <div 
              className="health-fill player" 
              style={{ width: `${Math.max(0, (battleState.player_health / 1000) * 100)}%` }}
            />
          </div>
          <p className="health-text">{battleState.player_health} HP</p>
        </div>

        <div className="combat-vs">VS</div>

        <div className="combatant enemy-side">
          <h4>Oracle Forces</h4>
          <div className="health-bar">
            <div 
              className="health-fill enemy" 
              style={{ width: `${Math.max(0, (battleState.enemy_health / 1000) * 100)}%` }}
            />
          </div>
          <p className="health-text">{battleState.enemy_health} HP</p>
        </div>
      </div>

      <div className="battle-log">
        <h4>Battle Log</h4>
        {battleState.battle_log.map((log, index) => (
          <p key={index}>{log}</p>
        ))}
      </div>

      {battleState.status === 'in_progress' && (
        <div className="combat-actions">
          <select 
            value={selectedAction} 
            onChange={(e) => setSelectedAction(e.target.value)}
            className="action-select"
          >
            <option value="attack">Attack</option>
            <option value="defend">Defend</option>
            <option value="special_ability">Special Ability</option>
          </select>
          <button onClick={executeBattleAction} className="action-btn">
            Execute Action
          </button>
        </div>
      )}
    </div>
  )
}

export default CombatView
