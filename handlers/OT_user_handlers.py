from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from keyboards import OT_builders
from data.OT_constants import LANGUAGES_ARRAY, LANGUAGES_DICT, UNIVERSITIES_ARRAY, COURSES
from data.OT_messages import UNIVERSITY_MESSAGES, COURSES_MESSAGES
from aiogram.fsm.context import FSMContext
from utils.states import Form
router = Router()

# @router.message()
# async def echo(message: Message):
    
#     # msg = message.text.lower()
#     msg = message.text
    
#     user_choises = await get_json("OT_user_choises.json")
    
#     print(f"{msg}")
#     if msg in LANGUAGES_ARRAY:
#         selected_language = get_dict_key_from_value(msg, LANGUAGES_DICT)
#         await message.answer(UNIVERSITIES_MESSAGES.get(selected_language), reply_markup=OT_builders.universities())    
#         user_data["language"] = selected_language
#     elif msg in UNIVERSITIES_ARRAY:
#         selected_university = msg
#         user_data["university"] = selected_university
#         print(user_data)
#         await message.answer(COURSES_MESSAGES.get(user_data["language"]), reply_markup=OT_builders.courses(selected_university))
#     elif msg in COURSES.get(user_data["university"]): 
#         selected_course = msg
        
#         user_data["course"] = selected_course  
#     else:
#         await message.answer("Bye, bye!")         
        
        
            
 
    
    