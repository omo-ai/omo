from enum import Enum

# these should align with the fields in TeamC object
# i.e. if X is listed here, then the user.Team object
# should have a X_configs field

class Connectors(Enum):
    GOOGLE_DRIVE = 'googledrive'
    ATLASSIAN = 'atlassian'


AVAILABLE_CONNECTORS = {
    Connectors.ATLASSIAN: {
        'display_name': 'Atlassian',
    },
    Connectors.GOOGLE_DRIVE: {
        'display_name': 'Google Drive',
    }
}

AVAILABLE_VECTOR_STORES = {
    'pinecone': {
        'display_name': 'Pinecone',
    }
}
ACTIVE_VECTOR_STORE = 'pinecone' # matches key above
