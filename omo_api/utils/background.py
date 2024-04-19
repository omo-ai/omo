import enum

class TaskStates(enum.Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    RETRY = 'RETRY'
    PROGRESS = 'PROGRESS'

def get_celery_task_status(task_id: str):
    from omo_api.workers.background import celery

    res = celery.AsyncResult(task_id)
    return {'ready': res.ready(), 'status': res.status }