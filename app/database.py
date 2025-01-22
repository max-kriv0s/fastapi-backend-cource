from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_async_engine(settings.database_url)
engine_nullpool = create_async_engine(settings.database_url, poolclass=NullPool)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async_session_maker_nullpool = async_sessionmaker(engine_nullpool, expire_on_commit=False)

class Base(DeclarativeBase):
    pass