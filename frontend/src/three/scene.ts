### File: frontend/src/three/scene.ts

/**
 * frontend/src/three/scene.ts
 * STEP: Three.js Scene Setup
 * Initializes 3D scene, camera, lighting for dominion visualization.
 */
import * as THREE from 'three'

export class GameScene {
  private scene: THREE.Scene
  private camera: THREE.PerspectiveCamera
  private renderer: THREE.WebGLRenderer
  private dominions: THREE.Group[] = []

  constructor(canvas: HTMLCanvasElement) {
    this.scene = new THREE.Scene()
    this.scene.background = new THREE.Color(0x0f0c29)
    
    this.camera = new THREE.PerspectiveCamera(
      75,
      canvas.width / canvas.height,
      0.1,
      1000
    )
    this.camera.position.z = 50
    this.camera.position.y = 30
    this.camera.lookAt(0, 0, 0)
    
    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true })
    this.renderer.setSize(canvas.width, canvas.height)
    
    this.setupLighting()
  }

  private setupLighting() {
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4)
    this.scene.add(ambientLight)
    
    const directionalLight = new THREE.DirectionalLight(0xffd700, 0.8)
    directionalLight.position.set(10, 20, 10)
    this.scene.add(directionalLight)
    
    const pointLight = new THREE.PointLight(0xffd700, 0.5)
    pointLight.position.set(0, 10, 0)
    this.scene.add(pointLight)
  }

  addDominion(position: THREE.Vector3, name: string) {
    const geometry = new THREE.SphereGeometry(3, 32, 32)
    const material = new THREE.MeshPhongMaterial({
      color: 0xffd700,
      emissive: 0x302b63,
      shininess: 30
    })
    
    const dominion = new THREE.Mesh(geometry, material)
    dominion.position.copy(position)
    
    const group = new THREE.Group()
    group.add(dominion)
    
    this.scene.add(group)
    this.dominions.push(group)
  }

  animate() {
    requestAnimationFrame(() => this.animate())
    
    this.dominions.forEach((dominion, index) => {
      dominion.rotation.y += 0.005
      dominion.position.y += Math.sin(Date.now() * 0.001 + index) * 0.01
    })
    
    this.renderer.render(this.scene, this.camera)
  }

  resize(width: number, height: number) {
    this.camera.aspect = width / height
    this.camera.updateProjectionMatrix()
    this.renderer.setSize(width, height)
  }
}