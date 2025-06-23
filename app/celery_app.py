from celery import Celery

from app.core.logging import setup_logging

setup_logging()

celery_app = Celery(
    "feedhound",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.task_routes = {
    "app.tasks.parser*": {"queue": "default"},
}

