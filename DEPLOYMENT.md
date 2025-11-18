## FINAL DOCUMENTATION FILES

### File: docs/DEPLOYMENT.md

# Deployment Guide

## Prerequisites
- Docker 24+ and Docker Compose 2+
- Kubernetes 1.28+ (optional)
- 16GB RAM minimum
- GPU recommended for LLM inference

## Development Deployment

```bash
# Clone repository
git clone <repository-url>
cd Thirteen-Oracles-Of-Astraeum

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Access application
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
# Grafana: http://localhost:3001
```

## Production Deployment

### Docker Compose (Simple)

```bash
# Build production images
docker-compose -f infrastructure/docker-compose.yml build

# Start services
docker-compose -f infrastructure/docker-compose.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Kubernetes (Advanced)

```bash
# Create namespace
kubectl create namespace astraeum

# Apply secrets
kubectl create secret generic postgres-secret \
  --from-literal=password=YOUR_PASSWORD \
  -n astraeum

# Deploy infrastructure
kubectl apply -f infrastructure/kubernetes/ -n astraeum

# Check deployment
kubectl get pods -n astraeum

# Access application
kubectl port-forward service/frontend-service 3000:80 -n astraeum
```

## Configuration

### Environment Variables
See `.env.example` for all configuration options.

Critical settings:
- `SECRET_KEY`: Change in production
- `JWT_SECRET`: Change in production
- `POSTGRES_PASSWORD`: Secure password
- `OLLAMA_BASE_URL`: LLM inference endpoint

### Database Migration

```bash
# Run migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"

# Rollback
alembic downgrade -1
```

### LLM Models

```bash
# Pull models
docker exec astraeum-ollama ollama pull llama3
docker exec astraeum-ollama ollama pull mistral

# List available models
docker exec astraeum-ollama ollama list
```

## Monitoring

### Prometheus
- Endpoint: http://localhost:9090
- Scrapes metrics from backend every 15s
- Configured in `infrastructure/monitoring/prometheus.yml`

### Grafana
- Endpoint: http://localhost:3001
- Default credentials: admin/admin
- Dashboards in `infrastructure/monitoring/grafana/dashboards/`

### Logs
```bash
# Backend logs
docker-compose logs -f backend

# All services
docker-compose logs -f

# Filter by level
docker-compose logs backend | grep ERROR
```

## Backup and Recovery

### Database Backup
```bash
# Manual backup
./scripts/backup.sh

# Automated backups (cron)
0 2 * * * /path/to/scripts/backup.sh
```

### Restore
```bash
# Restore from backup
gunzip backups/astraeum_backup_TIMESTAMP.sql.gz
docker exec -i astraeum-postgres psql -U astraeum astraeum_game < backups/astraeum_backup_TIMESTAMP.sql
```

## Scaling

### Horizontal Scaling
```bash
# Scale backend
docker-compose up -d --scale backend=3

# Kubernetes
kubectl scale deployment astraeum-backend --replicas=5 -n astraeum
```

### Resource Limits
Adjust in `docker-compose.yml` or Kubernetes manifests:
```yaml
resources:
  limits:
    memory: 2Gi
    cpu: 2000m
  requests:
    memory: 1Gi
    cpu: 1000m
```

## Security

### SSL/TLS
Use Let's Encrypt with Caddy or cert-manager for Kubernetes:

```bash
# Caddy configuration
tls your@email.com
```

### Firewall
```bash
# Allow only necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 5432/tcp  # PostgreSQL
ufw deny 6379/tcp  # Redis
```

### Secrets Management
Use Kubernetes secrets or external secret managers (Vault, AWS Secrets Manager)

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Database not ready: wait 30s and retry
# - Missing environment variables: check .env
# - Port conflicts: change API_PORT
```

### LLM inference fails
```bash
# Check Ollama status
docker exec astraeum-ollama ollama list

# Pull models if missing
docker exec astraeum-ollama ollama pull llama3

# Check memory usage (LLMs need 4GB+ RAM)
docker stats
```

### Database connection errors
```bash
# Check PostgreSQL status
docker exec astraeum-postgres pg_isready

# Test connection
docker exec astraeum-postgres psql -U astraeum -d astraeum_game -c "SELECT 1"
```

## Performance Tuning

### Database
```sql
-- Increase connection pool
ALTER SYSTEM SET max_connections = 200;

-- Enable query optimization
ALTER SYSTEM SET shared_buffers = '2GB';
```

### Redis
```bash
# Increase memory limit
docker-compose exec redis redis-cli CONFIG SET maxmemory 2gb
```

### LLM Inference
- Use GPU for 3-5x speedup
- Reduce `max_tokens` for faster responses
- Enable response caching