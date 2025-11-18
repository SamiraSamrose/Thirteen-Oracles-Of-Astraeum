### File: docs/API.md

# API Documentation

## Authentication Endpoints

### POST /api/v1/auth/register
Register new player account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "display_name": "string (optional)"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "player_id": 1,
  "username": "string"
}
```

### POST /api/v1/auth/login
Login and get JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** Same as register

### GET /api/v1/auth/me
Get current authenticated player info.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "display_name": "string",
  "total_games": 0,
  "games_won": 0,
  "oracles_defeated": 0
}
```

## Game Management Endpoints

### POST /api/v1/game/create
Create new game session.

**Request Body:**
```json
{
  "difficulty": "normal"
}
```

**Response:**
```json
{
  "game_id": 1,
  "message": "Game created successfully",
  "starting_resources": {
    "weapons": ["Mortal Spear"],
    "gold": 100,
    "insight_tokens": 1
  }
}
```

### GET /api/v1/game/{game_id}
Get complete game state.

**Response:**
```json
{
  "game_id": 1,
  "current_stage": 1,
  "oracles_defeated": 0,
  "resources": {
    "gold": 100,
    "insight_tokens": 1,
    "healing_draughts": 1
  },
  "inventory": {
    "weapons": ["Mortal Spear"],
    "special_items": [],
    "potions": ["Basic Healing Draught"]
  },
  "is_completed": false,
  "oracles": [...],
  "dominions": [...]
}
```

### POST /api/v1/game/{game_id}/save
Save game progress.

### GET /api/v1/game/{game_id}/inventory
Get player inventory and armies.

### POST /api/v1/game/{game_id}/insight
Use insight token for hint.

**Request Body:**
```json
{
  "question": "string"
}
```

## Oracle Interaction Endpoints

### POST /api/v1/oracle/challenge
Challenge an oracle.

**Query Parameters:**
- game_id: integer

**Request Body:**
```json
{
  "oracle_name": "Chronos"
}
```

### POST /api/v1/oracle/{game_id}/puzzle/solve
Submit puzzle solution.

**Request Body:**
```json
{
  "oracle_state_id": 1,
  "solution": "string"
}
```

### POST /api/v1/oracle/{game_id}/battle/start
Start battle with oracle.

**Query Parameters:**
- oracle_id: integer

### POST /api/v1/oracle/{game_id}/battle/action
Execute combat turn.

**Query Parameters:**
- oracle_id: integer

**Request Body:**
```json
{
  "action": "attack"
}
```

### POST /api/v1/oracle/{game_id}/defeat/{oracle_id}
Mark oracle as defeated and receive rewards.

## WebSocket Events

### Connection
```
ws://localhost:8000/ws/{game_id}/{player_id}
```

### Message Types

**Client to Server:**
```json
{
  "type": "ping",
  "data": {}
}
```

```json
{
  "type": "game_action",
  "data": {
    "action": "move",
    "target": "dominion_name"
  }
}
```

**Server to Client:**
```json
{
  "type": "player_action",
  "data": {
    "player_id": 1,
    "action": "string"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

```json
{
  "type": "oracle_defeated",
  "data": {
    "oracle_name": "Chronos",
    "rewards": {...}
  },
  "timestamp": "2024-01-01T00:00:00Z"
}