import asyncio
import logging
import time
from typing import Tuple, Union

from pyrogram import filters as Filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from pyrogram import StopTransmission

from ..helpers.downloader import Downloader
from ..helpers.uploader import Uploader
from ..translations import L10n
from ..config import Config
from ..bot import Bot

log = logging.getLogger(__name__)

@Bot.on_message(
    Filters.chat([Config.UPLOAD_CHAT_ID])
    & Filters.incoming
    & Filters.command('upload')
    & Filters.user(Config.AUTH_USERS)
)
async def _upload_video(c: Bot, m: Message) -> None:
    await _upload(c, m, "")

@Bot.on_message(
    Filters.chat([Config.UPLOAD_CHAT_ID])
    & Filters.incoming
    & Filters.command('upload_decoration')
    & Filters.user(Config.AUTH_USERS)
)
async def _upload_decoration(c: Bot, m: Message) -> None:
    await _upload(c, m, "decoration")

@Bot.on_message(
    Filters.chat([Config.UPLOAD_CHAT_ID])
    & Filters.incoming
    & Filters.command('upload_craft')
    & Filters.user(Config.AUTH_USERS)
)
async def _upload_craft(c: Bot, m: Message) -> None:
    await _upload(c, m, "craft")

# Private

async def _upload(c: Bot, m: Message, playlist: str) -> None:
    media_message = m.reply_to_message

    if not media_message:
        await m.reply_text(L10n.not_a_reply_msg, True)
        return

    if not media_message.media:
        await m.reply_text(L10n.not_a_media_msg, True)
        return
    
    if not valid_media(media_message):
        await m.reply_text(L10n.not_a_valid_media_msg, True)
        return
    
    title = media_message.text
    if not title:
        await m.reply_text(L10n.not_a_title_msg, True)
        return

    # Handle

    status_message = await m.reply_text(L10n.processing, True)

    # Try to download

    await status_message.edit_text(L10n.downloading)

    try:
        downloaded_file = await Downloader(media_message, c, progress_callback).start_download()
        await status_message.edit_text(L10n.downloading_success)

    except Exception as e:
        await status_message.edit_text(
            text=L10n.downloading_failed.format(e),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Try to upload

    await status_message.edit_text(L10n.uploading)

    try:
        video_id = await Uploader(downloaded_file, title, playlist=playlist).start_upload()
        await status_message.edit_text(L10n.uploading_success.format(title, video_id), parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await status_message.edit_text(
            text=L10n.uploading_failed.format(e),
            parse_mode=ParseMode.MARKDOWN
        )
        return

def valid_media(message: Message) -> bool:
    if message.video:
        return True
    elif message.video_note:
        return True
    elif message.animation:
        return True
    elif message.document and "video" in message.document.mime_type:
        return True
    else:
        return False

async def progress_callback(
    current: int,
    total: int,
    start_time: float,
    operation_name: str,
    message: Message,
    c: Bot,
    download_id: str,
):
    if not c.download_controller.get(download_id):
        raise StopTransmission

    try:
        diff = int(time.time() - start_time)

        if (int(time.time()) % 5 == 0) or (current == total):
            await asyncio.sleep(1)

            speed, unit = human_bytes(current / diff, True)
            curr = human_bytes(current)
            tott = human_bytes(current)
            progress = round((current * 100) / total, 2)
            
            await message.edit_text(
                text=L10n.downloading_report.format(operation_name, progress, curr, tott, speed, unit),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(L10n.cancel_button, f"cncl+{download_id}")]]
                ),
            )

    except Exception as e:
        pass

def human_bytes(
    num: Union[int, float], split: bool = False
) -> Union[str, Tuple[int, str]]:
    base = 1024.0
    sufix_list = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    for unit in sufix_list:
        if abs(num) < base:
            if split:
                return round(num, 2), unit
            return f"{round(num, 2)} {unit}"
        num /= base