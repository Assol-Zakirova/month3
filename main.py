import asyncio
from config import BOT_TOKEN
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from src.handlers import router
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from db.database import init_db

BOT_TOKEN = BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main(): 
    init_db()
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

