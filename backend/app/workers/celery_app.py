from celery import Celery

from app.config import settings


celery_app = Celery(
    "enterprise_support_agent",
    broker=settings.redis_broker_url,
    backend=settings.redis_result_backend,
    include=["app.workers.tasks"],
)