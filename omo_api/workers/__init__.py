# Import tasks here. They will be autodiscovered
# when the Celery object is created
from omo_api.workers.drive import tasks as gdrive_tasks
from omo_api.workers.notion import tasks as notion_tasks