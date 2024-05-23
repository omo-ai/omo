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


def display_task_status(status: str):
    """The status to display on the frontend"""
    if status == TaskStates.PENDING.value:
        # Task ID is pending OR unknown
        return 'synced'
    if status == TaskStates.PROGRESS.value:
        return 'syncing'
    if status == TaskStates.SUCCESS.value:
        return 'synced'
    if status == TaskStates.FAILURE.value:
        return 'error'
    
    return status