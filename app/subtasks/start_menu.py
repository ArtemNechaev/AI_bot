from email import message
from fnmatch import translate
from typing import Text
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from matplotlib.pyplot import text
from collections import deque



async def start(message: types.Message):

    cv_button = InlineKeyboardButton('Сказать что на картинке!', callback_data='cv')
    dialog_button = InlineKeyboardButton('Поддержать диалог', callback_data='dialog')
    translate_button = InlineKeyboardButton('Перевести текст с русского на английский или наоборот', callback_data='translate')


    kb = InlineKeyboardMarkup()
    kb.add(cv_button)
    kb.add(dialog_button)
    kb.add(translate_button)
    
    await message.answer('Привет я бот.\nВот что я могу:', reply_markup=kb)

async def cv (instance):
    if isinstance(instance , types.CallbackQuery):
        instance = instance.message

    assert(isinstance(instance , types.Message))
    await instance.answer("Отправь мне картинку, а я скажу что на ней")

async def dialog(instance, state: FSMContext ):
    if isinstance(instance , types.CallbackQuery):
        instance = instance.message
    assert(isinstance(instance , types.Message))

    async with state.proxy() as state_dict:
        state_dict['mode']='dialog'
        state_dict['context'] = deque([], maxlen=6)
    
    await instance.answer("Включен режим диалога")

async def translate(instance, state: FSMContext):
    if isinstance(instance , types.CallbackQuery):
        instance = instance.message
    assert(isinstance(instance , types.Message))
    
    async with state.proxy() as state_dict:
        state_dict['mode']='translate'

    await instance.answer("Переведу все, что ты напишешь")


def register_start_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(cv, commands='vision')
    dp.register_message_handler(dialog, commands='dialog', state='*')
    dp.register_message_handler(translate, commands='translate', state='*')
    dp.register_callback_query_handler(cv, text='cv')
    dp.register_callback_query_handler(dialog, text='dialog', state='*')
    dp.register_callback_query_handler(translate, text='translate', state='*')
    
