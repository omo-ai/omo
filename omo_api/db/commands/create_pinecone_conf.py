import sys
import json
import logging
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create
from omo_api.db.models import PineconeConfig, Team, TeamConfig
from omo_api.utils.prompt import query_yes_no
from omo_api.utils.auth import get_aws_secret


logger = logging.getLogger(__name__)

secret_json = json.loads(get_aws_secret('prod/omo-api/alloydigital/pinecone'))

pinecone_kwargs = {
    'index_name': 'alloydigital-default',
    'environment': 'gcp-starter',
    'api_key': 'prod/omo-api/alloydigital/pinecone',
    'team_config_id': 1, # alloydigital
}


for key in pinecone_kwargs:
    print(f"{key}: {pinecone_kwargs[key]}")

response = query_yes_no('Create Pinecone Config?')

if not response:
    sys.exit()

try:
    pinecone_config, created = get_or_create(session, PineconeConfig, **pinecone_kwargs)
    logger.debug(f"Created Pinecone Config: {pinecone_config.id}")
except Exception as e:
    logger.debug(f"Error creating config: {e}")







