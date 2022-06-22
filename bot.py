from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os
from dotenv import load_dotenv


from pages.start_menu import register_start_menu

if not os.environ.get('BOT_TOKEN'):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

TOKEN=os.environ['BOT_TOKEN']


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
register_start_menu(dp)

if __name__ == '__main__':
    executor.start_polling(dp)