import logging
import tarfile

import requests
from aiogram import Bot, md, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook
import os
from handlers import register_start_handler, register_vision_handler, register_text2text_handler, register_translate_handler

from settings import TOKEN, WEBHOOK_HOST, IS_PROD


WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings

WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.environ['PORT']


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

register_start_handler(dp)
register_vision_handler(dp)
register_translate_handler(dp)
register_text2text_handler(dp)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    if IS_PROD:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=False,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp, skip_updates=True)
