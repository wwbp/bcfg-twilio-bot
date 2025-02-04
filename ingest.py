from interface import IncomingMessage, GroupIncomingMessage
from database import verify_update_database
from completion import generate_response
from fastapi import BackgroundTasks

from send import send_message_to_participant, send_message_to_participant_group


async def ingest(id: str, message: IncomingMessage, background_tasks: BackgroundTasks):
    # Verify or update the database (or create the user/assistant record)
    verify_update_database(id, message)

    # Correctly formatted instruction string using both name and school_name
    instructions = (
        f"Chat with {message.context.name} from {message.context.school_name}"
    )
    response = await generate_response("", instructions, message.message)

    background_tasks.add_task(send_message_to_participant, id, response)
    # In production, update the database and trigger the outgoing API call.
    print(f"Generated response for participant {id}: {response}")


async def ingest_group(
    id: str, message: GroupIncomingMessage, background_tasks: BackgroundTasks
):
    print(
        f"Group message received for group {id} from sender {message.sender_id}: {message.message}"
    )
    verify_update_database(id, message)  # Stubbed DB update for now

    # Create an instructions string that lists the participants.
    participant_names = ", ".join([p.name for p in message.context.participants])
    instructions = f"Group chat from {message.context.school_name} with participants: {participant_names}"
    response = await generate_response("", instructions, message.message)

    background_tasks.add_task(send_message_to_participant_group, id, response)
    print(f"Generated group response for group {id}: {response}")
