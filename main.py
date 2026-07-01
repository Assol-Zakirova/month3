import asyncio
from decouple import config
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command

BOT_TOKEN = config('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Hello! {message.from_user.first_name} I am your first bot')

@dp.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(f"Available commands\n /start - greeting with the bot\n /about - the list of commands")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

