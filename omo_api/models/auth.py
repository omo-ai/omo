from pydantic import BaseModel
from typing import Dict, Any, Optional
from pydantic import BaseModel

class OAuthProxyHeaders(BaseModel):
    content_type: str
    authorization: Optional[str] = None
    x_connector: Optional[str] = None

class OAuthProxyRequest(BaseModel):
    endpoint: str
    body: Optional[str] = None
    headers: OAuthProxyHeaders
