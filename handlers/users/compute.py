import wolframalpha
from aiogram import types

from data import config
from loader import dp


@dp.message_handler(state=None)
async def bot_start(message: types.Message):
    client = wolframalpha.Client(config.WA_TOKEN)
    res = client.query(message.text)

    await message.answer("{} => *{}*".format(message.text, next(res.results).text))
