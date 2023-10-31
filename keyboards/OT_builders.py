from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data.OT_constants import UNIVERSITIES_ARRAY, COURSES
from callbacks.OT_procedures import *
def universities():
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in UNIVERSITIES_ARRAY]
    builder.button(text="Cancel")
    builder.adjust(*[4] * 4)

    return builder.as_markup(resize_keyboard=True)

def courses(university):
    
    univ_courses = get_courses_for_university(university)
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in univ_courses]
    builder.button(text="Cancel")
    builder.adjust(*[1] * 4)

    return builder.as_markup(resize_keyboard=True)


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    
    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)