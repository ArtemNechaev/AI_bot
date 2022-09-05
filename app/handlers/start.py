from typing import Text
from collections import deque
from aiogram import types, md
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


async def start(message: types.Message, state: FSMContext):

    async with state.proxy() as state_dict:
        text = 'Hello, how can i help you?'

        if not state_dict.get('context'):
            state_dict['context'] = deque([], maxlen=6)
            input = 'user1>>: ' + text
            state_dict['context'].append(input)

        await message.answer(text)

async def skills(message: types.Message, state: FSMContext):

    cv_button = InlineKeyboardButton("What's on image?", callback_data='vision_start')
    translate_button = InlineKeyboardButton('Translation eng-rus, rus-eng', callback_data='translate_start')

    kb = InlineKeyboardMarkup()
    kb.add(cv_button)
    kb.add(translate_button)
    
    await message.answer(md.text(md.bold("Here are some of my skills:")), reply_markup=kb, parse_mode='Markdown')
    await message.answer("Or we can just talk...")



def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(skills, commands='skills')

    
