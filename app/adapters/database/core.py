# database/core.py
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

load_dotenv(dotenv_path=".env", override=True)

DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASS = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOSTNAME")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_QUERY = os.getenv("DATABASE_QUERY_PARAM")

ASYNC_DB_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?{DB_QUERY}"
    if DB_QUERY
    else f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# single shared async engine
engine = create_async_engine(ASYNC_DB_URL, pool_pre_ping=True)

# async session maker – each call returns a NEW AsyncSession
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
)

# declarative base class
Base = declarative_base()
