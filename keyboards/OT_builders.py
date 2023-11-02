from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from data.OT_constants import UNIVERSITIES_ARRAY, COURSES_DICT, LANGUAGES_ARRAY, BOOL_DICT
from callbacks.OT_procedures import *

def languages_inline():
    
    builder = InlineKeyboardBuilder()
    
    for element in LANGUAGES_ARRAY:
        builder.add(InlineKeyboardButton(
        text=element,
        callback_data=element)
    )
        
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True)

def universities_inline():
    
    builder = InlineKeyboardBuilder()
    for element in UNIVERSITIES_ARRAY:
        builder.add(InlineKeyboardButton(
        text=element,
        callback_data=element)
    )
    
    builder.adjust(*[4] * 4)

    return builder.as_markup(resize_keyboard=True)

def courses_inline(university):
    
    univ_courses = get_courses_for_university(university)
    
    builder = InlineKeyboardBuilder()
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

def language_reply():
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in LANGUAGES_ARRAY]
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def universities_reply():
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in UNIVERSITIES_ARRAY]
    # builder.button(text="Cancel")
    builder.adjust(*[4] * 4)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def courses_reply(university):
    
    univ_courses = get_courses_for_university(university)
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in univ_courses]
    # builder.button(text="Cancel")
    builder.adjust(*[1] * 4)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def bool_reply(language):
    bool_array = BOOL_DICT.get(language)
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in bool_array]
    # builder.button(text="Cancel")
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


