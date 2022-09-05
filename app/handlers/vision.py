
from typing import Text
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from io import BytesIO
from PIL import Image
from ai import detect_pipe


async def vision_start (instance, *args):
    if isinstance(instance , types.CallbackQuery):
        instance = instance.message

    await instance.answer("Send me a picture and I'll try to tell you what's on it")


async def vision(message: types.Message, ):
    image = BytesIO()
    await message.photo[-1].download(destination_file=image)
    is_loading = await message.answer('обработка...')

    image.seek(0)
    image = Image.open(image)
    image = detect_pipe(image)
    photo = types.InputFile(image)
    await is_loading.delete()
    await message.delete()
    await message.answer_photo(photo)


def register_vision_handler(dp: Dispatcher):
    dp.register_message_handler(vision_start, commands='vision')
    dp.register_callback_query_handler(vision_start, text='vision_start')
    dp.register_message_handler(vision, content_types='photo')
