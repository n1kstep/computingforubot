from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Use commands /compute or /get."
    )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
