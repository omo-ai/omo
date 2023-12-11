from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Dict, List, Optional


class GoogleDriveObject(BaseModel):
    id: str             # The Google Drive file ID
    serviceId: str      # Which Google service e.g. docs, pres, spread
    name: str           # filename
    description: str    # file description
    type: str           # file type (folder, document)
    lastEditedUtc: int  # timestamp in milliseconds since epoch
    url: str            # url to file
    sizeBytes: int      # filesize

    class Config:
        orm_mode = True

class GoogleDriveObjects(BaseModel):
    files: List[GoogleDriveObject]