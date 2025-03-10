import asyncio
import asyncpg

async def test_connection():
    try:
        conn = await asyncpg.connect("postgresql://postgres:saketh123@db.zfcqnzovzfgdogwlkzsj.supabase.co:5432/postgres?sslmode=prefer")
        print("✅ Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

asyncio.run(test_connection())
