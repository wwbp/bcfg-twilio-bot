import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(module)s - %(message)s",
)

logger = logging.getLogger(__name__)


def verify_update_database(id: str, message):
    """
    Verify if the participant (or group) exists;
    create a record if not.
    """
    logger.info(f"Checking database for participant/group ID: {id}")

    # Simulate checking the database
    # TODO: Replace with real DB operation
    exists = False  # Placeholder for actual database query

    if exists:
        logger.info(f"Participant/group ID {id} exists. Updating records.")
    else:
        logger.warning(
            f"Participant/group ID {id} not found. Creating a new record. Recieved message: {message}")

    logger.debug(f"Received message for verification: {message}")

    # TODO: Implement actual DB update or creation logic


def load_chat_history_json(id: str):
    """
    Load chat history from the database.
    """
    logger.info(f"Loading chat history for participant/group ID: {id}")

    # Simulate loading chat history from the database
    dummy_test_output = [
        {'role': 'user',
         'content': 'hi, my name is max',
         'name': None,
         'tool_call_id': None,
         'tool_calls': None,
         'is_tool_call_error': None},
        {'role': 'assistant',
         'content': 'Hi Max! How can I assist you today?',
         'name': None,
         'tool_call_id': None,
         'tool_calls': [],
         'is_tool_call_error': None},
        {'role': 'user',
         'content': 'I like everything and nothing',
         'name': None,
         'tool_call_id': None,
         'tool_calls': None,
         'is_tool_call_error': None},
        {'role': 'assistant',
         'content': "That sounds like a unique perspective! It can be interesting to have a wide-ranging appreciation for many things while also feeling indifferent towards others. Is there a particular topic or area you're interested in discussing?",
         'name': None,
         'tool_call_id': None,
         'tool_calls': [],
         'is_tool_call_error': None},
        {'role': 'user',
         'content': 'football',
         'name': None,
         'tool_call_id': None,
         'tool_calls': None,
         'is_tool_call_error': None},
        {'role': 'assistant',
         'content': 'Great! Football is an exciting sport with a passionate following. Are you a fan of a specific team or league? Or is there a particular aspect of football you enjoy, like the strategies, players, or major events like the World Cup?',
         'name': None,
         'tool_call_id': None,
         'tool_calls': [],
         'is_tool_call_error': None}
    ]
    return dummy_test_output
