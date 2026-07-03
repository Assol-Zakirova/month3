from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from src.keyboards import keyboard_main, inline


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Hello {message.from_user.first_name}! I am your first bot',
        reply_markup=keyboard_main
        )
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - greeting\n'
        '/help - the list of commands',
        reply_markup=inline
    )

@router.callback_query(F.data == "learn_start")
async def quiz_start(callback: CallbackQuery):
    await callback.answer('Are you ready?', show_alert=True)
    await callback.message.answer("We are getting started!")

@router.message(F.text == "Python")
async def cmd_python(message: Message):
    await message.answer("Python is a highly popular, general-purpose programming language known for its clean, readable syntax. It is used for web development, software creation, data analysis, and automation. Because it is beginner-friendly and requires fewer lines of code, it is the top choice for developers and non-programmers alike.")

@router.message(F.text == "JS")
async def cmd_js(message: Message):
    await message.answer("JavaScript (JS) is a versatile programming language primarily used to add dynamic, interactive behavior to websites. Alongside HTML and CSS, it is one of the three core technologies that power the modern web. Without it, websites would just be static text and images.")

@router.message(F.text == "Java")
async def cmd_java(message: Message):
    await message.answer("Java is a widely used, object-oriented programming language and software computing platform. Developed by Sun Microsystems and now owned by Oracle, it powers billions of devices globally, ranging from Android mobile phones to enterprise-level banking systems and desktop applications.")

@router.message(F.text == "Trash")
async def get_group(message: Message):
    await message.answer("Hello this is your trash")

@router.message()
async def echo(message: Message):
    await message.answer(f"You sent: {message.text}")

