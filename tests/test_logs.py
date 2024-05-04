# tests/test_logs.py
import json


def test_log_creation(client):
    response = client.post(
        "/log/test_app", json={"message": "Test log message"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Log entry added"


def test_get_logs(client):
    response = client.get("/logs/test_app")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["message"] == "Test log message"
