import random
from typing import Any

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from keyboards import reply, OT_reply, OT_inline

from filters.is_admin import IsAdmin
from filters.is_digit_or_float import CheckForDigit

from data.OT_messages import WELCOME_MESSAGES, BEGIN_MESSAGES

router = Router()


# @router.message(CommandStart(), IsAdmin(1490170564))
@router.message(CommandStart())
async def start(message: Message, bot: Bot) -> None:
    # await bot.send_message(message.chat.id, WELCOME_MESSAGES.get("ro"))
    await message.answer(WELCOME_MESSAGES.get("ro"), reply_markup=OT_inline.begin_markup)
    
@router.message(Command("pay"), CheckForDigit()) # /pay 1234
async def pay_the_order(message: Message, command: CommandObject) -> None:
    await message.answer("Вы успешно оплатили товар!")


@router.message(Command(commands=["rn", "random-number"])) # /rn 1-100
async def get_random_number(message: Message, command: CommandObject) -> None:
    a, b = [int(n) for n in command.args.split("-")]
    rnum = random.randint(a, b)

    await message.reply(f"Random number: {rnum}")


@router.message(Command("test"))
async def test(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, "test")