### File: frontend/src/three/effects.ts

/**
 * frontend/src/three/effects.ts
 * STEP: Visual Effects
 * Particle systems, animations, special effects.
 */
import * as THREE from 'three'

export class ParticleEffect {
  private particles: THREE.Points
  private geometry: THREE.BufferGeometry
  private material: THREE.PointsMaterial

  constructor(count: number = 1000) {
    this.geometry = new THREE.BufferGeometry()
    const positions = new Float32Array(count * 3)
    
    for (let i = 0; i < count * 3; i++) {
      positions[i] = (Math.random() - 0.5) * 100
    }
    
    this.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    
    this.material = new THREE.PointsMaterial({
      color: 0xffd700,
      size: 0.5,
      transparent: true,
      opacity: 0.6
    })
    
    this.particles = new THREE.Points(this.geometry, this.material)
  }

  update() {
    const positions = this.geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < positions.length; i += 3) {
      positions[i + 1] -= 0.1
      
      if (positions[i + 1] < -50) {
        positions[i + 1] = 50
      }
    }
    
    this.geometry.attributes.position.needsUpdate = true
  }

  getObject(): THREE.Points {
    return this.particles
  }
}