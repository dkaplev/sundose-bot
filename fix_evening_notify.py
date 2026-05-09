import asyncio
import asyncpg
from config import DATABASE_URL

url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

async def main():
    conn = await asyncpg.connect(url)
    await conn.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS evening_notify BOOLEAN DEFAULT FALSE")
    print("OK: evening_notify column added")
    await conn.close()

asyncio.run(main())
