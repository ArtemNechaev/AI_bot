
from typing import Text
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from io import BytesIO
from PIL import Image
from ai import detect


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


def register_vision(dp: Dispatcher):
    dp.register_message_handler(vision,content_types='photo')