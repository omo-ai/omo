import os
from enum import Enum
from cryptography.fernet import Fernet

# TODO move this to YAML

############################
######## Connectors ########
############################

# To add a new Connector:
# 1. Add a new name to the Connectors class
# 2. Add it to AVAILABLE_CONNECTORS

class Connector(Enum):
    GOOGLE_DRIVE = 'googledrive'
    ATLASSIAN = 'atlassian'
    NOTION = 'notion'

AVAILABLE_CONNECTORS = {
    Connector.ATLASSIAN.value: {
        'display_name': 'Atlassian',
    },
    Connector.GOOGLE_DRIVE.value: {
        'display_name': 'Google Drive',
    },
    Connector.NOTION.value: {
        'display_name': 'Notion',
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