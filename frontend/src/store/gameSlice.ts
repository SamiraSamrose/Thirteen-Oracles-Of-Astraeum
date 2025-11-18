### File: frontend/src/store/gameSlice.ts

/**
 * frontend/src/store/gameSlice.ts
 * STEP: Game State Slice
 * Manages game-specific state in Zustand store.
 */
import { StateCreator } from 'zustand'
import { GameState, Oracle, BattleState } from '../types'

export interface GameSlice {
  gameId: number | null
  gameState: GameState | null
  selectedOracle: Oracle | null
  currentPhase: string
  battleState: BattleState | null
  
  setGameId: (id: number) => void
  setGameState: (state: GameState) => void
  setSelectedOracle: (oracle: Oracle | null) => void
  setCurrentPhase: (phase: string) => void
  setBattleState: (state: BattleState | null) => void
  resetGame: () => void
}

export const createGameSlice: StateCreator<GameSlice> = (set) => ({
  gameId: null,
  gameState: null,
  selectedOracle: null,
  currentPhase: 'menu',
  battleState: null,
  
  setGameId: (id) => set({ gameId: id }),
  setGameState: (state) => set({ gameState: state }),
  setSelectedOracle: (oracle) => set({ selectedOracle: oracle }),
  setCurrentPhase: (phase) => set({ currentPhase: phase }),
  setBattleState: (state) => set({ battleState: state }),
  resetGame: () => set({
    gameId: null,
    gameState: null,
    selectedOracle: null,
    currentPhase: 'menu',
    battleState: null
  })
})