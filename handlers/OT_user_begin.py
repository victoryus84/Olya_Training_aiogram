from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from keyboards import OT_inline
from data.OT_messages import WELCOME_MESSAGES, HELP_MESSAGE, BEGIN_MESSAGES
from data.OT_constants import user_data
from keyboards import OT_builders
# from handlers import user_data
from callbacks.OT_procedures import *

router = Router()

@router.message(F.text.lower().in_(["hi", "hello", "привет"]))
async def greetings(message: Message):
    await message.reply("Hello mate!")
    
# @router.message(CommandStart(), IsAdmin(1490170564))
@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    # await bot.send_message(message.chat.id, WELCOME_MESSAGES.get("ro"))
    await message.answer(WELCOME_MESSAGES.get("ro"), reply_markup=OT_inline.begin_markup)
    print(user_data)
    
@router.message(Command("help"))
async def help(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, HELP_MESSAGE[0])
  
@router.callback_query(F.data == "begin")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(BEGIN_MESSAGES.get("ro"), reply_markup=OT_builders.languages_inline())    
    
    