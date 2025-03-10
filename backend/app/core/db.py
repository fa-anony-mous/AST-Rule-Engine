from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.settings import settings  # Correct import
from typing import AsyncGenerator
import ssl

# Explicit SSL context
ssl_context = ssl.create_default_context(cafile="/etc/ssl/certs/ca-certificates.crt")  # Or path to your CA cert

# PostgreSQL Async Setup
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
    connect_args={"ssl": ssl_context}  # Pass SSL context
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Async Database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 