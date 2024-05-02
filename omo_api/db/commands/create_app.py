import click
from omo_api.db.models import Application
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create

@click.command()
@click.option('--name', '-n', required=True, help='App name')
@click.option('--userid', '-u', required=True, help='User ID')
def create_app(name, userid):
    """Generate an Application for a User"""
    app_kwargs = {
        'name': name,
        'user_id': userid
    }
    app, created = get_or_create(session, Application, **app_kwargs)

    if created:
        click.echo(f"App \"{name}\" created!")
    else:
        click.echo(f"App \"{name}\" already exists. App ID: {app.id}") 

if __name__ == '__main__':
    create_app()