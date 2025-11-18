# THIRTEEN ORACLES OF ASTRAEUM - An Adventure Against 13 Autonomous Mythic Machine-Lords

A Web-Based Puzzle–Strategy–Narrative–Adventure Game featuring 13-agent orchestration with hybrid LLM agentic integration and AI architecture

## Comprehensive Project Description

Thirteen Oracles of Astraeum is a production-ready AI-powered strategy game implementing event-driven microservices architecture with intelligent agent coordination. The system deploys 13 isolated oracle agents, each executing unique behavioral patterns through local LLM inference (Llama 3/Mistral via Ollama), coordinated by a LangGraph orchestrator.

## Links

- **Live Site Demo**: https://samirasamrose.github.io/Thirteen-Oracles-Of-Astraeum/
- **Source Code**: https://github.com/SamiraSamrose/Thirteen-Oracles-Of-Astraeum
- **Video Demo**: https://youtu.be/SKlXMBoyx-8

## Tech Stack

- Languages: Python 3.11, TypeScript, JavaScript, SQL, YAML, JSON, Bash
- Backend Frameworks: FastAPI, SQLAlchemy, Alembic, Pydantic, AsyncIO
- Frontend Frameworks: React 18, Vite, Zustand
- Databases: PostgreSQL 15, Redis 7, Weaviate
- Message Queue: Apache Kafka, Zookeeper
- Storage: MinIO (S3-compatible)
- AI/ML: Ollama, vLLM, LangGraph, LangChain
- LLM Models: Llama 3, Mistral, DeepSeek, nomic-embed-text
- Agent Framework: LangGraph, Custom Agent Orchestrator
- Libraries: aiokafka, redis-py, psycopg2, boto3, minio, weaviate-client, httpx, jose, passlib, jsonschema, prometheus-client
- Frontend Libraries: Three.js, @react-three/fiber, @react-three/drei, axios, lucide-react
- WebSocket: Native WebSocket API, FastAPI WebSocket
- Authentication: JWT (JSON Web Tokens), bcrypt
- Monitoring: Prometheus, Grafana, Sentry
- Containerization: Docker, Docker Compose
- Orchestration: Kubernetes
- Reverse Proxy: NGINX, Caddy
- Testing: pytest, FastAPI TestClient
- DevOps Tools: Alembic (migrations), Git, GitHub Actions
- APIs: REST API, WebSocket API, Ollama API, MinIO API
- Data Integrations: Kafka event streams, Redis pub/sub, PostgreSQL ACID transactions, Vector embeddings via Weaviate
- Datasets: Player session data, Oracle configurations (YAML), Puzzle schemas (JSON), Army unit definitions, Game state snapshots, Agent memory vectors, Conversation histories


## Technical Implementation:

The backend utilizes FastAPI for asynchronous request handling, PostgreSQL for ACID-compliant state persistence, Redis for sub-millisecond cache access and pub/sub messaging, and Kafka for reliable event streaming between services. Each oracle agent maintains episodic memory in Weaviate vector database, enabling semantic retrieval of past interactions for contextual decision-making. WebSocket connections provide real-time state synchronization with React frontend rendering 3D dominion visualizations via Three.js.

## Agent Architecture:

Agents operate as independent processes subscribing to game events through Redis channels. The orchestrator routes events based on game state, validates agent outputs against JSON schemas, and prevents invalid state mutations. LLM calls include structured prompts combining agent personality configurations (YAML), current game context, and relevant memories retrieved through vector similarity search. Each agent implements domain-specific puzzle generation, tactical combat decisions, and diplomatic interactions, with outputs cached to reduce inference latency. 

List of 13 agents, 

- Oracle of Chronos- Time & Fate
- Oracle of Helios- Sun & Fire 
- Oracle of Nyx- Night & Shadows 
- Oracle of Boreas- Winter Storms 
- Oracle of Gaia- Earth & Growth 
- Oracle of Athenaia- Wisdom & Strategy
- Oracle of Aresion- War & Combat 
- Oracle of Themis- Law & Balance 
- Oracle of Proteus- Illusion & Transformation 
- Oracle of Echo- Sound & Voice 
- Oracle of Selene- Moon & Dreams  
- Oracle of DelphiX- Prophecy & Prediction 
- Oracle of Typhon- Chaos

## Data Flow:

Player actions trigger REST API endpoints that persist state changes to PostgreSQL, publish events to Kafka topics, and broadcast updates via WebSocket. Kafka consumers activate agent processing pipelines. Agents query vector memory, invoke LLM with validated prompts, and return decisions through orchestrator validation. Successful validations update game state and generate cascade events for multi-agent reactions. MinIO stores static assets accessed through presigned URLs.

