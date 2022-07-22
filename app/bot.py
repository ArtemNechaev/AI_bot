import logging

from aiogram import Bot, md, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook
import os
from subtasks import register_start_menu, register_vision, register_text2text_generation

from settings import TOKEN, WEBHOOK_HOST


WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings

WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.environ['PORT']


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
register_start_menu(dp)
register_vision(dp)
register_text2text_generation(dp)



async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    #start_webhook(
    #    dispatcher=dp,
    #    webhook_path=WEBHOOK_PATH,
    #    on_startup=on_startup,
    #    on_shutdown=on_shutdown,
    #    skip_updates=False,
    #    host=WEBAPP_HOST,
    #    port=WEBAPP_PORT,
    #)
