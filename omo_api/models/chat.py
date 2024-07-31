from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from omo_api.models.user import UserContext

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None
    chat_id: Optional[str] = None

class ChatPayload(BaseModel):
    chat_id: str
    messages: List[Message]

class ChatHistoryResponseModel(BaseModel):
    id: int
    chat_id: str
    title: str
    updated_at: datetime