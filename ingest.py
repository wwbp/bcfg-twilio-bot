
from interface import IncomingMessage
from database import verify_update_database


async def ingest(id: str, message: IncomingMessage):
    # TODO: check and update database
    verify_update_database(id, message)

    # TODO: generate response send message to completion engine
    

    # TODO: background task: store response in database

    # TODO: background task: send response to BCFG

    pass
