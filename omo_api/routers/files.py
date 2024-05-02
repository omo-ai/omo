import logging
from pydantic import BaseModel
from fastapi import APIRouter
from typing import List

logger = logging.getLogger(__name__) 

router = APIRouter()

class DriveObjectResponseModel(BaseModel):
    id: str # gdrive_id
    service_id: str
    name: str
    description: str
    type: str
    last_edited_utc: int 
    url: str
    size_bytes: int 

class DriveResponse(BaseModel):
    result: List[DriveObjectResponseModel]

# @router.get('/v1/files') 
# async def get_files(db: Session = Depends(get_db)):

#     logger.debug('get files')
#     results = db.query(GDriveObject).all()
#     #result = db.execute(stmt)
#     #results = result.fetchall()
#     logger.debug(results)

#     # TODO is there an way to automatically do this mapping?
#     data = []
#     for r in results:
#         obj = {
#             'id': r.gdrive_id,
#             'serviceId': r.service_id,
#             'name': r.name,
#             'description': r.description,
#             'type': r.type,
#             'lastEditedUtc': r.last_edited_utc,
#             'url': r.url,
#             'sizeBytes': r.size_bytes,
#         }
#         data.append(obj)

#     logger.debug('returning files', data)
#     return data
