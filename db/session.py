from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger('db_session')

# Get root directory
ROOT_DIR = Path(__file__).parent.parent

# Database URL - SQLite in root folder
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{ROOT_DIR}/db.sqlite3")
logger.info(f"Database URL: {DATABASE_URL}")

# Async engine for FastAPI/bot
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Sync engine for SQLAdmin
SYNC_DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
)


async def get_async_session():
    """Async session dependency for FastAPI endpoints"""
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_session():
    """Sync session dependency for SQLAdmin"""
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()

