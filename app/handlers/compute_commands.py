import wolframalpha
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from .. import dbworker


class Computation(StatesGroup):
    compute_input = State()
    print_computed = State()


async def ask_to_compute(message: types.Message):
    await message.answer(
        "Input the expression to compute..."
    )
    await Computation.compute_input.set()


async def make_computation(message: types.Message, state: FSMContext):
    inp = message.text
    flag_comp = False

    computed = "Nothing to compute."
    if len(inp) > 0:
        try:
            client = wolframalpha.Client('T7P64G-TTQ3LQ65GA')
            computed = client.query(inp)
            flag_comp = True
            dbworker.insert_or_update(message.from_user.id,
                                      inp,
                                      True,
                                      next(computed.results).text
                                      )
        except:
            pass

    await state.update_data(yt_hash=True)
    await message.answer(next(computed.results).text
                         if flag_comp else computed,
                         # parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True,
                         )
    await Computation.print_computed.set()


async def get_last_queries(message: types.Message):
    await message.answer(dbworker.get_queries(message.from_user.id))


def register_add_links_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_to_compute, commands="compute", state="*")
    dp.register_message_handler(make_computation, state=Computation.compute_input)
    dp.register_message_handler(get_last_queries, commands="get", state="*")
