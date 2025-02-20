from interface import IncomingMessage, GroupIncomingMessage
from database import verify_update_database, load_chat_history_json, save_chat_round
from completion import generate_response
from fastapi import BackgroundTasks

from send import send_message_to_participant, send_message_to_participant_group


async def ingest(id: str, data: IncomingMessage, background_tasks: BackgroundTasks):
    # Verify or update the database (or create the user/assistant record)
    verify_update_database(id, data)
    history_json = load_chat_history_json(id)

    # prompt pull
    instructions = (
        f"Chat with {data.context.name} from {data.context.school_name}"
    )

    response = await generate_response(history_json, instructions, data.message)

    background_tasks.add_task(save_chat_round, id, data.message, response)
    # background_tasks.add_task(send_message_to_participant, id, response)

    print(f"Generated response for participant {id}: {response}")

    return


async def ingest_group(
    id: str, message: GroupIncomingMessage, background_tasks: BackgroundTasks
):
    print(
        f"Group message received for group {id} from sender {message.sender_id}: {message.message}"
    )
    verify_update_database(id, message)  # Stubbed DB update for now

    # Create an instructions string that lists the participants.
    participant_names = ", ".join(
        [p.name for p in message.context.participants])
    instructions = f"Group chat from {message.context.school_name} with participants: {participant_names}"
    response = await generate_response("", instructions, message.message)

    background_tasks.add_task(send_message_to_participant_group, id, response)
    print(f"Generated group response for group {id}: {response}")
