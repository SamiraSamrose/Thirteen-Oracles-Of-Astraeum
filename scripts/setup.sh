### File: scripts/setup.sh

#!/bin/bash

# STEP: Automated Setup Script
# Initializes project, installs dependencies, starts services

set -e

echo "=== Thirteen Oracles of Astraeum - Setup Script ==="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env with your configuration"
fi

# Start infrastructure services
echo "Starting infrastructure services..."
cd infrastructure
docker-compose up -d postgres redis kafka minio weaviate ollama

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Pull Ollama models
echo "Pulling LLM models..."
docker exec astraeum-ollama ollama pull llama3
docker exec astraeum-ollama ollama pull mistral

# Run database migrations
echo "Running database migrations..."
cd ../backend
docker-compose run --rm backend alembic upgrade head

# Seed database
echo "Seeding initial data..."
python scripts/seed_data.py

# Start all servicesexport interface Oracle {
  id: number
  name: string
  domain: string
  title: string
  description: string
  is_defeated: boolean
  is_hostile: boolean
  current_phase: string
}

export interface Dominion {
  name: string
  oracle_name: string
  is_controlled: boolean
  is_accessible: boolean
}

export interface ArmyUnit {
  unit_name: string
  quantity: number
  total_health: number
  morale: number
  experience_level: number
  is_deployed: boolean
}

export interface GameState {
  game_id: number
  current_stage: number
  oracles_defeated: number
  resources: {
    gold: number
    insight_tokens: number
    healing_draughts: number
  }
  inventory: {
    weapons: string[]
    special_items: string[]
    potions: string[]
  }
  is_completed: boolean
  oracles: Oracle[]
  dominions: Dominion[]
}

export interface PuzzleData {
  puzzle_type: string
  description: string
  solution?: string
  hints: string[]
  difficulty: number
}

export interface BattleState {
  turn: number
  player_health: number
  enemy_health: number
  status: string
  battle_log: string[]
}

export interface WebSocketMessage {
  type: string
  data: any
  timestamp?: string
}
