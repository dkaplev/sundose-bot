import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.handlers import info, settings, start
from bot.handlers import duels
from bot.middleware import DatabaseMiddleware
from bot.scheduler import setup_scheduler
from config import BOT_TOKEN, DATABASE_URL
from db.models import Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(DatabaseMiddleware(session_factory))

    dp.include_router(start.router)
    dp.include_router(settings.router)
    dp.include_router(info.router)
    dp.include_router(duels.router)

    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler, bot, session_factory)
    scheduler.start()

    logger.info("SunDose bot starting...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), scheduler=scheduler)
    finally:
        scheduler.shutdown()
        await bot.session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
