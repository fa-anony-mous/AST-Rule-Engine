from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.settings import settings
from typing import AsyncGenerator
import ssl
import os
import io

# Get the certificate content from the environment variable
ca_certificate_content = os.environ.get("SUPABASE_CA_CERTIFICATE_CONTENT")

# Create an SSL context from the certificate content
if ca_certificate_content:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_verify_locations(cadata=ca_certificate_content)  # Load from content
else:
    ssl_context = None  # Handle the case where the environment variable is not set

# PostgreSQL Async Setup
connect_args = {}
if ssl_context:
    connect_args["ssl"] = ssl_context

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
    connect_args=connect_args  # Pass SSL context
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