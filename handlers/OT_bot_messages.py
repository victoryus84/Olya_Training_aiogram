from aiogram import Router, F
from aiogram.types import Message

from keyboards import reply, inline, builders, fabrics, OT_reply, OT_inline, OT_builders
from data.OT_subloader import get_json
from data.OT_constants import LANGUAGES_ARRAY, LANGUAGES_DICT, UNIVERSITIES_ARRAY, COURSES
from data.OT_messages import BEGIN_MESSAGES, UNIVERSITIES_MESSAGES, COURSES_MESSAGES
from callbacks.OT_procedures import get_dict_key_from_value

router = Router()
user_data = {}

@router.message(F.text.lower().in_(["хай", "хелоу", "привет"]))
async def greetings(message: Message):
    await message.reply("Привееееть!")


@router.message()
async def echo(message: Message):
    
    # msg = message.text.lower()
    msg = message.text
    
    user_choises = await get_json("OT_user_choises.json")
    
    print(f"{msg}")
    if msg == "begin":
        await message.answer(BEGIN_MESSAGES.get("ro"), reply_markup=OT_reply.language_markup)
    elif msg in LANGUAGES_ARRAY:
        selected_language = get_dict_key_from_value(msg, LANGUAGES_DICT)
        await message.answer(UNIVERSITIES_MESSAGES.get(selected_language), reply_markup=OT_builders.universities())    
        user_data["language"] = selected_language
    elif msg in UNIVERSITIES_ARRAY:
        selected_university = msg
        user_data["university"] = selected_university
        print(user_data)
        await message.answer(COURSES_MESSAGES.get(user_data["language"]), reply_markup=OT_builders.courses(selected_university))
    elif msg in COURSES.get(user_data["university"]): 
        selected_course = msg
        
        user_data["course"] = selected_course  
    else:
        await message.answer("Bye, bye!")  
    # if msg == "ссылки":
    #     await message.answer("Вот ваши ссылки:", reply_markup=inline.links)
    # elif msg == "спец. кнопки":
    #     await message.answer("Спец. кнопки:", reply_markup=reply.spec)
    # elif msg == "калькулятор":
    #     await message.answer("Введите выражение:", reply_markup=builders.calc())
    # elif msg == "смайлики":
    #     await message.answer(f"{smiles[0][0]} <b>{smiles[0][1]}</b>", reply_markup=fabrics.paginator())
    # elif msg == "назад":
    #     await message.answer("Вы перешли в главное меню!", reply_markup=reply.main)