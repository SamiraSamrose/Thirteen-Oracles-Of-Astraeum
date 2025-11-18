### File: backend/tests/test_api.py

"""
backend/tests/test_api.py
STEP: API Endpoint Testing
Tests all REST endpoints for correct responses.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register():
    """Test player registration"""
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_create_game(auth_token):
    """Test game creation"""
    response = client.post(
        "/api/v1/game/create",
        # Start all services
echo "Starting all services..."
cd ../infrastructure
docker-compose up -d

echo ""
echo "=== Setup Complete! ==="
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo "Grafana: http://localhost:3001 (admin/admin)"
echo "MinIO Console: http://localhost:9001 (minioadmin/minioadmin)"
echo ""
echo "Run 'docker-compose logs -f' to view logs"
