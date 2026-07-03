from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton
                           )


keyboard_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Python")],
    [KeyboardButton(text="JS"), KeyboardButton(text="Java")]
], resize_keyboard=True, input_field_placeholder="You can choose one of these PL")


inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Documentation for Python", url="https://docs.python.org/3/")],
    [InlineKeyboardButton(text="Documentation for JS", url="https://devdocs.io/javascript/")],
    [InlineKeyboardButton(text="Documentation for Java", url="https://dev.java/learn/")],
    [InlineKeyboardButton(text="Get started the learning", callback_data="learn_start")],
])
