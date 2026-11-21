import asyncio
from aiogram import Bot, Dispatcher
from config import get_bot_token
from db import Database
from handlers import (
    common_router,
    domains_router,
    fun_text_router,
    media_router,
    stats_router,
)


async def main():
    token = get_bot_token()
    bot = Bot(token=token)
    dp = Dispatcher()

    db = Database()
    dp["db"] = db

    dp.include_router(common_router)
    dp.include_router(domains_router)
    dp.include_router(fun_text_router)
    dp.include_router(media_router)
    dp.include_router(stats_router)

    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
