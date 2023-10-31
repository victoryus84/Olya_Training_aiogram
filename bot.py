import asyncio
from aiogram import Bot, Dispatcher

from handlers import OT_bot_messages, OT_user_commands
from callbacks import pagination

from middlewares.check_sub import CheckSubscription
from middlewares.antiflood import AntiFloodMiddleware
# Load .env
import os
from dotenv import load_dotenv
load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv('BOTTOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

async def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # dp.message.middleware(CheckSubscription())
    # dp.message.middleware(AntiFloodMiddleware(5))

    dp.include_routers(
        OT_user_commands.router,
        OT_bot_messages.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())