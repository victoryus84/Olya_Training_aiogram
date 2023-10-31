from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards import fabrics
from data.subloader import get_json
from data.OT_constants import COURSES

router = Router()

# Funcția care returnează cursurile unei universități
def get_dict_key_from_value(val, my_dict):
   
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return print(f"for value {val} key doesn't exist")

# Funcția care returnează cursurile unei universități
def get_courses_for_university(university_name):
    return COURSES.get(university_name, [])

# @router.callback_query_handler(F.Text(equals="my_button_data"))
# async def my_button_callback(callback_query: CallbackQuery):
#     # Gestionează acțiunea butonului aici
#     print(f"my_button_callback")
#     await callback_query.answer("Ai apăsat pe 'My Button'")
