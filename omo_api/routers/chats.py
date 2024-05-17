import logging
from typing import Optional, List
from fastapi import Depends, APIRouter, HTTPException 
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.db.models import Chat
from omo_api.utils import get_current_active_user
from omo_api.models.chat import Message, ChatPayload
from omo_api.db.models import User

logger = logging.getLogger(__name__) 

router = APIRouter()

def get_chats_for_user(db: Session, user_id: str) -> Optional[Chat]:
    result = db.query(Chat).filter(Chat.user_id == user_id).order_by(desc(Chat.updated_at)).all()
    return result

@router.get("/v1/chats/{chat_id}")
async def get_chat_by_id(chat_id: str,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_active_user)):

    logger.debug('get chats', chat_id)
    chat = db.query(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == user.id).one_or_none()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat




@router.put('/v1/chats/{chat_id}')
async def put_chat(payload: ChatPayload,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_active_user)):
    
    chat_kwargs = {
        'user_id': user.id,
        'chat_id': payload.chat_id,
    }

    messages = jsonable_encoder(payload.messages)
    defaults = {
        'messages': messages,
    }
    chat, created = get_or_create(db, Chat, defaults=defaults, **chat_kwargs)

    if created:
        # todo use OpenAI to summarize the title
        chat.title = payload.messages[0].content
        db.commit()
    else:
        chat.messages = messages
        db.commit()

    return chat

@router.get("/v1/chats/")
async def get_user_chats(user: User = Depends(get_current_active_user),
                         db: Session = Depends(get_db)):

    chat = get_chats_for_user(db, user.id)
    return chat