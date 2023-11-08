from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from keyboards import OT_inline
from data.OT_messages import (
    HELP_MESSAGE, BEGIN_MESSAGE, LANGUAGE_MESSAGE,
    UNIVERSITY_MESSAGES, COURSES_MESSAGES, COURSES_MESSAGES_BEGIN,
    COURSES_MESSAGES_WHY, COURSES_CANCEL
    )
from data.OT_constants import (
    LANGUAGES_DICT, UNIVERSITIES_DICT, COURSES_FULL_DICT
    )

from keyboards import OT_builders
from callbacks.OT_procedures import *
from aiogram.fsm.context import FSMContext
from utils.states import Form

router = Router()

@router.message(F.text.lower().in_(["hi", "hello", "привет"]))
async def greetings(message: Message):
    await message.reply("Hello mate! (MENU->START OR type <</start>>)")

@router.message(Command(commands=["help"]))
async def help(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, HELP_MESSAGE[0])
        
# @router.message(CommandStart(), IsAdmin(1490170564))
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.BEGIN)
    await message.answer(BEGIN_MESSAGE.get("all"), 
                         reply_markup=OT_inline.begin_markup)
    
@router.callback_query(F.data == "begin", Form.BEGIN)
async def language_choise(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.LANGUAGE)
    await callback.message.answer(LANGUAGE_MESSAGE.get("all"), 
                                  reply_markup=OT_builders.language_reply(),
                                  disable_notification=True)  
    
@router.message(Form.LANGUAGE)
async def univerersity_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(LANGUAGE=get_dict_key_from_value(message.text, LANGUAGES_DICT))
    await state.set_state(Form.UNIVERSITY)
    data = await state.get_data()
    await message.answer(UNIVERSITY_MESSAGES.get(data["LANGUAGE"]), 
                         reply_markup=OT_builders.universities_reply(),
                         disable_notification=True)
    
@router.message(Form.UNIVERSITY)
async def course_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(UNIVERSITY=message.text)
    await state.set_state(Form.COURSE)
    data = await state.get_data()
    await message.answer(COURSES_MESSAGES.get(data["LANGUAGE"]), 
                         reply_markup=OT_builders.courses_reply(message.text),
                         disable_notification=True)
    
@router.message(Form.COURSE)
async def course_handler_begin(message: Message, state: FSMContext) -> None:
    await state.update_data(COURSE=message.text)
    data = await state.get_data()
    await message.answer(COURSES_MESSAGES_BEGIN.get(data["LANGUAGE"]), 
                         reply_markup=OT_inline.begin_course_markup)
    
@router.callback_query(F.data == "begin_course", Form.COURSE)
async def course_handler_begin_callback(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await callback.message.answer(COURSES_MESSAGES_WHY.get(data["LANGUAGE"]), reply_markup=ReplyKeyboardRemove())      
    
    full_university = UNIVERSITIES_DICT.get(data["UNIVERSITY"])
    full_course = COURSES_FULL_DICT.get(data["COURSE"])
    aprove_text = f"Ai aplicat la cursul <b><u>{full_course}</u></b>  universitatea <b><u>{full_university}</u></b> ?" 
    await callback.message.answer(aprove_text, reply_markup=OT_builders.bool_reply(data["LANGUAGE"]))      

    await state.set_state(Form.CHOISE)
    await state.update_data(CHOISE=callback.message.text)
    data = await state.get_data()
    
@router.message(Form.CHOISE)
async def course_handler_start(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if (message.text == "No/Nu") or (message.text == "No"):
        await message.answer(COURSES_CANCEL.get(data["LANGUAGE"]))
        await state.clear()
    else:
        await message.answer(COURSES_MESSAGES_BEGIN.get(data["LANGUAGE"]), 
                         reply_markup=OT_inline.begin_course_markup)
     
    

    