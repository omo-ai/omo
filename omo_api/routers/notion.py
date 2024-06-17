import logging
import requests
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, HTTPException
from omo_api.db.utils import get_db, get_or_create
from omo_api.workers.notion import tasks
from omo_api.db.models import User, NotionConfig

from omo_api.utils import get_current_active_user

logger = logging.getLogger(__name__) 

router = APIRouter()

def get_notion_context(user: User = Depends(get_current_active_user),
                       db: Session = Depends(get_db)):

    context, created = get_or_create(db, NotionConfig, team_id=user.team_id)

    return context 

    
@router.post('/v1/notion/pages')
async def get_notion_pages(x_notion_authorization: Annotated[str, Header()],
                           notion_context = Depends(get_notion_context),
                           db: Session = Depends(get_db)) -> dict:
    """
    Retrieves Notion pages based on the provided authorization token.

    Args:
        x_notion_authorization (str): The authorization token for accessing Notion API.

    Returns:
        dict: A dictionary containing the response from the Notion API.
    """



    response = requests.post(
        "https://api.notion.com/v1/search",
        headers={
            "Authorization": x_notion_authorization,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        },
        json={
            "query": "",  # An empty query will return all pages the user has access to
            "filter": {
                "value": "page",
                "property": "object"
            }
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    pages = response.json()

    if x_notion_authorization.startswith('Bearer '):
        x_notion_authorization = x_notion_authorization.replace('Bearer ', '')

    page_metadata = [
        (
            page['id'], 
            page['properties']['title']['title'][0]['plain_text'],
            page['created_time'],
            page['last_edited_time'], 
            page['url'], 
        ) for page in pages['results']
    ]

    task_payload = [(page, x_notion_authorization,) for page in page_metadata]

    notion_context.oauth_token = x_notion_authorization
    notion_context.pages = page_metadata
    db.add(notion_context)
    db.commit()

    chunk_size = 2

    task_result = tasks.sync_notion_pages.chunks(task_payload, chunk_size).apply_async()
    task_result.save()

    return response.json()
