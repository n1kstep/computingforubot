from aiogram import types
import wolframalpha
from data import config
from aiogram.dispatcher import FSMContext

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    # await message.answer(f"Эхо без состояния."
    #                      f"Сообщение:\n"
    #                      f"{message.text}")

    client = wolframalpha.Client(config.WA_TOKEN)
    res = client.query(message.text)

    await message.answer("{} => *{}*".format(message.text, next(res.results).text))


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
