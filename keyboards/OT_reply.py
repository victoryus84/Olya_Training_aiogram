from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
)
import data.OT_constants as constants   
import data.OT_messages as texts

# def build_buttons_dict(data):
#     # data este o listă sau altă structură de date care conține informații pentru butoane
#     buttons = []
    
#     for key, value in data.items():
#         button = KeyboardButton(
#         text=value
#         )
#         buttons.append(button)
#     return buttons

# def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, header_buttons)
#     if footer_buttons:
#         menu.append(footer_buttons)
#     return menu
language_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=constants.LANGUAGES_DICT.get("en")),
            KeyboardButton(text=constants.LANGUAGES_DICT.get("ro"))
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose a language",
)
    
ok_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="OK")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click button please",
)

next_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Next")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click button please",
)

show_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="""Show the interview questions.
                \nAfiseaza intrebarile pentru interviu.""")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click button please",
)        
    
    