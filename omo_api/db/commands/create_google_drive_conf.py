import sys
import logging
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create
from omo_api.db.models import GoogleDriveConfig, Team, TeamConfig
from omo_api.utils.prompt import query_yes_no

logger = logging.getLogger(__name__)

gdrive_kwargs = {
    'gdrive_id': 'root',
    'delegate_email': '',
    'team_config_id': '',
}
for key in gdrive_kwargs:
    logger.debug(f"{key}: {gdrive_kwargs[key]}")

response = query_yes_no('Create GDrive Config?')

if not response:
    sys.exit()

try:
    gdrive_config, created = get_or_create(session, GoogleDriveConfig, **gdrive_kwargs)
    logger.debug(f"Created GDrive Config: {gdrive_config.id}")
except Exception as e:
    logger.debug(f"Error creating config: {e}")