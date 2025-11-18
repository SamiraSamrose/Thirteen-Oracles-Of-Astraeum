### File: Thirteen-Oracles-Of-Astraeum/SETUP.md
```markdown
# Setup Guide

## Prerequisites

- Docker 24+ and Docker Compose 2+
- Python 3.11+
- Node.js 18+
- 16GB RAM minimum
- 50GB disk space

## Installation Steps

### 1. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

### 2. Database Setup

```bash
# Start PostgreSQL
docker-compose up -d postgres

# Run migrations
cd backend
alembic upgrade head

# Seed initial data
python scripts/seed_data.py
```

### 3. Start Infrastructure Services

```bash
# Start Redis, Kafka, MinIO, Weaviate
docker-compose up -d redis kafka minio weaviate
```

### 4. Start Ollama with Models

```bash
# Pull required models
docker-compose up -d ollama
docker exec -it ollama ollama pull llama3
docker exec -it ollama ollama pull mistral
```

### 5. Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 7. Access Application

- Game UI: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001
- MinIO Console: http://localhost:9001

## Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md)
