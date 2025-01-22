from celery import Celery
from celery.schedules import crontab

from app.cache.cache import get_redis_url


redis_url = get_redis_url()

celery_app = Celery(
    'tasks',
    broker=redis_url,
    include=['app.tasks.tasks',
             'app.tasks.scheduled'],
    broker_connection_retry_on_startup=True,
    # backend=redis_url
)

celery_app.conf.beat_schedule = {
    'name': {
        'task': 'periodic_task',
        "schedule": 5 # seconds
        # 'schedule': crontab(minute='30', hour='15')
    }
}