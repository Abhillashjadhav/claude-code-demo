import json
from src.app import app

def client():
    return app.test_client()

def test_health():
    c = client()
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_echo():
    c = client()
    payload = {"message": "hello"}
    resp = c.post("/echo", data=json.dumps(payload),
                  content_type="application/json")
    assert resp.status_code == 200
    assert resp.get_json()["received"] == payload
