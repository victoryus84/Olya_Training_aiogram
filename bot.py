import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher

from handlers import OT_user_begin, OT_user_language, OT_user_university, OT_user_course
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
    bot = Bot(TOKEN)
    dp = Dispatcher()
    
    # dp.message.middleware(CheckSubscription())
    dp.message.middleware(AntiFloodMiddleware(5))

    dp.include_routers(
        OT_user_begin.router,
        OT_user_language.router,
        OT_user_university.router,
        OT_user_course.router,
        
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())