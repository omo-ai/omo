from celery import Celery
from omo_api.utils import get_env_var

celery = Celery(
    'celery',
    broker=get_env_var('CELERY_BROKER'),
    backend=get_env_var('CELERY_BACKEND'),
    include=['omo_api.workers.drive.tasks']
)