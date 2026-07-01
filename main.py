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

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - greeting\n'
        '/help - list of commands\n'
        '/about - info about the bot'
    )
@dp.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(f"Created via Python(aiogram)\nMade by @zakir0vaa04")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

