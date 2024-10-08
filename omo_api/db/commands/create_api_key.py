import sys
import click
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from omo_api.db.models import APIKey, Application
from omo_api.db.connection import session
from omo_api.utils import create_api_key, get_api_key_hash

@click.command()
@click.option('--appid', '-a', help='App ID')
def create_app_api_key(appid):
    """Generate an API key for an Application"""
    max_attempts = 5
    num_attempts = 0

    stmt = select(Application).where(Application.id == appid)
    app = session.execute(stmt).one_or_none()

    if not app:
        click.echo('User not found. Exiting')
        raise click.Abort()
    else:
        app = app[0] # sqlalchemy returns result in a set
    
    while num_attempts < max_attempts:

        raw_api_key = create_api_key()
        hashed_key = get_api_key_hash(raw_api_key)

        try:
            result = session.query(APIKey).filter(APIKey.hashed_api_key == hashed_key).count()

            if result > 0:
                raise MultipleResultsFound

            click.echo('Creating new API Key...')
            app_api_key = APIKey(app_id=app.id, hashed_api_key=hashed_key)

            session.add(app_api_key)
            session.commit()
            output = f"""
            API Key created! Save this key somewhere safe. We'll only display
            this once below. If you lose this, you'll have to generate a
            new API key.
            API Key: {raw_api_key}
            """
            click.echo(output)

            sys.exit(0) # return successfully

        except Exception as e:
            click.echo(f'Exception: {e}. Generating another...')
            num_attempts += 1
            continue
    

    else:
        click.echo(f"Hit max attempts {max_attempts}. Exiting")
        click.Abort()


if __name__ == '__main__':
    create_app_api_key()