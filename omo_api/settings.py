from enum import Enum


# To add a new Connector:
# 1. Add a new name to the Connectors class
# 2. Add it to AVAILABLE_CONNECTORS

############################
######## Connectors ########
############################

class Connector(Enum):
    GOOGLE_DRIVE = 'googledrive'
    ATLASSIAN = 'atlassian'

AVAILABLE_CONNECTORS = {
    Connector.ATLASSIAN: {
        'display_name': 'Atlassian',
    },
    Connector.GOOGLE_DRIVE: {
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
    VectorStores.PINECONE: {
        'display_name': 'Pinecone',
    }
}
ACTIVE_VECTOR_STORE = VectorStores.PINECONE
