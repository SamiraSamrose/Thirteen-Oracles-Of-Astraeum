### File: frontend/src/index.tsx

/**
 * frontend/src/index.tsx
 * STEP: React Application Entry Point
 * Initializes React app and renders root component.
 */
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
