import os
import ssl
from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql.expression import Delete, Insert, Update
from sqlalchemy.exc import SQLAlchemyError

from app.core.settings import settings

# Context variable for session scoping
session_context: ContextVar[str] = ContextVar("session_context")

print(f"SQLALCHEMY_DATABASE_URI: {settings.SQLALCHEMY_DATABASE_URI}")

def get_session_context() -> str:
    return session_context.get()

def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)

def reset_session_context(context: Token) -> None:
    session_context.reset(context)

# Enum for engine type (supports future read/write separation)
class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"

# # Configure SSL if certificate is provided
# ca_certificate_content = os.environ.get("SUPABASE_CA_CERTIFICATE_CONTENT")
# ssl_context = None
# if ca_certificate_content:
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = True
#     ssl_context.verify_mode = ssl.CERT_REQUIRED
#     ssl_context.load_verify_locations(cadata=ca_certificate_content)

# # Database connection arguments
# connect_args = {}
# if ssl_context:
#     connect_args["ssl_context"] = ssl_context  # Correct key for SQLAlchemy

# Async Database Engines (Support Read/Write Separation)
engines = {
    EngineType.WRITER: create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        echo=True,
        pool_size=10,
        max_overflow=5,
        pool_pre_ping=False,  # ❌ Disable pre-ping for testing
        pool_recycle=300,  # ✅ Increase recycle time to 5 minutes (or try -1 to disable recycle)
        # connect_args=connect_args,
    ),
    EngineType.READER: create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI,  # Currently same DB, change if needed
        echo=True,
        pool_size=10,
        max_overflow=5,
        pool_pre_ping=False, # ❌ Disable pre-ping for testing
        pool_recycle=300, # ✅ Increase recycle time to 5 minutes (or try -1 to disable recycle)
        # connect_args=connect_args,
    ),
}

# Custom Session Class to Route Queries (Read vs. Write)
class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine  # Write queries use WRITER DB
        else:
            return engines[EngineType.READER].sync_engine  # Read queries use READER DB

# Create a Session Factory
_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)

# Base Model
class Base(DeclarativeBase):
    pass

# Async Session Dependency for FastAPI
@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = _async_session_factory()
    try:
        yield _session
    except SQLAlchemyError as e:
        await _session.rollback()  # ✅ Rollback on error
        raise e
    finally:
        await _session.close() 
     # ✅ Ensure session closes properly

#use session_factory() as db:
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as db:
        yield db