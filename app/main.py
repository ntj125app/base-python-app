from fastapi import FastAPI, Body
import sentry_sdk
import os
from fastapi.responses import JSONResponse
from worker import celery
from celery.result import AsyncResult

env_dsn_sentry = os.getenv("SENTRY_PYTHON_DSN", None)

sentry_sdk.init(
    dsn=env_dsn_sentry,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=0.01,
)

app = FastAPI()

# Health check API
@app.get("/app/healthcheck")
def read_root():
    return JSONResponse({"status": "ok"})

# Celery list worker API
@app.get("/api/workers")
def get_workers():
    workers = celery.control.inspect().stats()
    return JSONResponse(workers)

# Celery get registered tasks API
@app.get("/api/tasks")
def get_task_lists():
    tasks = celery.control.inspect().registered()
    return JSONResponse(tasks)

# Celery get list of active tasks API
@app.get("/api/active-tasks")
def get_active_tasks():
    tasks = celery.control.inspect().active()
    return JSONResponse(tasks)

# Submit task API
@app.post("/api/task-submit/{task_name}")
def submit_task(task_name):
    task = celery.send_task(task_name)
    return JSONResponse({"task_id": task.id})

# Task status API
@app.get("/api/task-status/{task_id}")
def get_task_status(task_id):
    task = AsyncResult(task_id)
    return JSONResponse({"task_id": task.id, "task_status": task.status, "task_executed": task.ready(), "task_results": task.result})
