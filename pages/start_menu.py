from typing import Text
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from io import BytesIO
from PIL import Image
import requests
from ai import detect

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

async def start(message: types.Message):

    cv = InlineKeyboardButton('Сказать что на картинке!', callback_data='cv')
 

    kb = InlineKeyboardMarkup()
    kb.add(cv)
    
    await message.answer('Привет я бот. Вот что я могу:', reply_markup=kb)

async def cv (call: types.CallbackQuery):
    await call.message.answer("Отправь мне картинку, а я скажу что на ней")

async def vision(message: types.Message):
    image = BytesIO()
    await message.photo[-1].download(destination_file=image)
    is_loading = await message.answer('обработка...')

    image.seek(0)
    image = Image.open(image)
    image = detect(image)
    photo = types.InputFile(image)
    await is_loading.delete()
    await message.delete()
    await message.answer_photo(photo)

 

def register_start_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_callback_query_handler(cv)
    dp.register_message_handler(vision,content_types='photo')
