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
    await message.photo[0].download(destination_file=image)
    
    image = Image.open(image)
    #url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
    #image = Image.open(requests.get(url, stream=True).raw)
    image = detect(image)
    photo = types.InputFile(image)
    await message.delete()
    await message.answer_photo(photo)

 

def register_start_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_callback_query_handler(cv)
    dp.register_message_handler(vision,content_types=['photo', 'file'])
