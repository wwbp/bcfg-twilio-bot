from pydantic import BaseModel
from typing import List


class Context(BaseModel):
    school_name: str
    school_mascot: str
    initial_message: str
    week_number: int
    name: str


class IncomingMessage(BaseModel):
    context: Context
    message: str


class Participant(BaseModel):
    name: str
    id: str


class GroupContext(BaseModel):
    school_name: str
    school_mascot: str
    initial_message: str
    week_number: int
    participants: List[Participant]


class GroupIncomingMessage(BaseModel):
    context: GroupContext
    sender_id: str
    message: str
