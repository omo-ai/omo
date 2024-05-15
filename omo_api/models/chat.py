from pydantic import BaseModel
from typing import List
from omo_api.models.user import UserContext

class Message(BaseModel):
    role: str
    content: str

class MessageUserContext(Message):
    user_context: UserContext

class ChatMessages(BaseModel):
    messages: List[Message]
    chat_id: str
