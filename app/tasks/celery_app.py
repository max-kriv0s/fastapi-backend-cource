from celery import Celery
from app.cache.cache import get_redis_url

celery = Celery(
    'tasks',
    brocker=get_redis_url(),
    include=['app.tasks.tasks']
)