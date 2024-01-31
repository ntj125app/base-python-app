import os

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://base_python_redis:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://base_python_redis:6379")


@celery.task(name="create_task")
def create_task():
    return True
