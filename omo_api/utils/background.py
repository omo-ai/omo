import enum
import logging
from celery.result import GroupResult
from .exceptions import CeleryGroupError

logger = logging.getLogger(__name__)


class TaskStates(enum.Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    RETRY = 'RETRY'
    PROGRESS = 'PROGRESS'

def get_celery_task_status(task_id: str) -> dict:
    from omo_api.workers.background import celery

    res = celery.AsyncResult(task_id)
    return {'ready': res.ready(), 'status': res.status }


def display_task_status(status: str) -> str:
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

def get_celery_group_progress(group_id: str) -> list:
    from omo_api.workers.background import celery
    try:
        gr = GroupResult.restore(group_id)

        if not gr:
            raise CeleryGroupError(f"Task group {group_id} not found")

        group_progress = { 
            'group_id': group_id,
            'num_tasks': len(gr.children), 
            'num_ready': sum([task.ready() for task in gr.results]), # ready = task ran but may have succeeeded or failed
            'num_success': gr.completed_count(),
            'num_failed': sum([task.failed() for task in gr.results]),
            'children': [task.id for task in gr.children],
        }
    except Exception as e:
        logger.error(f"Could not get group status: {e}")
        group_progress = {}

    return group_progress


def get_celery_group_status(group_id: str) -> tuple:
    progress = get_celery_group_progress(group_id)

    if not progress or 'num_failed' not in progress:
        logger.error(f"Group {group_id} not found")
        return 'error', 0.0

    if progress['num_failed']:
        logger.error(f"Group {group_id} failed: { progress['num_failed'] } tasks failed")
        return 'failed', 0.0

    pct_complete = progress['num_success'] / progress['num_tasks']

    if pct_complete == 1:
        return 'synced', pct_complete

    elif pct_complete < 1:
        return 'syncing', pct_complete