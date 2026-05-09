import asyncio
import asyncpg
from config import DATABASE_URL

# asyncpg needs plain postgresql:// not postgresql+asyncpg://
url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

async def main():
    with open("migrate_v2.sql") as f:
        sql = f.read()

    conn = await asyncpg.connect(url)
    try:
        # Run each statement separately (asyncpg doesn't support multi-statement strings)
        statements = [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("--")]
        for stmt in statements:
            try:
                await conn.execute(stmt)
                print(f"OK: {stmt[:60]}...")
            except Exception as e:
                print(f"SKIP/ERROR: {e} — {stmt[:60]}")
    finally:
        await conn.close()
    print("\nMigration complete.")

asyncio.run(main())
