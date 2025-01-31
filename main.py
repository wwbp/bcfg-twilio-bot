from fastapi import FastAPI, BackgroundTasks, status
from ingest import IncomingMessage, ingest

app = FastAPI()


@app.post("/api/participant/{id}/incoming", status_code=status.HTTP_202_ACCEPTED)
async def endpoint_individual(id: str, message: IncomingMessage, background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest, id, message)
    return {"message": "Data received"}
