import asyncio
import sys
import os
from pathlib import Path
from aiogram import Bot, Dispatcher

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from handlers import router
from db.base import Base
from db.session import async_engine
from utils.logger import setup_logger

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
logger = setup_logger('bot_main')


async def main():
    logger.info("Starting bot...")
    # Create all tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Bot started polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
