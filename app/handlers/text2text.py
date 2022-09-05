from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from ai import dialog_pipe, translate_pipe
from collections import deque

from .translate import translate_start, translate_last_message
from .vision import vision_start
from .start import skills
from .films import what2watch

commands = [skills, translate_start, vision_start,
            what2watch, translate_last_message]


async def text2text_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as state_dict:

        text = message.text

        if not state_dict.get('context'):
            state_dict['context'] = deque([], maxlen=6)
            state_dict['keywords'] = deque([], maxlen=3)

        input = 'user1>>: ' + text
        state_dict['context'].append(input)

        keyword = None
        if len(set(state_dict['keywords'])) == 1 and state_dict['keywords'][-1] != 'no_keywords' and len(state_dict['keywords']) == 3:
            keyword = 'no_keywords'

        answ = dialog_pipe(state_dict['context'], text, keyword)

        if isinstance(answ, int):
            await commands[answ](message, state)
            return
        else:
            answ, keyword = answ
            state_dict['context'].append('user2>>: ' + answ)
            state_dict['keywords'].append(keyword)

        if answ.lower() in ['hello', 'hi']:
            answ = answ +f', {message.from_user.first_name}'

        await message.answer(answ)


def register_text2text_handler(dp: Dispatcher):
    dp.register_message_handler(text2text_handler, state='*')
