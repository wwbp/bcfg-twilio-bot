import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BCFG_DOMAIN = os.getenv("BCFG_DOMAIN", "https://bcfg-domain.com")


async def send_message_to_participant(participant_id: str, message: str):
    """
    Logs a message instead of sending it to an external API.

    This function mimics sending a message and logs the details.
    """
    logger.info(
        f"[DEBUG] Simulated sending message to participant {participant_id}: {message}"
    )
    return {"status": "success", "participant_id": participant_id, "message": message}


async def send_message_to_participant_group(group_id: str, message: str):
    """
    Logs a group message instead of sending it to an external API.

    This function mimics sending a group message and logs the details.
    """
    logger.info(f"[DEBUG] Simulated sending message to group {group_id}: {message}")
    return {"status": "success", "group_id": group_id, "message": message}


# import httpx
# import os

# BCFG_DOMAIN = os.getenv("BCFG_DOMAIN", "https://bcfg-domain.com")


# async def send_message_to_participant(participant_id: str, message: str):
#     """
#     Sends a message to a single participant via the BCFG endpoint.

#     Endpoint:
#       POST /ai/api/participant/{id}/send
#     Body:
#       { "message": "What a lovely day" }
#     """
#     url = f"{BCFG_DOMAIN}/ai/api/participant/{participant_id}/send"
#     payload = {"message": message}

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=payload)
#         # This will raise an exception if the response status is 4xx or 5xx.
#         response.raise_for_status()
#         # You can process the response as needed. Here we simply return the JSON.
#         return response.json()


# async def send_message_to_participant_group(group_id: str, message: str):
#     """
#     Sends a message to a participant group via the BCFG endpoint.

#     Endpoint:
#       POST /ai/api/participantgroup/{id}/send
#     Body:
#       { "message": "What a lovely day" }
#     """
#     url = f"{BCFG_DOMAIN}/ai/api/participantgroup/{group_id}/send"
#     payload = {"message": message}

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=payload)
#         response.raise_for_status()
#         return response.json()
