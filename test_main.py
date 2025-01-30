import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_endpoint_individual():
    payload = {
        "context": {
            "school_name": "Acme University",
            "school_mascot": "wolverine",
            "initial_message": "Starting college is like [...]",
            "week_number": 4,
            "name": "James"
        },
        "message": "What a lovely day"
    }

    response = client.post("/api/participant/123/incoming", json=payload)

    assert response.status_code == 202
    assert response.json() == {"message": "Data received"}
