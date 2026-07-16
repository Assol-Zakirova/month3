from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from src.keyboards import keyboard_main, inline, restart_inline
from aiogram.fsm.state import  State, StatesGroup
from src.questions import QUESTIONS
from db.users import get_user, create_user
from db.results import get_score
from db.questions import get_all_questions, add_question, delete_question, if_exists, get_question_by_id
from db.results import save_result, get_score, delete_score, get_rating

router = Router()

class Quiz(StatesGroup):
    waiting_answer = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Anonymouse")
    await message.answer(f'Hello {message.from_user.first_name}! I am your first bot', reply_markup=keyboard_main)

@router.message(Command('list'))
async def cmd_list(message: Message):
    questions = get_all_questions()
    if questions:
        await message.answer ("\n".join([f'{i.get('id')}. {i.get('question_text')} - {i.get('correct_answer')}' for i in questions]))
    else:
        await message.answer("There are not any questions")

@router.message(Command('add'))
async def cmd_add(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Enter: /add question | answer\n" 
        "Example: /add The capital of Spain? | madrid")
        return
    parts = command.args.split("|")
    if len(parts) != 2:
        await message.answer('You need to divide question and answer via |')
        return
    question_text = parts[0].strip().lower()
    answer_text = parts[1].strip().lower()
    if not if_exists(question_text):
        await message.answer('This kind of question is already exists')
        return
    new_id = add_question(question_text, answer_text)
    await message.answer(f"The question was added succsessfully its ID is {new_id.get("id")}")

@router.message(Command("del"))
async def cmd_del(message: Message, command: CommandObject):
    if not command.args or not command.args.isdigit():
        await message.answer("Enter: /del id\n"
            "Example: /del 8")
        return 
    index = int(command.args.strip())
    if not get_question_by_id(index):
        await message.answer("There is no question with such ID")
        return
    delete_question(index)
    await message.answer(f"The question with ID {index} was succsessfully deleted")

@router.message(Command("rating"))
async def cmd_rating(message: Message):
    rating = get_rating()
    if not rating:
        await message.answer("There is no users with score")
        return
    print(rating)
    top_3 = rating[3] if len(rating) >= 3 else rating
    await message.answer("\n".join([f"{i.get("username")} - {i.get("total")}" for i in top_3]))


@router.callback_query(F.data == "my_score")
async def my_score(callback: CallbackQuery):
    user = get_user(
        telegram_id=callback.from_user.id)

    if not user:
        await callback.answer('User Not Found', show_alert=True)
        return
    
    data = get_score(
        user_id=user.get("id")
    )
    await callback.answer('')
    await callback.message.answer(f'Your score: {data["correct"] or 0}/{data["total"] or 0}', show_alert=True)

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
    if not get_all_questions():
        await callback.message.answer(f"The database is empty")
        return
    user = get_user(callback.from_user.id)
    if get_score(user.get('id')):
        delete_score(user.get('id'))
    await state.update_data(index=1, score=0)
    await state.set_state(Quiz.waiting_answer)
    await callback.message.answer(f"Question 1: {get_question_by_id(1).get('question_text')}")

@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]
    question = get_question_by_id(index)
    user = get_user(message.from_user.id)
    is_correct = message.text.lower() == question.get('correct_answer')
    save_result(user.get('id'), index, int(is_correct))
    if is_correct:
        score += 1
        await message.answer("Correct! +1")
    else:
        await message.answer(f"Incorrect! The right answer is: {get_question_by_id(index).get('correct_answer')}")
    
    index += 1
    if index > len(get_all_questions()):
        await message.answer(f"The end! Your score: {score}/{len(get_all_questions())}", reply_markup=restart_inline)
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Question {index}: {get_question_by_id(index).get('question_text')}")

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

