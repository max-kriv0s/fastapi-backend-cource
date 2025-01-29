from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqladmin import Admin
from app.admin.auth import authentication_backend

from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.admin.view import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.cache.cache import get_redis_connection

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.images.router import router as router_images

from app.pages.router import router as router_pages

from app.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация Redis с использованием aioredis
    redis = get_redis_connection()
    
    # Ожидание подключения к Redis
    await redis.ping()  # Проверка подключения
    
    # Передаем cache_manager в приложение (если нужно)
    app.state.cache = redis
    
    yield
    
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_images)

app.include_router(router_pages)


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 
                   'Access-Control-Allow-Origin', 'Authorization'
    ]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

