import os
from enum import Enum
from cryptography.fernet import Fernet
from omo_api.utils import get_env_var



############################
######## Connectors ########
############################

# To add a new Connector:
# 1. Add a new name to the Connectors class
# 2. Add it to AVAILABLE_CONNECTORS

class Connector(Enum):
    GOOGLE_DRIVE = 'googledrive'
    ATLASSIAN = 'atlassian'

AVAILABLE_CONNECTORS = {
    Connector.ATLASSIAN.value: {
        'display_name': 'Atlassian',
    },
    Connector.GOOGLE_DRIVE.value: {
        'display_name': 'Google Drive',
    }
}

############################
###### Vector Stores #######
############################

# Only Pinecone is supported currently

class VectorStores(Enum):
    PINECONE = 'pinecone'

AVAILABLE_VECTOR_STORES = {
    VectorStores.PINECONE.value: {
        'display_name': 'Pinecone',
    }
}
ACTIVE_VECTOR_STORE = VectorStores.PINECONE

############################
#### GENERAL SETTINGS ######
############################

APP_ENV = os.environ.get('APP_ENV', 'development')

if APP_ENV == 'production':
    CORS_ORIGINS = [
        "https://api.omo.bot",
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