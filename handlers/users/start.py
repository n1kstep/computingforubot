from aiogram import types

from loader import dp


@dp.message_handler(commands='compute')
async def bot_start(message: types.Message):

    await message.answer(f"Привет, {message.from_user.full_name}!")
