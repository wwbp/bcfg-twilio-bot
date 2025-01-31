

from pydantic import BaseModel


class Context(BaseModel):
    school_name: str
    school_mascot: str
    initial_message: str
    week_number: int
    name: str


class IncomingMessage(BaseModel):
    context: Context
    message: str


