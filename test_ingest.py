import pytest
from fastapi import BackgroundTasks
from interface import IncomingMessage, GroupIncomingMessage, Context, Participant
import ingest  # This is your ingest module


@pytest.mark.asyncio
async def test_ingest_individual(monkeypatch):
    # Prepare a dummy incoming message for an individual.
    context = Context(
        school_name="Acme University",
        school_mascot="wolverine",
        initial_message="Starting college is like ...",
        week_number=4,
        name="James",
    )
    message_data = IncomingMessage(context=context, message="Hello")

    # Set a flag when verify_update_database is called.
    db_called = False

    def dummy_verify(id, message):
        nonlocal db_called
        db_called = True

    # Replace the imported verify_update_database in the ingest module.
    monkeypatch.setattr(ingest, "verify_update_database", dummy_verify)

    # Replace the generate_response function with a dummy async function.
    async def dummy_generate_response(state, instructions, message):
        return "dummy response"

    monkeypatch.setattr(ingest, "generate_response", dummy_generate_response)

    # Create a BackgroundTasks instance.
    background_tasks = BackgroundTasks()

    # Call ingest with the background_tasks parameter.
    await ingest.ingest("123", message_data, background_tasks)

    # Assert that the database function was called.
    assert db_called

    # Assert that a background task was added.
    # The .tasks property is a list of tasks added.
    assert len(background_tasks.tasks) == 1


@pytest.mark.asyncio
async def test_ingest_group(monkeypatch):
    # Prepare a dummy group incoming message.
    participants = [Participant(name="James", id="1"), Participant(name="Mary", id="2")]
    group_context = {
        "school_name": "Acme University",
        "school_mascot": "wolverine",
        "initial_message": "Starting college is like ...",
        "week_number": 4,
        # For this test, assume your GroupIncomingMessage context accepts a list of Participant objects.
        "participants": participants,
    }
    group_msg = GroupIncomingMessage(
        context=group_context, sender_id="2", message="Hi everyone"
    )

    db_called = False

    def dummy_verify(id, message):
        nonlocal db_called
        db_called = True

    monkeypatch.setattr(ingest, "verify_update_database", dummy_verify)

    async def dummy_generate_response(state, instructions, message):
        return "dummy group response"

    monkeypatch.setattr(ingest, "generate_response", dummy_generate_response)

    background_tasks = BackgroundTasks()

    await ingest.ingest_group("group123", group_msg, background_tasks)

    assert db_called
    assert len(background_tasks.tasks) == 1
