from aiogram import Bot, Dispatcher
from aiogram.methods.delete_webhook import DeleteWebhook
from src.handlers import router
from data.config import TOKEN
import asyncio
import logging
import sys



async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(token=TOKEN)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

