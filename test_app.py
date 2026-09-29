from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home_requires_login():
    response = client.post("/generate-home", json={
        "budget": 10000, "room_type": "Living Room",
        "style": "Modern", "items": "lights"
    })
    assert response.status_code == 401
