from pydantic import BaseModel

class WebMessagePayload(BaseModel):
    question: str