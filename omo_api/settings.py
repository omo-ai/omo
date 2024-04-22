import os
from enum import Enum
from omo_api.conf.auth0 import AUTH0_CORS_IPS


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

AUTH_PROVIDER = 'auth0' # TODO support basic

if APP_ENV == 'production':
    CORS_ORIGINS = [
        "https://api.omo.bot",
        "https://app.helloomo.ai",
    ]

    if AUTH_PROVIDER == 'auth0':
        CORS_ORIGINS += AUTH0_CORS_IPS

    OPENAPI_URL = None # don't publish docs publicly

else:
    CORS_ORIGINS = [
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    OPENAPI_URL = '/api/v1/openapi.json'