### File: scripts/deploy.sh

#!/bin/bash

# STEP: Production Deployment Script
# Builds and deploys to production environment

set -e

echo "=== Deploying Thirteen Oracles of Astraeum ==="

# Build images
echo "Building Docker images..."
docker-compose -f infrastructure/docker-compose.yml build

# Tag images for registry
REGISTRY="your-registry.com"
VERSION=$(git describe --tags --always)

docker tag astraeum-backend:latest $REGISTRY/astraeum-backend:$VERSION
docker tag astraeum-frontend:latest $REGISTRY/astraeum-frontend:$VERSION

# Push to registry
echo "Pushing to registry..."
docker push $REGISTRY/astraeum-backend:$VERSION
docker push $REGISTRY/astraeum-frontend:$VERSION

# Deploy to Kubernetes (if using K8s)
if command -v kubectl &> /dev/null; then
    echo "Deploying to Kubernetes..."
    kubectl apply -f infrastructure/kubernetes/
    kubectl set image deployment/backend backend=$REGISTRY/astraeum-backend:$VERSION
    kubectl set image deployment/frontend frontend=$REGISTRY/astraeum-frontend:$VERSION
else
    echo "Kubernetes not available, using Docker Compose..."
    docker-compose -f infrastructure/docker-compose.yml up -d
fi

echo "=== Deployment Complete ==="