from omo_api.settings import ACTIVE_VECTOR_STORE, AVAILABLE_VECTOR_STORES

def get_current_vector_store():
    if ACTIVE_VECTOR_STORE.value not in AVAILABLE_VECTOR_STORES.keys():
        raise RuntimeError("not a valid vector store")
    
    return ACTIVE_VECTOR_STORE.value