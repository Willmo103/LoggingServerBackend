# tests/test_auth.py
import json


def test_register_app(client):
    response = client.post("/register_app", json={"app_name": "test_app"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "api_key" in data
