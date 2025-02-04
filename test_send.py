import send
import pytest
import respx
import httpx
import asyncio
from send import (
    send_message_to_participant,
    send_message_to_participant_group,
    BCFG_DOMAIN,
)

# For testing, we’ll override the BCFG_DOMAIN in send.py.
# You can do this by monkeypatching, or simply setting the variable here.
# Here we override it by direct assignment.
TEST_DOMAIN = "https://test-bcfg.com"
# Note: In your module, BCFG_DOMAIN is a module-level variable.
# For testing purposes, you can set it here.
# Alternatively, you could refactor your code to read from an environment variable.
send.BCFG_DOMAIN = TEST_DOMAIN


@respx.mock
@pytest.mark.asyncio
async def test_send_message_to_participant():
    participant_id = "123"
    message = "Test message"
    url = f"{TEST_DOMAIN}/ai/api/participant/{participant_id}/send"

    # Mock the POST endpoint to return a successful JSON response.
    route = respx.post(url).mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    response = await send_message_to_participant(participant_id, message)

    # Verify that the endpoint was called.
    assert route.called
    # Check that the response from our send function is as expected.
    assert response == {"status": "ok"}


@respx.mock
@pytest.mark.asyncio
async def test_send_message_to_participant_group():
    group_id = "group123"
    message = "Test group message"
    url = f"{TEST_DOMAIN}/ai/api/participantgroup/{group_id}/send"

    route = respx.post(url).mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    response = await send_message_to_participant_group(group_id, message)
    assert route.called
    assert response == {"status": "ok"}
