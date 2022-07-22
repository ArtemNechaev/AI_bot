from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from ai import sec2sec


async def text2text_generation(message: types.Message, state: FSMContext):
    async with state.proxy() as state_dict:

        mode = state_dict.get('mode', 'translate')
        text = message.text
        if mode == 'dialog':
            state_dict['context'].append(f'user1>>: {text}')
            answer, native_ln_answer = sec2sec(
                " ".join(state_dict['context']), mode)
            last_answer = state_dict['context'][-2] if len(state_dict['context']) > 1 else ''
            if 'sorry' in native_ln_answer or  last_answer == f'user2>>: {native_ln_answer}':
                state_dict['context'].clear()
            else:
                state_dict['context'].append(f'user2>>: {native_ln_answer}')
        else:
            answer = sec2sec(text, mode)

        await message.answer(answer)


def register_text2text_generation(dp: Dispatcher):
    dp.register_message_handler(text2text_generation, state='*')
