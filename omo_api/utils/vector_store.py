
# these should align with the fields in TeamConfig object
# i.e. if X is listed here, then the user.TeamConfig object
# should have a X_configs field
AVAILABLE_VECTOR_STORES = [
    'pinecone'
]
AVAILABLE_APPS = [
    'atlassian',
    'googledrive',
]

ACTIVE_VECTOR_STORE = 'pinecone'

def get_current_vector_store():
    if ACTIVE_VECTOR_STORE not in AVAILABLE_VECTOR_STORES:
        raise RuntimeError("not a valid vector store")
    
    return ACTIVE_VECTOR_STORE