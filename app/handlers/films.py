
from typing import Text
from aiogram import types, md
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from bs4 import BeautifulSoup
import requests

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
           "Accept-Language": "en-EN,en;q=0.9,en-US;q=0.8,en;q=0.7"}

url = "https://www.google.com/search?q=What+to+watch&lr=lang_en"


async def what2watch(message: types.Message, *args):
    resp = requests.get(url, headers=headers)
    root = BeautifulSoup(resp.content, "html.parser")
    films = [root.find('div', attrs={'data-cindex': '0', 'data-index': str(i)}).get('data-ttl')
             for i in range(1, 6)]
    films = [md.text(f) for f in films]

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Information provided by google', url=url))

    await message.reply(
        md.text(
            md.bold('Here are some popular movies and shows:'),
            *films,
            sep='\n'
        ),
        parse_mode='Markdown', reply_markup=kb)

    
