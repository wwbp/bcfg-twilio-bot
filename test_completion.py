import pytest
import asyncio
from completion import generate_response


@pytest.mark.asyncio
async def test_generate_response():
    message = "Hello, world!"
    instructions = "This is a test"
    stateJSON = """
    {"version":1,"always_included_messages":[{"role":"system","content":"This is a test","name":null,"tool_call_id":null,"tool_calls":null,"is_tool_call_error":null}],"chat_history":[{"role":"user","content":"Hello, world!","name":null,"tool_call_id":null,"tool_calls":null,"is_tool_call_error":null},{"role":"assistant","content":"Hello! How can I assist you today?","name":null,"tool_call_id":null,"tool_calls":null,"is_tool_call_error":null}]}
    """
    response = await generate_response(stateJSON, instructions, message)
    print(response)
    assert isinstance(response, str)
