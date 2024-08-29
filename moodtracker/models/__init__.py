from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from . import moods
from . import users

from .moods import *
from .users import *

connect_args = {}

engine = None

def init_db(settings):
    global engine
    engine = create_async_engine(
        settings.SQLDB_URL, 
        echo = True, 
        future = True,
        connect_args = connect_args,
    )

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession: # type: ignore
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session