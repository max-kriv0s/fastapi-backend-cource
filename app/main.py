from contextlib import asynccontextmanager
import time
from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI

from app.admin.auth import authentication_backend
from app.admin.view import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.cache.cache import get_redis_connection
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users


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


app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_images)

app.include_router(router_pages)
from app.logger import logger

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

app = VersionedFastAPI(app, 
    version_format='{major}',
    prefix_format='/v{major}'
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        start_time = time.perf_counter()
        logger.info("Processing request", extra={"url": str(request.url)})
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        # response.headers["X-Process-Time"] = str(process_time)
        
        logger.info('Request handling time', extra={
            'process_time': round(process_time, 4)
        })
        
        return response

    except Exception as e:
        import traceback
        logger.error(f"Unhandled exception: {e}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

app.mount('/static', StaticFiles(directory='app/static'), 'static')