### File: frontend/src/components/InventoryPanel.tsx

/**
 * frontend/src/components/InventoryPanel.tsx
 * STEP: Inventory Display Component
 * Shows weapons, items, armies, and resources.
 */
import React, { useEffect, useState } from 'react'
import { useGameStore } from '../store'
import { gameAPI } from '../services/api'
import './InventoryPanel.css'

const InventoryPanel: React.FC = () => {
  const { gameId, setShowInventory } = useGameStore()
  const [inventory, setInventory] = useState<any>(null)

  useEffect(() => {
    loadInventory()
  }, [])

  const loadInventory = async () => {
    try {
      const response = await gameAPI.getInventory(gameId!)
      setInventory(response.data)
    } catch (error) {
      console.error('Failed to load inventory:', error)
    }
  }

  if (!inventory) {
    return <div className="inventory-loading">Loading inventory...</div>
  }

  return (
    <div className="inventory-overlay" onClick={() => setShowInventory(false)}>
      <div className="inventory-panel" onClick={(e) => e.stopPropagation()}>
        <div className="inventory-header">
          <h2>Inventory</h2>
          <button onClick={() => setShowInventory(false)} className="close-btn">×</button>
        </div>

        <div className="inventory-content">
          <section className="inventory-section">
            <h3>Weapons</h3>
            <div className="item-list">
              {inventory.weapons.map((weapon: string, index: number) => (
                <div key={index} className="item-card weapon">
                  <span>{weapon}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="inventory-section">
            <h3>Special Items</h3>
            <div className="item-list">
              {inventory.special_items.length > 0 ? (
                inventory.special_items.map((item: string, index: number) => (
                  <div key={index} className="item-card special">
                    <span>{item}</span>
                  </div>
                ))
              ) : (
                <p className="empty-message">No special items yet</p>
              )}
            </div>
          </section>

          <section className="inventory-section">
            <h3>Potions</h3>
            <div className="item-list">
              {inventory.potions.map((potion: string, index: number) => (
                <div key={index} className="item-card potion">
                  <span>{potion}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="inventory-section">
            <h3>Army Units</h3>
            <div className="army-list">
              {inventory.armies.map((army: any, index: number) => (
                <div key={index} className="army-card">
                  <h4>{army.unit_name}</h4>
                  <p>Quantity: {army.quantity}</p>
                  <p>Health: {army.total_health}</p>
                  <p>Morale: {army.morale.toFixed(1)}</p>
                  <p>Level: {army.experience_level}</p>
                  <span className={`status ${army.is_deployed ? 'deployed' : 'reserve'}`}>
                    {army.is_deployed ? 'Deployed' : 'Reserve'}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

export default InventoryPanel
