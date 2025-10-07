from fastapi.testclient import TestClient
from main import create_app

# Crear app sin lifespan para tests
app = create_app(use_lifespan=False)
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "pong"
    assert "timestamp" in data