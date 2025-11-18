# frontend/src/components/PuzzleRenderer.tsx
# STEP: Puzzle Display and Solution Component
# Renders puzzles and handles player solutions with validation.

import React, { useState, useEffect } from 'react'
import { useGameStore } from '../store'
import { oracleAPI } from '../services/api'
import './PuzzleRenderer.css'

interface PuzzleData {
  puzzle_type: string
  description: string
  solution?: string
  hints: string[]
  difficulty: number
  false_clues?: string[]
  time_limit?: number
}

const PuzzleRenderer: React.FC = () => {
  const { 
    currentPuzzle, 
    gameId, 
    selectedOracle, 
    setCurrentPhase, 
    setNotification 
  } = useGameStore()
  
  const [solution, setSolution] = useState('')
  const [showHint, setShowHint] = useState(false)
  const [currentHintIndex, setCurrentHintIndex] = useState(0)
  const [loading, setLoading] = useState(false)
  const [attempts, setAttempts] = useState(0)
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null)
  const [puzzleData, setPuzzleData] = useState<PuzzleData | null>(null)

  useEffect(() => {
    // Load puzzle data
    loadPuzzle()
  }, [selectedOracle])

  useEffect(() => {
    // Timer countdown
    if (timeRemaining !== null && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1)
      }, 1000)
      return () => clearTimeout(timer)
    } else if (timeRemaining === 0) {
      handleTimeout()
    }
  }, [timeRemaining])

  const loadPuzzle = async () => {
    if (!selectedOracle) return

    try {
      // In production, this would fetch from API
      const mockPuzzle: PuzzleData = {
        puzzle_type: 'logic',
        description: `Solve the ${selectedOracle.domain} puzzle to proceed. The oracle watches your every move.`,
        hints: [
          'Consider the fundamental pattern',
          'Look beyond the obvious solution',
          'The answer lies in simplicity'
        ],
        difficulty: 5,
        false_clues: selectedOracle.name === 'Nyx' ? [
          'The first path is always correct',
          'Trust your initial instinct'
        ] : undefined,
        time_limit: selectedOracle.name === 'Chronos' ? 180 : undefined
      }

      setPuzzleData(mockPuzzle)
      
      if (mockPuzzle.time_limit) {
        setTimeRemaining(mockPuzzle.time_limit)
      }
    } catch (error) {
      console.error('Failed to load puzzle:', error)
    }
  }

  const handleSubmitSolution = async () => {
    if (!solution.trim()) {
      setNotification('Please enter a solution')
      setTimeout(() => setNotification(null), 3000)
      return
    }

    setLoading(true)
    setAttempts(attempts + 1)

    try {
      const response = await oracleAPI.solvePuzzle(
        gameId!,
        selectedOracle!.id,
        solution
      )

      if (response.data.valid) {
        setNotification('Correct! The oracle acknowledges your wisdom.')
        setTimeout(() => {
          setCurrentPhase('battle')
          setNotification(null)
        }, 2000)
      } else {
        setNotification(`Incorrect solution. Attempts: ${attempts + 1}`)
        setSolution('')
        setTimeout(() => setNotification(null), 3000)
      }
    } catch (error) {
      console.error('Failed to submit solution:', error)
      setNotification('Error validating solution')
      setTimeout(() => setNotification(null), 3000)
    } finally {
      setLoading(false)
    }
  }

  const handleShowHint = () => {
    if (puzzleData && currentHintIndex < puzzleData.hints.length) {
      setShowHint(true)
      // Increment hint index for next time
      setTimeout(() => {
        setCurrentHintIndex(currentHintIndex + 1)
      }, 5000)
    }
  }

  const handleTimeout = () => {
    setNotification('Time expired! The oracle gains advantage.')
    setTimeout(() => {
      setCurrentPhase('battle')
      setNotification(null)
    }, 2000)
  }

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (!puzzleData) {
    return (
      <div className="puzzle-loading">
        <div className="spinner-border text-warning" role="status">
          <span className="visually-hidden">Loading puzzle...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="puzzle-renderer">
      <div className="puzzle-header">
        <h3>
          <i className="fas fa-puzzle-piece"></i> {selectedOracle?.name}'s Challenge
        </h3>
        {timeRemaining !== null && (
          <div className={`time-indicator ${timeRemaining < 60 ? 'time-critical' : ''}`}>
            <i className="fas fa-clock"></i> {formatTime(timeRemaining)}
          </div>
        )}
      </div>

      <div className="puzzle-description">
        <p>{puzzleData.description}</p>
        <div className="puzzle-meta">
          <span className="badge bg-secondary">Type: {puzzleData.puzzle_type}</span>
          <span className="badge bg-warning">Difficulty: {puzzleData.difficulty}/13</span>
          <span className="badge bg-info">Attempts: {attempts}</span>
        </div>
      </div>

      {puzzleData.false_clues && (
        <div className="false-clues-warning">
          <i className="fas fa-exclamation-triangle"></i>
          <span>Warning: Some information may be deceptive</span>
        </div>
      )}

      <div className="puzzle-input-area">
        <label htmlFor="solution-input" className="form-label">
          Your Solution:
        </label>
        <textarea
          id="solution-input"
          value={solution}
          onChange={(e) => setSolution(e.target.value)}
          placeholder="Enter your solution here..."
          rows={4}
          className="puzzle-input form-control"
          disabled={loading}
        />
      </div>

      <div className="puzzle-actions">
        <button 
          onClick={handleSubmitSolution} 
          disabled={loading || !solution.trim()} 
          className="btn btn-primary submit-btn"
        >
          {loading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status"></span>
              Validating...
            </>
          ) : (
            <>
              <i className="fas fa-check"></i> Submit Solution
            </>
          )}
        </button>
        
        <button 
          onClick={handleShowHint} 
          className="btn btn-outline-warning hint-btn"
          disabled={currentHintIndex >= puzzleData.hints.length}
        >
          <i className="fas fa-lightbulb"></i> 
          {showHint ? 'Show Next Hint' : 'Show Hint'} 
          ({puzzleData.hints.length - currentHintIndex} remaining)
        </button>
      </div>

      {showHint && currentHintIndex > 0 && (
        <div className="puzzle-hints">
          <h5>
            <i className="fas fa-info-circle"></i> Hints:
          </h5>
          {puzzleData.hints.slice(0, currentHintIndex).map((hint, index) => (
            <div key={index} className="hint-item">
              <span className="hint-number">{index + 1}.</span>
              <span className="hint-text">{hint}</span>
            </div>
          ))}
        </div>
      )}

      {puzzleData.false_clues && (
        <div className="false-clues-section">
          <h6 className="text-muted">
            <i className="fas fa-mask"></i> Suspicious Information:
          </h6>
          {puzzleData.false_clues.map((clue, index) => (
            <div key={index} className="false-clue-item">
              {clue}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default PuzzleRenderer
