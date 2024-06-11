import os
import time

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.result_expires = 3600

@celery.task(bind=True,name="test_task")
def test_task(self):
    return {"return": True, "message": "test_task done"}
