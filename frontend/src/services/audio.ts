### File: frontend/src/services/audio.ts

/**
 * frontend/src/services/audio.ts
 * STEP: Web Audio Service
 * Manages game audio, music, sound effects using Web Audio API.
 */
export class AudioService {
  private audioContext: AudioContext | null = null
  private soundBuffers: Map<string, AudioBuffer> = new Map()
  private musicSource: AudioBufferSourceNode | null = null
  private masterGain: GainNode | null = null

  initialize() {
    this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    this.masterGain = this.audioContext.createGain()
    this.masterGain.connect(this.audioContext.destination)
    this.masterGain.gain.value = 0.5
  }

  async loadSound(name: string, url: string) {
    if (!this.audioContext) this.initialize()

    try {
      const response = await fetch(url)
      const arrayBuffer = await response.arrayBuffer()
      const audioBuffer = await this.audioContext!.decodeAudioData(arrayBuffer)
      this.soundBuffers.set(name, audioBuffer)
    } catch (error) {
      console.error('Failed to load sound:', name, error)
    }
  }

  playSound(name: string, volume: number = 1.0) {
    const buffer = this.soundBuffers.get(name)
    if (!buffer || !this.audioContext) return

    const source = this.audioContext.createBufferSource()
    const gainNode = this.audioContext.createGain()
    
    source.buffer = buffer
    gainNode.gain.value = volume
    
    source.connect(gainNode)
    gainNode.connect(this.masterGain!)
    
    source.start(0)
  }

  playMusic(url: string, loop: boolean = true) {
    this.stopMusic()
    
    fetch(url)
      .then(response => response.arrayBuffer())
      .then(arrayBuffer => this.audioContext!.decodeAudioData(arrayBuffer))
      .then(audioBuffer => {
        this.musicSource = this.audioContext!.createBufferSource()
        this.musicSource.buffer = audioBuffer
        this.musicSource.loop = loop
        this.musicSource.connect(this.masterGain!)
        this.musicSource.start(0)
      })
      .catch(error => console.error('Music playback failed:', error))
  }

  stopMusic() {
    if (this.musicSource) {
      this.musicSource.stop()
      this.musicSource = null
    }
  }

  setVolume(volume: number) {
    if (this.masterGain) {
      this.masterGain.gain.value = Math.max(0, Math.min(1, volume))
    }
  }
}

export const audioService = new AudioService()