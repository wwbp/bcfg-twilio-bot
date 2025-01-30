from fastapi import FastAPI, BackgroundTasks, status
from pydantic import BaseModel

app = FastAPI()


class Context(BaseModel):
    school_name: str
    school_mascot: str
    initial_message: str
    week_number: int
    name: str


class IncomingMessage(BaseModel):
    context: Context
    message: str


async def process_data(message: IncomingMessage):
    print(f"Processing data: {message.message}")


@app.post("/api/participant/{id}/incoming", status_code=status.HTTP_202_ACCEPTED)
async def endpoint_individual(id: str, message: IncomingMessage, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_data, message)
    return {"message": "Data received"}
