import logging
from omo_api.config import config
from omo_api.utils.vector_store import get_active_vector_store

logger = logging.getLogger(__name__)

def test_get_active_vector_store():
    # Test case 1: Active vector store exists
    config['vector_stores'] = [
        {'name': 'store1', 'display_name': 'Store 1', 'active': False},
        {'name': 'store2', 'display_name': 'Store 2', 'active': True},
        {'name': 'store3', 'display_name': 'Store 3', 'active': False},
    ]
    active_store = get_active_vector_store()
    assert active_store == {'name': 'store2', 'display_name': 'Store 2'}

    # Test case 2: No active vector store
    config['vector_stores'] = [
        {'name': 'store1', 'display_name': 'Store 1', 'active': False},
        {'name': 'store2', 'display_name': 'Store 2', 'active': False},
        {'name': 'store3', 'display_name': 'Store 3', 'active': False},
    ]
    active_store = get_active_vector_store()
    assert active_store is None

    # Test case 3: Empty vector stores list
    config['vector_stores'] = []
    active_store = get_active_vector_store()
    assert active_store is None

    # Test case 4: Invalid config format
    config['vector_stores'] = None
    active_store = get_active_vector_store()
    assert active_store is None