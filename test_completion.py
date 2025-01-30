import pytest
import asyncio
from completion import generate_response


@pytest.mark.asyncio
async def test_generate_response():
    data = "Hello, world!"
    response = await generate_response(data)
    print(response)
    assert isinstance(response, str)
