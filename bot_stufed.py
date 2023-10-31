import asyncio
from aiogram import Bot, Dispatcher

from handlers import bot_messages, user_commands, questionaire
from callbacks import pagination

from middlewares.check_sub import CheckSubscription
from middlewares.antiflood import AntiFloodMiddleware

from config_reader import config


async def main() -> None:
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    dp.message.middleware(CheckSubscription())
    dp.message.middleware(AntiFloodMiddleware(5))

    dp.include_routers(
        user_commands.router,
        pagination.router,
        questionaire.router,
        bot_messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())