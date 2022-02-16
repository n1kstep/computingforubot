from uuid import uuid4

import wolframalpha
import logging
from aiogram import Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from aiogram.utils.markdown import link
from aiogram.utils.markdown import quote_html
from .. import dbworker


async def inline_handler(query: types.inline_query):
    inp = query.query[:-1]
    flag_comp = False
    wa_link = link('Full answer', f'https://www.wolframalpha.com/input/?i={inp}')

    filler_done = 'Done.'
    filler_wait = "Wait."
    filler_err = 'Not found.'

    state = filler_wait
    res = 'Nothing to show.'
    if len(inp) > 0 and query.query[-1] == "=":
        client = wolframalpha.Client('T7P64G-TTQ3LQ65GA')
        computed = client.query(inp)
        try:
            res = next(computed.results).text
            flag_comp = True
            state = filler_done
        except:
            state = filler_err

        dbworker.insert_or_update(user_id=query.from_user.id,
                                  inp_query=inp,
                                  suc=True,
                                  res=res
                                  )
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"Computing: {state}",
            input_message_content=InputTextMessageContent(
                "{} => *{}* {}...".format(inp, res, wa_link)
                if flag_comp
                else f'{res} {wa_link}...',
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            ),
            description=res,
            hide_url=True,
        )]

    await query.answer(results,
                       cache_time=60,
                       is_personal=True,
                       # switch_pm_text="Compute something... »»",
                       # switch_pm_parameter="add"
                       )


# Хэндлер для сбора статистики
async def chosen_handler(chosen_result: types.ChosenInlineResult):
    logging.info(f"Chosen query: {chosen_result.query}"
                 f"from user: {chosen_result.from_user.id}")


def register_inline_handlers(dp: Dispatcher):
    dp.register_inline_handler(inline_handler, state="*")
    dp.register_chosen_inline_handler(chosen_handler, state="*")
