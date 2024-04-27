import sys
import secrets
import click
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from omo_api.db.models import UserAPIKey, User
from omo_api.db.connection import session
from omo_api.utils.auth import create_api_key
from omo_api.settings import cipher_suite

@click.command()
@click.option('--userid', help='User ID')
def create_api_key(userid):
    """Generate an API key for a user ID"""
    max_attempts = 5
    num_attempts = 0
    stmt = select(User).where(User.id == userid)
    user = session.execute(stmt).one_or_none()

    if not user:
        click.echo('User not found. Exiting')
        raise click.Abort()
    else:
        user = user[0] # sqlalchemy returns result in a set
    
    while num_attempts < max_attempts:

        key = create_api_key()

        try:
            result = session.query(UserAPIKey).filter(UserAPIKey.api_key == key).count()

            if result > 0:
                raise MultipleResultsFound

            click.echo('Creating new API Key...')
            user_api_key = UserAPIKey(user_id=user.id, api_key=key)

            session.add(user_api_key)
            session.commit()
            click.echo(f"API Key created: {key}")

            sys.exit(0) # return successfully

        except Exception as e:
            click.echo(f'Exception: {e}. Generating another...')
            num_attempts += 1
            continue
    

    else:
        click.echo(f"Hit max attempts {max_attempts}. Exiting")
        click.Abort()


if __name__ == '__main__':
    create_api_key()