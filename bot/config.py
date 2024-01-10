import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    CLIENT_NAME = os.getenv("CLIENT_NAME")
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    UPLOAD_CHAT_ID = int(os.getenv("UPLOAD_CHAT_ID"))

    BOT_OWNER = int(os.getenv("BOT_OWNER"))

    AUTH_USERS = [BOT_OWNER]

    CLIENT_SECRET_FILE = "client_secret.json"
    TOKEN_FILE = "token.json"

    DEBUG = bool(os.getenv("DEBUG"))