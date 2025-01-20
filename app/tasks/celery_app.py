from celery import Celery
from app.cache.cache import get_redis_url


redis_url = get_redis_url()

celery_app = Celery(
    'tasks',
    broker=redis_url,
    include=['app.tasks.tasks'],
    broker_connection_retry_on_startup=True,
    # backend=redis_url
)