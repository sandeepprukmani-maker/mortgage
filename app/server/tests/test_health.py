from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Valargen API"}


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_has_status_field():
    response = client.get("/health")
    data = response.json()
    assert "status" in data
