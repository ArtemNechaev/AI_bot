from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton

from ai import translate_pipe

class TranslateMode(StatesGroup):
    text = State()

async def translate_start(instance, state:FSMContext):
    if isinstance(instance , types.CallbackQuery):
        instance = instance.message

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('cancel')

    await TranslateMode.text.set()
    await instance.answer("Send me a text. I'll transalate it", reply_markup=kb)

async def translate_text(message: types.Message, state: FSMContext):
    answ = translate_pipe(message.text)
    await message.answer(answ)

async def translate_last_message(message: types.Message, state: FSMContext):
    async with state.proxy() as state_dict:
        last_message = state_dict['context'][-1].replace("user2>>: ","")
    answ = translate_pipe(last_message)
    await message.answer(answ)


async def exit_translate_mode(message: types.Message, state: FSMContext):

    await state.finish()
    await message.reply('Translation mode disabled', reply_markup=ReplyKeyboardRemove())

def register_translate_handler(dp: Dispatcher):

    dp.register_message_handler(translate_start, commands='translate', state='*')
    dp.register_callback_query_handler(translate_start, text='translate_start', state='*')
    dp.register_message_handler(exit_translate_mode, Text(equals='cancel') , state=TranslateMode.text)
    dp.register_message_handler(translate_text,  state=TranslateMode.text)
    
