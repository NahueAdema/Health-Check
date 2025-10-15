from fastapi.testclient import TestClient
from main import create_app

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

def test_get_responses_without_token():
    response = client.get("/get-responses")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing token"

def test_get_responses_with_valid_token():
    # Simulamos que el token "abc123" existe (gracias al mock en conftest.py)
    response = client.get("/get-responses", headers={"Authorization": "Bearer abc123"})
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "logs" in data