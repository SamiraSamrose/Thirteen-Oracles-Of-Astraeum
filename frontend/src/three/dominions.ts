### File: frontend/src/three/dominions.ts

/**
 * frontend/src/three/dominions.ts
 * STEP: Dominion 3D Models
 * Creates floating island models for each dominion.
 */
import * as THREE from 'three'

export function createDominionIsland(theme: string): THREE.Group {
  const group = new THREE.Group()
  
  const baseGeometry = new THREE.CylinderGeometry(5, 3, 2, 32)
  const baseMaterial = new THREE.MeshPhongMaterial({
    color: getThemeColor(theme),
    flatShading: true
  })
  const base = new THREE.Mesh(baseGeometry, baseMaterial)
  group.add(base)
  
  const topGeometry = new THREE.SphereGeometry(4, 16, 16)
  const topMaterial = new THREE.MeshPhongMaterial({
    color: getThemeColor(theme),
    transparent: true,
    opacity: 0.8
  })
  const top = new THREE.Mesh(topGeometry, topMaterial)
  top.position.y = 2
  group.add(top)
  
  return group
}

function getThemeColor(theme: string): number {
  const colors: Record<string, number> = {
    'Time': 0x6366f1,
    'Darkness': 0x1e1b4b,
    'Illusion': 0x8b5cf6,
    'War': 0xef4444,
    'Wisdom': 0x3b82f6,
    'Fire': 0xf59e0b,
    'Ice': 0x06b6d4,
    'Earth': 0x22c55e,
    'Law': 0xeab308,
    'Sound': 0xec4899,
    'Moon': 0xa78bfa,
    'Prophecy': 0x8b5cf6,
    'Chaos': 0x7c3aed
  }
  return colors[theme] || 0xffd700
}