from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import enums

from ..translations import L10n
from ..config import Config
from ..bot import Bot

@Bot.on_message(
    Filters.chat([Config.UPLOAD_CHAT_ID])
    & Filters.incoming
    & Filters.command("start")
    & Filters.user(Config.AUTH_USERS)
)
async def _start(c: Bot, m: Message):
    await m.reply_chat_action(enums.ChatAction.TYPING)

    await m.reply_text(
        text=L10n.start_message.format(m.from_user.first_name),
        quote=True
    )
