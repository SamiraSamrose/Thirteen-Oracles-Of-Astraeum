### File: frontend/src/store/playerSlice.ts

/**
 * frontend/src/store/playerSlice.ts
 * STEP: Player State Slice
 * Manages player-specific state in Zustand store.
 */
import { StateCreator } from 'zustand'

export interface PlayerSlice {
  playerId: number | null
  username: string | null
  isAuthenticated: boolean
  
  setPlayerId: (id: number) => void
  setUsername: (name: string) => void
  setAuthenticated: (auth: boolean) => void
  logout: () => void
}

export const createPlayerSlice: StateCreator<PlayerSlice> = (set) => ({
  playerId: null,
  username: null,
  isAuthenticated: false,
  
  setPlayerId: (id) => set({ playerId: id }),
  setUsername: (name) => set({ username: name }),
  setAuthenticated: (auth) => set({ isAuthenticated: auth }),
  logout: () => {
    localStorage.removeItem('token')
    set({
      playerId: null,
      username: null,
      isAuthenticated: false
    })
  }
})