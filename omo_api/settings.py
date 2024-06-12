import os
import yaml
from cryptography.fernet import Fernet


############################
#### GENERAL SETTINGS ######
############################

ENV = os.environ.get('ENV', 'dev')

if ENV in ('production', 'prod'):
    CORS_ORIGINS = [
        "https://api.helloomo.ai",
        "https://app.helloomo.ai",
    ]

    OPENAPI_URL = None # don't publish docs publicly

else:
    CORS_ORIGINS = [
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    OPENAPI_URL = '/api/v1/openapi.json'