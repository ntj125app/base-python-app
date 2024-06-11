import os
import time

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.result_expires = 3600
celery.conf.update(result_extended=True)

@celery.task(bind=True,name="test_task")
def test_task(self):
    return {"return": True, "message": "test_task done"}

@celery.task(bind=True,name="test_body_task")
def test_body_task(self, args1: str | None = None, args2: str | None = None, args3: str | None = None):
    body = {"args1": args1, "args2": args2, "args3": args3}
    return {"return": True, "message": "test_body_task done", "body": body}