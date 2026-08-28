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
    root = client.get("/")

    assert root.status_code == 200
    assert root.headers["content-type"].startswith("text/html")
    assert "AEGIS" in root.text
    assert client.get("/docs").status_code == 200


def test_web_console_assets_are_available():
    favicon = client.get("/favicon.ico")

    assert favicon.status_code == 200
    assert favicon.headers["content-type"].startswith("image/svg+xml")
    assert client.get("/static/app.css").status_code == 200
