import asyncio
import asyncpg

async def test_connection():
    conn = await asyncpg.connect('postgresql://postgres:saketh123@db.zfcqnzovzfgdogwlkzsj.supabase.co:5432/postgres?sslmode=require')
    print("Connection successful!")
    await conn.close()

asyncio.run(test_connection())