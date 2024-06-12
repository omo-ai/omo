import logging
from typing import Optional, Dict
from omo_api.config import config

logger = logging.getLogger(__name__)

def get_active_vector_store() -> Optional[Dict]:
    """
    Retrieves the active vector store from the configuration file.

    Returns:
        dict or None: A dictionary containing the name and display name of the active vector store,
                      or None if the active vector store could not be found.
    """
    try:
        for vs in config['vector_stores']:
            if vs['active']:
                return { 'name': vs['name'], 'display_name': vs['display_name'] }

    except Exception as e:
        logger.error(f"Could not get active vector store: {e}")
        return None