from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    settings.app_name,
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Paris",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,
)

# Exemple de tâche périodique (type cron) : nettoyage toutes les nuits à 3h
celery_app.conf.beat_schedule = {
    "nettoyage-quotidien": {
        "task": "app.tasks.tache_planifiee_exemple",
        "schedule": crontab(hour=3, minute=0),
    },
}
