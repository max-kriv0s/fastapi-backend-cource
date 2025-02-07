
import hashlib
import json
from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder

from redis import Redis
import redis.asyncio as redis

from functools import wraps
from typing import Callable

from app.config import settings

def get_redis_url() -> str:
    return  f'redis://{settings.REDIS_USER}:{settings.REDIS_USER_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}'

def get_redis_connection() -> Redis:
    return redis.from_url(
        get_redis_url(),
        encoding="utf8", decode_responses=True
    )

# Декоратор для кеширования
def redis_cache(expire: int):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs) -> Response:
           # Получаем объект Redis из app.state.cache через запрос (Request)
            cache = getattr(request.app.state, "cache", None)  # Получаем Redis из состояния приложения
            if not cache:
                return await func(request=request, *args, **kwargs)
            
            # Собираем все параметры запроса (например, location, date_from, date_to)
            # Мы будем строить ключ кеша на основе всех параметров запроса
            cache_key_parts = []
            for key, value in kwargs.items():
                if key != 'cache':  # Пропускаем объект Redis, не включая его в ключ
                    cache_key_parts.append(f"{key}={value}")
            
            # Генерируем уникальный ключ для кеша
            cache_key = hashlib.md5("".join(cache_key_parts).encode('utf-8')).hexdigest()
            
            # Пытаемся получить данные из кеша
            cached_data = await cache.get(cache_key)
            if cached_data:
                # Если данные есть в кеше, возвращаем их
                cache_json = json.loads(cached_data)
                # response = cache_json.decode()
                # response = json.loads(cached_data.decode())
                return cache_json

            # Если данных нет в кеше, вызываем оригинальную функцию
            result = await func(request=request, *args, **kwargs)

            # Кэшируем результат на указанное время (TTL)
            serializable_data = jsonable_encoder(result)
            serialized_data = json.dumps(serializable_data)
            
            await cache.set(cache_key, serialized_data, ex=expire)

            return result
        return wrapper
    return decorator