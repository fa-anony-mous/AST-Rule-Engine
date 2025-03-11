from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.settings import settings
from typing import AsyncGenerator
import ssl
import os

# Get the certificate content from the environment variable
ca_certificate_content = os.environ.get("SUPABASE_CA_CERTIFICATE_CONTENT")

# Create an SSL context from the certificate content
ssl_context = None
if ca_certificate_content:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_verify_locations(cadata=ca_certificate_content)  # Load from content

# PostgreSQL Async Setup
connect_args = {}
if ssl_context:
    connect_args["ssl"] = ssl_context  # Pass the SSL context correctly

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
    connect_args=connect_args  # Pass SSL context correctly
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):  # Preferred way in SQLAlchemy 2.0+
    pass

# Async Database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
