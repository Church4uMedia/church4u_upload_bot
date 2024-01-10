import logging
import random
import string
import time

from typing import Optional
from pyrogram.types import Message
from pyrogram import StopTransmission

from ..translations import L10n
from ..bot import Bot

log = logging.getLogger(__name__)

class Cancelled(Exception):
    pass

class Downloader:
    def __init__(
        self,
        media_message: Message,
        client: Bot,
        progress_callback: callable = None,
        *args
    ):
        self.message = media_message
        self.client = client
        self.progress_callback = progress_callback
        self.args = args

        self.start_time: Optional[float] = None

        self.progress_callback: Optional[callable] = None
        self.args: Optional[tuple] = None

    async def start_download(self) -> str:
        self.start_time = time.time()

        download_id = self._get_download_id(self.client.download_controller)
        self.client.download_controller[download_id] = True

        downloaded_file = await self.message.download(progress=self._progress_callback)

        self.client.download_controller.pop(download_id)

        if not downloaded_file:
            raise StopTransmission
        
        return downloaded_file

    async def _progress_callback(self, current: int, total: int) -> None:
        if not self.progress_callback:
            return

        await self.progress_callback(current, total, self.start_time, L10n.downloading, *self.args)

    def _get_download_id(self, storage: dict) -> str:
        while True:
            download_id = "".join([random.choice(string.ascii_letters) for i in range(3)])
            if download_id not in storage:
                break

        return download_id