## Scalability Features:

Stateless API design enables horizontal scaling behind load balancer. Database connection pooling and Redis caching minimize query overhead. Kafka partitioning distributes event processing. Kubernetes manifests provide container orchestration with resource limits. Prometheus scrapes metrics for auto-scaling triggers. Grafana dashboards visualize system health, agent performance, and LLM inference statistics.

## Readiness:

The system includes comprehensive error handling with Sentry integration, structured logging for debugging, Alembic database migrations, pytest test suite covering unit and integration scenarios, Docker Compose for development environments, and Kubernetes configurations for production deployment. Security implements JWT authentication, password hashing with bcrypt, SQL injection prevention through parameterized queries, and CORS configuration. Monitoring covers API latency, database connections, agent decision latency, and LLM inference duration.

## Features

- 13 AI-driven Oracle agents with unique personalities
- Real-time multiplayer support via WebSocket
- Local LLM integration (Llama 3, Mistral, DeepSeek)
- Vector memory for agent learning
- Event-driven architecture with Kafka
- Production monitoring with Prometheus/Grafana

## Core Features & Functionality

- Game Management:
Player authentication with JWT, game session creation, state persistence, save/load functionality, inventory management, resource tracking (gold, tokens, potions)

- 13 Oracle Agents:
Each oracle operates as isolated AI agent with personality-driven behavior, dynamic puzzle generation via LLM, tactical combat decisions, diplomatic interactions, memory-based learning, rule modification capabilities

- Puzzle System:
LLM-generated puzzles validated against JSON schemas, oracle-specific mechanics (time manipulation, deception, illusion, combat focus), difficulty scaling, hint system using insight tokens, solution validation.

This browser-based puzzle-strategy game implements a sequential challenge system where players defeat 13 AI-powered opponents through distinct puzzle mechanics. The architecture uses vanilla JavaScript for game logic, CSS Grid for responsive layouts, and Web Audio API for sound generation. Each Oracle presents a different puzzle type—Sudoku variants, bubble shooter mechanics, hidden object grids, sliding ice mazes, pattern formation, chess tactics, tactical combat grids, balance puzzles, match-3 with rotation, musical memory sequences, jigsaw pairing, word formation, and chaotic symbol matching. The difficulty system modifies puzzle complexity by adjusting grid dimensions, target requirements, time multipliers, and AI behavior intensity. AI agents implement oracle-specific behaviors including predictive move blocking, misinformation, dynamic rule changes, spatial element movement, and ring-based matrix transformations. The state management system tracks defeated oracles, accumulated resources, puzzle progress, and timer states in memory. Validation engines verify solutions against predefined answer matrices, exact move counts, and pattern matching algorithms. The reward system grants armies, weapons, insight tokens for hints, and time-extension potions upon oracle defeat. Progressive unlocking ensures sequential gameplay by activating the next oracle only after current defeat. Audio synthesis generates timer ticks using oscillators and plays musical note sequences through frequency-based sound generation. The project contains no external libraries, databases, or server-side components, operating entirely through client-side JavaScript execution within the browser environment.


- Combat Engine:
Deterministic turn-based calculations, army composition management, unit deployment, health/morale tracking, special abilities, victory/defeat conditions

- Multi-Agent Coordination:
Event-driven communication via Kafka, Redis pub/sub for real-time agent messaging, orchestrator mediates interactions, alliance formation between oracles, betrayal mechanics, collective strategy adaptation

- Learning System:
Vector memory stores agent experiences, player behavior pattern recognition, semantic search for relevant memories, adaptive difficulty based on performance, strategy evolution

- Real-Time Updates:
WebSocket connections for state synchronization, event broadcasting to game rooms, instant battle updates, oracle defeat notifications

- Asset Management:
MinIO storage for configurations, signed URLs for secure access, YAML-based agent personalities, JSON puzzle definitions

- Monitoring:
Prometheus metrics collection, Grafana dashboards, agent performance tracking, LLM inference latency, database connection pooling, error tracking via Sentry

## PROJECT ROOT FILES

### File: Thirteen-Oracles-Of-Astraeum/README.md
```markdown
# Thirteen Oracles of Astraeum

AI-powered strategy game where players navigate 13 floating dominions ruled by intelligent Oracle-Wizards powered by local LLMs.

## Quick Start

```bash
# Clone repository
git clone <repository-url>
cd Thirteen-Oracles-Of-Astraeum

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Start all services
docker-compose up -d

# Access game at http://localhost:3000
```

## Documentation

- [Setup Guide](SETUP.md)
- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Game Mechanics](docs/GAME_MECHANICS.md)

