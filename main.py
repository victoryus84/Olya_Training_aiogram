import asyncio
import logging
import sys
from aiogram import Dispatcher

from bot_instanse import bot
from handlers import OT_user_begin
from middlewares.antiflood import AntiFloodMiddleware
from data.OT_storage import SQLiteStorage

async def main() -> None:
    
    storage = SQLiteStorage()
    dp = Dispatcher()
    
    # dp.message.middleware(CheckSubscription())
    # dp.message.middleware(AntiFloodMiddleware(5))

    dp.include_routers(
        OT_user_begin.router,
        # OT_ARU_user_handlers.router,
    )

    # 
    try:
        await dp.start_polling(bot)
        await bot.delete_webhook(drop_pending_updates=True)
    finally:
        bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    asyncio.run(main())