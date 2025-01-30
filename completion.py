import os
from kani import Kani
from kani.engines.openai import OpenAIEngine


api_key = os.getenv(
    "OPENAI_API_KEY", "abc")


async def _generate_response(engine, state, instructions, data):
    # idempotent function to generate response
    engine = OpenAIEngine(api_key, model="gpt-4o-mini")
    assistant = Kani(engine, system_prompt=instructions)
    if os.path.exists(state):
        assistant.load(state)
    response = await assistant.chat_round_str(data)
    assistant.save(state)
    return response


async def generate_response(data):
    state = "kani_state.json"
    instructions = "Complete the following sentence: "
    engine = OpenAIEngine(api_key, model="gpt-4o-mini")
    response = await _generate_response(engine, state, instructions, data)
    return response
