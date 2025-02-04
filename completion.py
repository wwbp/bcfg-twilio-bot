import os
from kani import Kani
from kani.engines.openai import OpenAIEngine

api_key = os.getenv("OPENAI_API_KEY", "")


async def _generate_response(state, instructions, message):
    engine = OpenAIEngine(api_key, model="gpt-4o-mini")
    assistant = Kani(engine, system_prompt=instructions)
    if os.path.exists(state):
        assistant.load(state)
    response = await assistant.chat_round_str(message)
    assistant.save(state)
    return response


async def generate_response(stateJSON, instructions, message):
    state = "kani_state.json"
    if stateJSON:
        with open(state, "w") as f:
            f.write(stateJSON)
    response = await _generate_response(state, instructions, message)
    return response
