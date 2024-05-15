from pydantic import BaseModel
from typing import List, Optional
from omo_api.models.user import UserContext

class Message(BaseModel):
    role: str
    content: str
    title: Optional[str] = None
    timestamp: Optional[str] = None

class MessageUserContext(Message):
    user_context: UserContext

class ChatMessages(BaseModel):
    messages: List[Message]
    chat_id: str
