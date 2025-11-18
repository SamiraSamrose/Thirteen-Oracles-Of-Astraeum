### File: frontend/src/store/index.ts
/**
 * frontend/src/store/index.ts
 * STEP: Zustand State Management
 * Manages global application state for game, player, UI.
 */
import { create } from 'zustand'
import { GameState, Oracle, BattleState, PuzzleData } from '../types'

interface GameStore {
  // Player state
  playerId: number | null
  setPlayerId: (id: number) => void
  
  // Game state
  gameId: number | null
  setGameId: (id: number) => void
  gameState: GameState | null
  setGameState: (state: GameState) => void
  
  // Current interaction
  selectedOracle: Oracle | null
  setSelectedOracle: (oracle: Oracle | null) => void
  currentPhase: string
  setCurrentPhase: (phase: string) => void
  
  // Puzzle state
  currentPuzzle: PuzzleData | null
  setCurrentPuzzle: (puzzle: PuzzleData | null) => void
  
  // Battle state
  battleState: BattleState | null
  setBattleState: (state: BattleState | null) => void
  
  // UI state
  showInventory: boolean
  setShowInventory: (show: boolean) => void
  showMap: boolean
  setShowMap: (show: boolean) => void
  notification: string | null
  setNotification: (message: string | null) => void
}

export const useGameStore = create<GameStore>((set) => ({
  playerId: null,
  setPlayerId: (id) => set({ playerId: id }),
  
  gameId: null,
  setGameId: (id) => set({ gameId: id }),
  gameState: null,
  setGameState: (state) => set({ gameState: state }),
  
  selectedOracle: null,
  setSelectedOracle: (oracle) => set({ selectedOracle: oracle }),
  currentPhase: 'menu',
  setCurrentPhase: (phase) => set({ currentPhase: phase }),
  
  currentPuzzle: null,
  setCurrentPuzzle: (puzzle) => set({ currentPuzzle: puzzle }),
  
  battleState: null,
  setBattleState: (state) => set({ battleState: state }),
  
  showInventory: false,
  setShowInventory: (show) => set({ showInventory: show }),
  showMap: false,
  setShowMap: (show) => set({ showMap: show }),
  notification: null,
  setNotification: (message) => set({ notification: message }),
}))
