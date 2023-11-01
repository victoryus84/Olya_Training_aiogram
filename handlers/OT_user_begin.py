from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards import OT_inline
from data.OT_messages import HELP_MESSAGE, BEGIN_MESSAGE, LANGUAGE_MESSAGE
from data.OT_messages import UNIVERSITY_MESSAGES, COURSES_MESSAGES

from keyboards import OT_builders
from callbacks.OT_procedures import *
from aiogram.fsm.context import FSMContext
from utils.states import Form

router = Router()

@router.message(F.text.lower().in_(["hi", "hello", "привет"]))
async def greetings(message: Message):
    await message.reply("Hello mate!")

@router.message(Command(commands=["help"]))
async def help(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, HELP_MESSAGE[0])
        
# @router.message(CommandStart(), IsAdmin(1490170564))
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    print("start_handler")
    await state.set_state(Form.BEGIN)
    await message.answer(BEGIN_MESSAGE.get("ro"), reply_markup=OT_inline.begin_markup)
    
    
@router.callback_query(F.data == "begin")
async def language_choise(callback: CallbackQuery, state: FSMContext):
    print("language_choise")
    await callback.message.answer(LANGUAGE_MESSAGE.get("ro"), reply_markup=OT_builders.languages_inline())  
    
@router.message(Form.BEGIN)
async def univerersity_handler(message: Message, state: FSMContext) -> None:
    print("univerersity_handler")
    await state.update_data(name=message.text)
    await state.set_state(Form.UNIVERSITIES)
    print(f"univerersity_handler {message.text}")
    await message.answer(UNIVERSITY_MESSAGES.get("ro"), reply_markup=OT_builders.universities_inline())
    
# @router.callback_query(F.data == "begin")
# async def send_random_value(callback: CallbackQuery):
#     await callback.message.answer(COURSES_MESSAGES.get("ro"), reply_markup=OT_builders.courses_inline())      
    

    