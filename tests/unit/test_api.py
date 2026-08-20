from fastapi.testclient import TestClient

from aegis.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "aegis"}


def test_api_status():
    response = client.get("/api/v1/status")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "aegis"


def test_root_and_documentation_are_available():
    assert client.get("/").status_code == 200
    assert client.get("/docs").status_code == 200
