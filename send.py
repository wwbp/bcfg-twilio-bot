import httpx

# Placeholder for the BCFG domain – update this with the actual domain when available.
BCFG_DOMAIN = ""


async def send_message_to_participant(participant_id: str, message: str):
    """
    Sends a message to a single participant via the BCFG endpoint.

    Endpoint:
      POST /ai/api/participant/{id}/send
    Body:
      { "message": "What a lovely day" }
    """
    url = f"{BCFG_DOMAIN}/ai/api/participant/{participant_id}/send"
    payload = {"message": message}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        # This will raise an exception if the response status is 4xx or 5xx.
        response.raise_for_status()
        # You can process the response as needed. Here we simply return the JSON.
        return response.json()


async def send_message_to_participant_group(group_id: str, message: str):
    """
    Sends a message to a participant group via the BCFG endpoint.

    Endpoint:
      POST /ai/api/participantgroup/{id}/send
    Body:
      { "message": "What a lovely day" }
    """
    url = f"{BCFG_DOMAIN}/ai/api/participantgroup/{group_id}/send"
    payload = {"message": message}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
