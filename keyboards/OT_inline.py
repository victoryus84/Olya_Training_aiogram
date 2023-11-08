from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="YouTube", url="https://youtu.be/@fsoky"),
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=fsoky_community")
        ]
    ]
)

sub_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подписаться", url="https://t.me/fsoky_community")
        ]
    ]
)

begin_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Let's begin \ Să începem.", callback_data="begin")
        ]
    ]
)

begin_course_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Why? \n De ce?", callback_data="begin_course")
        ]
    ]
)

ok_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="OK \n Bine?", callback_data="ok_step")
        ]
    ]
)

next_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Next \n Pasul Urmator", callback_data="next_step")
        ]
    ]
)

show_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="""Show the interview questions.
                \nAfiseaza intrebarile pentru interviu.""", callback_data="next_step")
        ]
    ]
)