from celery import Celery
from celery.schedules import crontab
from app.core.config import REDIS_URL

celery_app = Celery(
    __name__,
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.backlink_task", "app.tasks.scheduler"]
)

celery_app.conf.timezone = "Asia/Kolkata"

celery_app.conf.beat_schedule = {
    'run-scheduled-jobs-every-minute': {
        'task': 'app.tasks.scheduler.check_and_schedule_jobs',
        'schedule': crontab(minute='*'),
    },
}