from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database setup
engine = create_async_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 