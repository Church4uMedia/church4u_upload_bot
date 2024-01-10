from pyrogram import filters as Filters
from pyrogram.types import CallbackQuery

from ..translations import L10n
from ..bot import Bot

@Bot.on_callback_query(
    Filters.create(lambda _, __, query: query.data.startswith("cncl+"))
)
async def cncl(c: Bot, q: CallbackQuery) -> None:
    _, pid = q.data.split("+")
    if not c.download_controller.get(pid, False):
        await q.answer(L10n.cancel_process_is_not_active, show_alert=True)
    else:
        c.download_controller[pid] = False
        await q.answer(L10n.cancel_will_be_cancelled, show_alert=True)
