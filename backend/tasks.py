import datetime
import time
import logging
from celery import Celery
from celery import current_app

from backend import lights

from config import config
logging.basicConfig(filename=config.LOG_FILENAME, format=config.LOG_FORMAT, level=config.LOG_LEVEL)

logger = logging.getLogger(__name__)

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
def light_task(self, light_id, colors, dim_value):
    logger.info("light_task %s" % light_id)
    lights.set_colors(light_id, colors, dim_value)


@celery.task(bind=True)
def dim_task(self, light_id, dim_value):
    logger.info("dim_task %s dim_value: %s" % (light_id, dim_value))
    lights.dim(light_id, dim_value)


def revoke_chain(last_result):
    logger.info('[CALLER] Revoking: %s' % last_result.task_id)
    last_result.revoke(terminate=True, signal='SIGKILL')
    if last_result.parent is not None:
        revoke_chain(last_result.parent)


@celery.task(bind=True)
def stop_task(self, task_name, task_id):
    foo_task = current_app.tasks['backend.tasks.%s_task' % task_name]
    result = foo_task.AsyncResult(task_id)
    revoke_chain(result)
