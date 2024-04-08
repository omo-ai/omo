from pydantic import BaseModel
from typing import List
from omo_api.models.user import UserContext

class Message(BaseModel):
    role: str
    content: str
    user_context: UserContext

# { messages: [{role, content}, {role, content}]}
class MessageHistoryPayload(BaseModel):
    messages: List[Message]


