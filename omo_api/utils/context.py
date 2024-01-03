import json
import logging
from enum import Enum
from typing import Annotated
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from omo_api.models.slack import SlackMessagePayload
from omo_api.db.utils import get_or_create, get_db
from omo_api.db.models.slack import SlackProfile
from omo_api.db.models.user import User, Team, TeamConfig
from omo_api.db.models.pinecone import PineconeConfig
from omo_api.utils.auth import get_aws_secret


logger = logging.getLogger(__name__)

class SOURCE_CLIENT(Enum):
    SLACK = 'slack'

PINECONE_DEFAULT_INDEX = 'starter_index'
PINECONE_DEFAULT_API_KEY = '/aws/secretsmanager/path'
PINECONE_DEFAULT_ENV = 'gcp-starter'

def get_request_source(request_body: dict):
    #TODO detect request source and return the client type
    return SOURCE_CLIENT.SLACK

async def get_slack_user_context(request: Request,
                                 db: Annotated[Session, Depends(get_db)]):

    request_body = await request.json()
    slack_payload = SlackMessagePayload(**request_body)

    context = {
        'omo_slack_profile_id': None,
        'omo_user_id': None,
        'omo_team_id': None,
        'omo_team_config_id': None,
        'omo_pinecone_index': PINECONE_DEFAULT_INDEX,
        'omo_pinecone_api_key': PINECONE_DEFAULT_API_KEY,
        'omo_pinecone_env': PINECONE_DEFAULT_ENV,
        'slack_team_id': None,
        'slack_user_id': None,
    }

    """
    Get or create the SlackProfile
    """
    slack_kwargs = {
        'team_id': slack_payload.team_id,
        'slack_user_id': slack_payload.event.user,
    }
    slack_profile, created = get_or_create(db, SlackProfile, **slack_kwargs)

    context['omo_slack_profile_id'] = slack_profile.id
    context['slack_team_id'] = slack_payload.team_id
    context['slack_user_id'] = slack_payload.event.user

    """
    Get or create a Omo Team object. Initialize to Slack team info as placeholders
    if none found
    """
    try:
        # We cannot use the preferred get_or_create here, because we want to select with one field
        # but create with multiple fields set.
        stmt = select(Team).where(Team.slack_team_id == slack_payload.team_id)
        team = db.scalars(stmt).one()
        
        if not team.is_active:
            logger.debug(f"Inactive team: {slack_payload.team_id}")
            return "Team not active. Please reach out to hello@blackarrow.software to activate."
        
        context['omo_team_id'] = team.id

    except MultipleResultsFound as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        logger.debug(f"Multiple results found: {message}") 

    except NoResultFound as e:
        logger.debug(f"Team not found. {e}")
        logger.debug(f"...creating team ID {slack_payload.team_id}.")
        # Set all these to the same value

        # The payload contains no other information about the team
        # so we set it to the Slack Team ID. We can backfill this data
        # querying the Slack API with the team ID
        team = Team(**{
            'name': slack_payload.team_id,
            'slug': slack_payload.team_id,
            'slack_team_id': slack_payload.team_id,
            'is_active': True,
        })
        db.add(team)
        db.commit()

        context['omo_team_id'] = team.id

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        logger.debug(f"Exception creating team: {message}")

    """
    Create a TeamConfig object with FK to the team that was
    selected earlier
    """
    try:
        
        if not team.team_config:
            team_config = TeamConfig(**{
                'team_id': team.id
            })
            db.add(team_config)
            db.commit()
            context['omo_team_config_id'] = team_config.id
        else:
            context['omo_team_config_id'] = team.team_config.id
        

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        logger.debug(f"Exception setting team_config: {message}")

    
    """
    Set the Pinecone Config for the user
    """

    try:
        if team.team_config.pinecone_configs:
             # this is modeled as a team having many pineconf_configs but in reality they only have one
            logger.debug('Getting existing Pinecone confs')
            pc_config = team.team_config.pinecone_configs[0]

            context['omo_pinecone_index'] = pc_config.index_name

            secret = json.loads(get_aws_secret(pc_config.api_key))
            context['omo_pinecone_api_key'] = secret['api_key']
        else:
            logger.debug('Creating new Pinecone conf for team_config')
            pc_kwargs = {
                'index_name': PINECONE_DEFAULT_INDEX,
                'api_key': PINECONE_DEFAULT_API_KEY,
                'environment': PINECONE_DEFAULT_ENV,
                'team_config': team.team_config.id
            }
            pc_conf = PineconeConfig(**pc_kwargs)
            db.add(pc_conf)
            db.commit()
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        logger.debug(f"Exception setting pinecone_config: {message}") 

    """
    Create the User object with FK to SlackProfile
    """
    try:
        if not slack_profile.user_id:
            logger.debug('No User object associated with Slack ID. Creating...')
            # There is no User object associated with this Slack ID. Create one
            # use the Slack username temporarily
            user = User(**{
                'username': slack_payload.event.user,
                'is_active': True,
                'team_id': team.id,
                'email': '',
                'hashed_password': '',
            })
            db.add(user)
            db.commit()

            slack_profile.user_id = user.id
            db.add(slack_profile)
            db.commit()

            context['omo_user_id'] = user.id
        else:
            logger.debug('Slack Profile has a user ID')
            context['omo_user_id'] = slack_profile.user_id

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        logger.debug(f"Error creating user: {message}")  
    

    logger.debug(f"Returning context: {context}")
    return context
