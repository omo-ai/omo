from pydantic import BaseModel
from typing import List, Optional
from omo_api.models.user import UserContext

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class MessageUserContext(Message):
    user_context: UserContext

class ChatPayload(BaseModel):
    chat_id: str
    messages: List[Message]