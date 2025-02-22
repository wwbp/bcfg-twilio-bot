from fastapi import FastAPI, BackgroundTasks, status
from ingest import ingest, ingest_group
from interface import IncomingMessage, GroupIncomingMessage

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}


@app.post("/api/participant/{id}/incoming", status_code=status.HTTP_202_ACCEPTED)
async def endpoint_individual(
    id: str, message: IncomingMessage, background_tasks: BackgroundTasks
):
    background_tasks.add_task(ingest, id, message, background_tasks)
    return {"message": "Data received"}


@app.post("/api/participantgroup/{id}/incoming", status_code=status.HTTP_202_ACCEPTED)
async def endpoint_group(
    id: str, message: GroupIncomingMessage, background_tasks: BackgroundTasks
):
    background_tasks.add_task(ingest_group, id, message, background_tasks)
    return {"message": "Data received"}
