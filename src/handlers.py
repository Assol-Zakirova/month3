from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from src.keyboards import keyboard_main, inline, restart_inline
from aiogram.fsm.state import  State, StatesGroup
from src.questions import QUESTIONS

router = Router()

class Quiz(StatesGroup):
    waiting_answer = State()

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


@router.message(Command('game'))
async def cmd_game(message: Message):
    await message.answer("Choose one field", reply_markup=inline)

@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Are you ready?', show_alert=True)
    await state.update_data(index=0, score=0)
    await state.set_state(Quiz.waiting_answer)      
    await callback.message.answer(f"Question 1: {QUESTIONS[0]['q']}")

@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]

    if message.text.lower() == QUESTIONS[index]['a']:
        score += 1
        await message.answer("Correct! +1")
    else:
        await message.answer(f"Incorrect! The right answer is: {QUESTIONS[index]['a']}")
    
    index += 1
    if index >= len(QUESTIONS):
        await message.answer(f"The end! Your score: {score}/{len(QUESTIONS)}", reply_markup=restart_inline)
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Question {index+1}: {QUESTIONS[index]['q']}")

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

