### File: docs/ARCHITECTURE.md

# System Architecture

## Overview
Thirteen Oracles of Astraeum uses a modern microservices architecture with event-driven agent coordination.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  React Frontend (TypeScript)                                    │
│  - Three.js 3D Rendering                                        │
│  - WebSocket Client                                             │
│  - Zustand State Management                                     │
│  - Web Audio API                                                │
└────────────┬────────────────────────────────────────────────────┘
             │ HTTPS/WSS
┌────────────▼────────────────────────────────────────────────────┐
│                    API GATEWAY / NGINX                          │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼───────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                         │
├────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐          │
│  │   Auth      │  │    Game      │  │    Oracle     │          │
│  │  Service    │  │   Service    │  │   Service     │          │
│  └─────────────┘  └──────────────┘  └───────────────┘          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐          │
│  │   Combat    │  │   Puzzle     │  │   Storage     │          │
│  │  Service    │  │   Service    │  │   Service     │          │
│  └─────────────┘  └──────────────┘  └───────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │         WebSocket Connection Manager             │          │
│  └──────────────────────────────────────────────────┘          │
└─────┬────────────┬─────────────┬─────────────┬─────────────────┘
      │            │             │             │
┌─────▼─────┐ ┌───▼──────┐ ┌───▼───────┐ ┌──▼──────────┐
│PostgreSQL │ │  Redis   │ │   Kafka   │ │   MinIO     │
│ Database  │ │  Cache   │ │  Events   │ │  Storage    │
│           │ │ Pub/Sub  │ │           │ │             │
└───────────┘ └────┬─────┘ └─────┬─────┘ └─────────────┘
                   │             │
┌──────────────────▼─────────────▼────────────────────────────────┐
│              AGENT ORCHESTRATOR (LangGraph)                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌────-──┐ ┌──────┐ ┌─────-─┐ ┌-──────┐ ┌─--─────┐ ┌──────┐     │
│  │Chronos│ │ Nyx  │ │Proteus│ │Aresion│ │Athenaia│ │Helios│     │
│  └─────-─┘ └──────┘ └──────-┘ └─-─────┘ └-──-────┘ └──────┘     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌────-──┐         │
│  │Boreas│ │ Gaia │ │Themis│ │ Echo │ │Selene│ │DelphiX│         │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └─────-─┘         │
│  ┌──────┐                                                       │
│  │Typhon│                                                       │
│  └──────┘                                                       │
└─────┬──────────────────┬────────────────────────────────────────┘
      │                  │
┌─────▼───────┐    ┌────▼────────┐
│   Ollama    │    │  Weaviate   │
│   vLLM      │    │   Vector    │
│ (Llama3,    │    │   Memory    │
│  Mistral)   │    │             │
└─────────────┘    └─────────────┘
      │
┌─────▼─────────────────────────────┐
│  Prometheus + Grafana Monitoring  │
└───────────────────────────────────┘

```

## Component Responsibilities

### Frontend (React + TypeScript)
- **Purpose**: User interface, 3D visualization, real-time updates
- **Technologies**: React 18, Three.js, WebSocket, Zustand
- **Responsibilities**:
  - Render game board and oracle selection
  - Display puzzles and battles
  - Manage player inventory
  - Real-time state synchronization via WebSocket

### Backend API (FastAPI)
- **Purpose**: RESTful API, business logic, authentication
- **Technologies**: Python 3.11, FastAPI, SQLAlchemy
- **Responsibilities**:
  - JWT authentication and session management
  - Game state CRUD operations
  - Oracle interaction coordination
  - WebSocket connection management
  - Event publishing to Kafka

### PostgreSQL Database
- **Purpose**: Persistent data storage
- **Schema**:
  - players, player_sessions
  - oracles, oracle_states
  - game_states, dominion_states
  - army_units, player_armies

### Redis Cache
- **Purpose**: Fast state access, pub/sub messaging
- **Usage**:
  - Cache frequently accessed game state
  - Pub/sub for agent communication
  - Rate limiting

### Kafka Event Stream
- **Purpose**: Event-driven architecture
- **Topics**:
  - game-events: Player actions, state changes
  - agent-actions: Oracle decisions, rule modifications

### Agent Orchestrator (LangGraph)
- **Purpose**: Coordinate 13 oracle agents
- **Responsibilities**:
  - Route events to appropriate agents
  - Manage agent lifecycle
  - Handle multi-agent interactions
  - Validate agent outputs

### LLM Inference (Ollama/vLLM)
- **Purpose**: Local LLM serving
- **Models**: Llama 3, Mistral, DeepSeek
- **Usage**:
  - Generate oracle dialogue
  - Create dynamic puzzles
  - Make tactical decisions

### Vector Memory (Weaviate)
- **Purpose**: Agent memory and learning
- **Storage**:
  - Agent memories and experiences
  - Player behavior patterns
  - Semantic search for context retrieval

### MinIO Object Storage
- **Purpose**: Asset storage (S3-compatible)
- **Contents**:
  - Audio files
  - 3D models
  - Configuration YAMLs
  - Generated puzzles

## Data Flow

### Game Creation Flow
1. Player registers/logs in → JWT issued
2. POST /game/create → FastAPI creates GameState
3. Initialize 13 OracleStates and DominionStates
4. Seed starting resources and army
5. Return game_id to frontend
6. Frontend establishes WebSocket connection

### Oracle Challenge Flow
1. Player selects oracle → POST /oracle/challenge
2. Backend updates oracle_state.current_phase = "puzzle"
3. Publish event to Kafka
4. Orchestrator routes to specific oracle agent
5. Agent generates puzzle via LLM
6. Puzzle validated and stored
7. Returned to player via WebSocket
8. Player submits solution
9. Validation → move to battle phase

### Battle Flow
1. POST /battle/start → Generate enemy army
2. Calculate combat stats
3. Store battle_state in oracle_state
4. Loop: Player action → Enemy counterattack
5. Check victory/defeat conditions
6. If victory → award rewards, mark oracle defeated
7. Broadcast result via WebSocket

## Scalability Considerations

### Horizontal Scaling
- Backend API: Stateless, can run multiple instances
- Agent workers: Each oracle agent can run in separate process
- Redis: Redis Cluster for high availability
- PostgreSQL: Read replicas for query load

### Performance Optimization
- Redis caching reduces database hits
- WebSocket for real-time updates (no polling)
- Async/await throughout Python code
- Database connection pooling
- LLM response caching

### Monitoring
- Prometheus metrics collection
- Grafana dashboards
- Sentry error tracking
- Application logs aggregation