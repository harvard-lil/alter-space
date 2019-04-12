import datetime
import time
from celery import Celery
from celery import current_app
from celery.utils.log import get_task_logger

from backend import lights

logger = get_task_logger(__name__)

celery = Celery(__name__, autofinalize=False)

lights.setup_light_store()


@celery.task(bind=True)
def wait_task(self, sleep_time):
    """sample task that sleeps 5 seconds then returns the current datetime"""
    time.sleep(sleep_time)
    return datetime.datetime.now().isoformat()


@celery.task(bind=True)
def chase_task(self, light_id):
    logger.info("chase_task %s" % light_id)
    while True:
        lights.chase(light_id)


@celery.task(bind=True)
def breathe_task(self, light_id, breathe_type):
    logger.info("breathe_task %s" % light_id, breathe_type)
    while True:
        lights.breathe(light_id, breathe_type=breathe_type)


@celery.task(bind=True)
def light_task(self, label, color, dim_value, duration=3000):
    logger.info("light_task %s" % label)
    lights.set_color(label, color, dim_value, duration=duration)


@celery.task(bind=True)
def dim_task(self, label, dim_value):
    logger.info("dim_task %s dim_value: %s" % (label, dim_value))
    lights.dim(label, dim_value)


@celery.task(bind=True)
def toggle_power_task(self, label):
    logger.info("dim_task %s" % label)
    lights.toggle_power(label)


def revoke_chain(last_result):
    logger.info('[CALLER] Revoking: %s' % last_result.task_id)
    last_result.revoke(terminate=True, signal='SIGTERM')
    if last_result.parent is not None:
        revoke_chain(last_result.parent)


@celery.task(bind=True)
def stop_task(self, task_name, task_id):
    foo_task = current_app.tasks['backend.tasks.%s_task' % task_name]
    result = foo_task.AsyncResult(task_id)
    revoke_chain(result)
