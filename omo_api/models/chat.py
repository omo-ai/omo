from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

# { messages: [{role, content}, {role, content}]}
class MessageHistoryPayload(BaseModel):
    messages: List[Message]


