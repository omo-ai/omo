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

class SlackUserContext:
    def __init__(self, payload: SlackMessagePayload, db: Session):
        self.context = {
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
        self.msg_payload = payload
        self.db = db

    def get_context(self):
        return self.context
    
    def slack_profile_context(self):
        slack_kwargs = {
            'team_id': self.msg_payload.team_id,
            'slack_user_id': self.msg_payload.event.user,
        }
        slack_profile, created = get_or_create(self.db, SlackProfile, **slack_kwargs)

        self.context['omo_slack_profile_id'] = slack_profile.id
        self.context['slack_team_id'] = self.msg_payload.team_id
        self.context['slack_user_id'] = self.msg_payload.event.user 

        return slack_profile
    
    def team_context(self):
        """
        Get or create a Omo Team object. Initialize to Slack team info as placeholders
        if none found
        """
        team = None
        try:
            # We cannot use the preferred get_or_create here, because we want to select with one field
            # but create with multiple fields set.
            stmt = select(Team).where(Team.slack_team_id == self.msg_payload.team_id)
            team = self.db.scalars(stmt).one()
            
            if not team.is_active:
                logger.debug(f"Inactive team: {self.msg_payload.team_id}")
                return "Team not active. Please reach out to hello@blackarrow.software to activate."
            
            self.context['omo_team_id'] = team.id

        except MultipleResultsFound as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            logger.debug(f"Multiple results found: {message}") 

        except NoResultFound as e:
            logger.debug(f"Team not found. {e}")
            logger.debug(f"...creating team ID {self.msg_payload.team_id}.")
            # Set all these to the same value

            # The payload contains no other information about the team
            # so we set it to the Slack Team ID. We can backfill this data
            # querying the Slack API with the team ID
            team = Team(**{
                'name': self.msg_payload.team_id,
                'slug': self.msg_payload.team_id,
                'slack_team_id': self.msg_payload.team_id,
                'is_active': True,
            })
            self.db.add(team)
            self.db.commit()

            self.context['omo_team_id'] = team.id

        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            logger.debug(f"Exception creating team: {message}")

        return team

    def team_config_context(self, team: Team):
        """
        Create a TeamConfig object with FK to the team that was
        selected earlier
        """
        team_config = None
        try:
            if not team.team_config:
                team_config = TeamConfig(**{
                    'team_id': team.id
                })
                self.db.add(team_config)
                self.db.commit()
                self.context['omo_team_config_id'] = team_config.id
            else:
                self.context['omo_team_config_id'] = team.team_config.id
                team_config = team.team_config
        
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            logger.debug(f"Exception setting team_config: {message}")

        return team_config

    def pinecone_context(self, team: Team):
        """
        Set the Pinecone Config for the user
        """
        pinecone_ctx = None

        try:

            if not team.team_config.pinecone_configs:
                # create the pinecone config for the team
                logger.debug(f"Creating new default pinecone conf for team_config: {team.team_config.id}")
                pc_kwargs = {
                    'index_name': PINECONE_DEFAULT_INDEX,
                    'api_key': PINECONE_DEFAULT_API_KEY,
                    'environment': PINECONE_DEFAULT_ENV,
                    'team_config_id': team.team_config.id
                }
                pc_config = PineconeConfig(**pc_kwargs)
                self.db.add(pc_config)
                self.db.commit()
                logger.debug(f"...created pinecone config {pc_config.id}")

            else:
                pc_config = team.team_config.pinecone_configs[0]

            self.context['omo_pinecone_index'] = pc_config.index_name 
            self.context['omo_pinecone_env'] = pc_config.environment
            
            secret = json.loads(get_aws_secret(pc_config.api_key))
            self.context['omo_pinecone_api_key'] = secret['api_key']

            pinecone_ctx = pc_config

        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            logger.debug(f"Exception setting pinecone config: {message}") 


        return pinecone_ctx
        
    def user_context(self, team: Team, slack_profile: SlackProfile) -> User:
        """
        Create the User object with FK to SlackProfile
        """
        user = None
        try:
            if not slack_profile.user_id:
                logger.debug('No User object associated with Slack ID. Creating...')
                # There is no User object associated with this Slack ID. Create one
                # use the Slack username temporarily
                user = User(**{
                    'username': self.msg_payload.event.user,
                    'is_active': True,
                    'team_id': team.id,
                    'email': '',
                    'hashed_password': '',
                })
                self.db.add(user)
                self.db.commit()

                slack_profile.user_id = user.id
                self.db.add(slack_profile)
                self.db.commit()

                self.context['omo_user_id'] = user.id
            else:
                logger.debug('Slack Profile has a user ID')
                self.context['omo_user_id'] = slack_profile.user_id
                user = slack_profile.user

        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            logger.debug(f"Error creating user: {message}")  

        return user

async def get_slack_user_context(body: SlackMessagePayload,
                                 db: Annotated[Session, Depends(get_db)]):

    ctx = SlackUserContext(body, db)

    slack_profile = ctx.slack_profile_context()
    team = ctx.team_context()
    
    if team:
        team_config_ctx = ctx.team_config_context(team)
        pinecone_ctx = ctx.pinecone_context(team)

        if slack_profile:
            user_ctx = ctx.user_context(team, slack_profile)
        else:
            msg = "Exception creating context: No Slack Profile"
            logger.debug(f"{msg}: {body}")
    else:
        msg = "Exception creating context: No Team"
        logger.debug(f"{msg}: {body}")

    return ctx.get_context() 
