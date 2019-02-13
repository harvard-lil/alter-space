import datetime
import time
import logging
from celery import Celery
from celery import current_app

from backend import lights

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)


@celery.task(bind=True)
def wait_task(self, sleep_time):
    """sample task that sleeps 5 seconds then returns the current datetime"""
    time.sleep(sleep_time)
    return datetime.datetime.now().isoformat()


@celery.task(bind=True)
def chase_task(self, id):
    print("chase_task", id)
    while True:
        lights.chase(id)


@celery.task(bind=True)
def breathe_task(self, id):
    print("breathe_task", id)
    while True:
        lights.breathe(id)


@celery.task(bind=True)
def light_task(self, id, colors, dim_value):
    lights.set_colors(id, colors, dim_value)


@celery.task(bind=True)
def dim_task(self, id, dim_value):
    lights.dim(id, dim_value)


def revoke_chain(last_result):
    print('[CALLER] Revoking: %s' % last_result.task_id)
    last_result.revoke(terminate=True, signal='SIGKILL')
    if last_result.parent is not None:
        revoke_chain(last_result.parent)


@celery.task(bind=True)
def stop_task(self, task_name, task_id):
    foo_task = current_app.tasks['backend.tasks.%s_task' % task_name]
    result = foo_task.AsyncResult(task_id)
    revoke_chain(result)
