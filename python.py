import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test_connection():
    engine = create_async_engine("postgresql+asyncpg://postgres:saketh123@db.zfcqnzovzfgdogwlkzsj.supabase.co:5432/postgres")
    async with engine.connect() as conn:
        print("Connection successful!")

asyncio.run(test_connection())