# FILE 3: frontend/src/utils/validators.ts
# STEP: Frontend Validation Utilities
# Client-side validation for forms, inputs, and game state.

/**
 * frontend/src/utils/validators.ts
 * STEP: Client-Side Validation Functions
 * Validates user input, game state, and API responses.
 */

export interface ValidationResult {
  valid: boolean
  error?: string
}

/**
 * Validate username format
 * Requirements: 3-20 characters, alphanumeric and underscore only
 */
export const validateUsername = (username: string): ValidationResult => {
  if (!username || username.length < 3) {
    return { valid: false, error: 'Username must be at least 3 characters' }
  }
  
  if (username.length > 20) {
    return { valid: false, error: 'Username must not exceed 20 characters' }
  }
  
  const usernameRegex = /^[a-zA-Z0-9_]+$/
  if (!usernameRegex.test(username)) {
    return { valid: false, error: 'Username can only contain letters, numbers, and underscores' }
  }
  
  return { valid: true }
}

/**
 * Validate email format
 */
export const validateEmail = (email: string): ValidationResult => {
  if (!email) {
    return { valid: false, error: 'Email is required' }
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return { valid: false, error: 'Invalid email format' }
  }
  
  return { valid: true }
}

/**
 * Validate password strength
 * Requirements: Minimum 8 characters, at least one letter and one number
 */
export const validatePassword = (password: string): ValidationResult => {
  if (!password || password.length < 8) {
    return { valid: false, error: 'Password must be at least 8 characters' }
  }
  
  if (password.length > 100) {
    return { valid: false, error: 'Password is too long' }
  }
  
  const hasLetter = /[a-zA-Z]/.test(password)
  const hasNumber = /[0-9]/.test(password)
  
  if (!hasLetter || !hasNumber) {
    return { valid: false, error: 'Password must contain both letters and numbers' }
  }
  
  return { valid: true }
}

/**
 * Validate puzzle solution input
 */
export const validatePuzzleSolution = (solution: string): ValidationResult => {
  if (!solution || solution.trim().length === 0) {
    return { valid: false, error: 'Solution cannot be empty' }
  }
  
  if (solution.length > 500) {
    return { valid: false, error: 'Solution is too long (max 500 characters)' }
  }
  
  return { valid: true }
}

/**
 * Validate game difficulty selection
 */
export const validateDifficulty = (difficulty: string): ValidationResult => {
  const validDifficulties = ['easy', 'normal', 'hard']
  
  if (!validDifficulties.includes(difficulty)) {
    return { valid: false, error: 'Invalid difficulty level' }
  }
  
  return { valid: true }
}

/**
 * Validate oracle selection
 */
export const validateOracleSelection = (oracleId: number, availableOracles: any[]): ValidationResult => {
  if (!oracleId || oracleId < 1) {
    return { valid: false, error: 'Invalid oracle selection' }
  }
  
  const oracle = availableOracles.find(o => o.id === oracleId)
  if (!oracle) {
    return { valid: false, error: 'Oracle not found' }
  }
  
  if (oracle.is_defeated) {
    return { valid: false, error: 'This oracle has already been defeated' }
  }
  
  return { valid: true }
}

/**
 * Validate JWT token format
 */
export const validateToken = (token: string): ValidationResult => {
  if (!token) {
    return { valid: false, error: 'Token is missing' }
  }
  
  const parts = token.split('.')
  if (parts.length !== 3) {
    return { valid: false, error: 'Invalid token format' }
  }
  
  return { valid: true }
}

/**
 * Validate game state object structure
 */
export const validateGameState = (gameState: any): ValidationResult => {
  if (!gameState) {
    return { valid: false, error: 'Game state is null' }
  }
  
  const requiredFields = ['game_id', 'current_stage', 'oracles_defeated', 'resources']
  
  for (const field of requiredFields) {
    if (!(field in gameState)) {
      return { valid: false, error: `Missing required field: ${field}` }
    }
  }
  
  if (gameState.current_stage < 1 || gameState.current_stage > 13) {
    return { valid: false, error: 'Invalid game stage' }
  }
  
  return { valid: true }
}

/**
 * Sanitize user input to prevent XSS
 */
export const sanitizeInput = (input: string): string => {
  return input
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
    .trim()
}

/**
 * Validate numeric input within range
 */
export const validateNumberInRange = (
  value: number, 
  min: number, 
  max: number, 
  fieldName: string
): ValidationResult => {
  if (isNaN(value)) {
    return { valid: false, error: `${fieldName} must be a number` }
  }
  
  if (value < min || value > max) {
    return { valid: false, error: `${fieldName} must be between ${min} and ${max}` }
  }
  
  return { valid: true }
}

/**
 * Validate array has minimum length
 */
export const validateArrayLength = (
  array: any[], 
  minLength: number, 
  fieldName: string
): ValidationResult => {
  if (!Array.isArray(array)) {
    return { valid: false, error: `${fieldName} must be an array` }
  }
  
  if (array.length < minLength) {
    return { valid: false, error: `${fieldName} must have at least ${minLength} items` }
  }
  
  return { valid: true }
}

/**
 * Validate WebSocket message format
 */
export const validateWebSocketMessage = (message: any): ValidationResult => {
  if (!message || typeof message !== 'object') {
    return { valid: false, error: 'Invalid message format' }
  }
  
  if (!message.type) {
    return { valid: false, error: 'Message type is required' }
  }
  
  return { valid: true }
}

/**
 * Validate battle action
 */
export const validateBattleAction = (action: string): ValidationResult => {
  const validActions = ['attack', 'defend', 'special_ability', 'tactical_retreat']
  
  if (!validActions.includes(action)) {
    return { valid: false, error: 'Invalid battle action' }
  }
  
  return { valid: true }
}

/**
 * Comprehensive form validation helper
 */
export const validateForm = (
  formData: Record<string, any>, 
  validationRules: Record<string, (value: any) => ValidationResult>
): { valid: boolean; errors: Record<string, string> } => {
  const errors: Record<string, string> = {}
  
  for (const [field, validator] of Object.entries(validationRules)) {
    const result = validator(formData[field])
    if (!result.valid && result.error) {
      errors[field] = result.error
    }
  }
  
  return {
    valid: Object.keys(errors).length === 0,
    errors
  }
}
