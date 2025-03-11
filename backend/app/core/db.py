import os
import ssl
from typing import AsyncGenerator
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError

from app.core.settings import settings

# Create a single async engine with minimal pooling
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,  # Disable SQL echo in production
    poolclass=None,  # Disable pooling entirely for serverless
    # Alternative approach with minimal pooling:
    # pool_size=1,
    # max_overflow=0,
    # pool_timeout=30,
    # pool_recycle=1800,
    # pool_pre_ping=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Base model class
class Base(DeclarativeBase):
    pass

# Async database dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_factory()
    
    # Function to safely close session without throwing exceptions
    async def safe_close():
        try:
            await session.close()
        except Exception as e:
            print(f"Safe session close - handled exception: {e}")
    
    try:
        yield session
    except Exception as e:
        await session.rollback()
        print(f"Database error: {e}")
        # Don't re-raise as HTTPException to avoid middleware handling issues
        # Just pass the original exception through
        raise
    finally:
        # Use a try-except block to prevent event loop errors
        try:
            await session.close()
        except RuntimeError as e:
            if "Event loop is closed" in str(e):
                # If event loop is closed, we can't do anything about it
                print(f"Warning: Could not close session properly - {e}")
            else:
                # For other errors, log but continue
                print(f"Error during session close: {e}")
        except Exception as e:
            # Catch any other exceptions during closing
            print(f"Unexpected error during session close: {e}")

# Special cleanup function that can be called directly from route handlers
# in critical paths if needed
async def cleanup_db_resources():
    try:
        await engine.dispose()
    except Exception as e:
        print(f"Error during engine disposal: {e}")