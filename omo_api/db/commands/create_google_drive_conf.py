import sys
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create
from omo_api.db.models import GoogleDriveConfig, Team, TeamConfig
from omo_api.utils.prompt import query_yes_no

gdrive_kwargs = {
    'gdrive_id': 'root',
    'delegate_email': 'chris@helloomo.ai',
    'team_config_id': 1,
}
for key in gdrive_kwargs:
    print(f"{key}: {gdrive_kwargs[key]}")
response = query_yes_no('Create GDrive Config?')

if not response:
    sys.exit()

try:
    gdrive_config, created = get_or_create(session, GoogleDriveConfig, **gdrive_kwargs)
    print(f"Created GDrive Config: {gdrive_config.id}")
except Exception as e:
    print(f"Error creating config: {e}")