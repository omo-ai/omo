import logging
import requests
from typing import Annotated
from fastapi import APIRouter, Header, HTTPException

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v1/notion/pages')
async def get_notion_pages(x_notion_authorization: Annotated[str, Header()]):
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
            "Notion-Version": "2022-06-28"  # Ensure you're using the correct version
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

    return response.json()
