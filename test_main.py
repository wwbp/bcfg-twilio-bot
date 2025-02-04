import pytest
import respx
import httpx
from fastapi.testclient import TestClient
from main import app
import send
import openai

send.BCFG_DOMAIN = "https://test-bcfg.com"

client = TestClient(app)


@respx.mock
def test_endpoint_individual():
    # Mock OpenAI API call with correct response structure
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "gpt-4",
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Hello! How can I assist you today?",
                        },
                        "finish_reason": "stop",
                    }
                ],
            },
        )
    )

    # Mock the outgoing HTTP request
    respx.post(f"https://test-bcfg.com/ai/api/participant/123/send").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    payload = {
        "context": {
            "school_name": "Acme University",
            "school_mascot": "wolverine",
            "initial_message": "Starting college is like [...]",
            "week_number": 4,
            "name": "James",
        },
        "message": "What a lovely day",
    }
    response = client.post("/api/participant/123/incoming", json=payload)

    assert response.status_code == 202
    assert response.json() == {"message": "Data received"}


@respx.mock
def test_endpoint_group():
    # Mock OpenAI API call with correct response structure
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "chatcmpl-456",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "gpt-4",
                "usage": {
                    "prompt_tokens": 15,
                    "completion_tokens": 7,
                    "total_tokens": 22,
                },
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Hi there! How can I help you today?",
                        },
                        "finish_reason": "stop",
                    }
                ],
            },
        )
    )

    # Mock the outgoing HTTP request
    respx.post(f"https://test-bcfg.com/ai/api/participantgroup/group123/send").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    payload = {
        "context": {
            "school_name": "Acme University",
            "school_mascot": "wolverine",
            "initial_message": "Starting college is like [...]",
            "week_number": 4,
            "participants": [{"name": "James", "id": "1"}, {"name": "Mary", "id": "2"}],
        },
        "sender_id": "2",
        "message": "Hi everyone",
    }
    response = client.post("/api/participantgroup/group123/incoming", json=payload)

    assert response.status_code == 202
    assert response.json() == {"message": "Data received"}
