from pyrogram import Client

from .config import Config

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=Config.CLIENT_NAME,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            in_memory=True,
            workers=6,
            plugins=dict(root="bot.plugins"),
        )
        self.DOWNLOAD_WORKERS = 6
        self.download_controller = {}
