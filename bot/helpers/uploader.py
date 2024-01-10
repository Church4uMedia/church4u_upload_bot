import asyncio

from ..google import Youtube
from ..translations import L10n
from ..config import Config

class Options:
    def __init__(
        self,
        title: str,
        description: str,
        tags: list,
        category: int,
        privacyStatus: str,
        selfDeclaredMadeForKids: bool,
        file: str
    ):
        self.title = title
        self.description = description
        self.tags = tags
        self.category = category
        self.privacyStatus = privacyStatus
        self.selfDeclaredMadeForKids = selfDeclaredMadeForKids
        self.file = file

class Uploader:
    def __init__(
        self,
        file: str,
        title: str,
        description: str = L10n.default_media_description,
        playlist: str = None
    ):
        self.options = Options(
            title=title,
            description=description,
            tags=self._get_tags(playlist),
            category=22,
            # privacyStatus="public",
            # selfDeclaredMadeForKids=False,
            privacyStatus="private",
            selfDeclaredMadeForKids=False,
            file=file
        )

    async def start_upload(self) -> str:
        youtube = Youtube(secret_file=Config.CLIENT_SECRET_FILE, token_file=Config.TOKEN_FILE)
        service = youtube.get_authenticated_service()
        response = await asyncio.get_running_loop().run_in_executor(
            None,
            youtube.initialize_upload,
            service,
            self.options
        )

        return response["id"]
    
    def _get_tags(self, playlist: str) -> [str]:
        tags = L10n.default_media_tags
        match playlist:
            case "decoration":
                tags.append("#decoration")
            case "craft":
                tags.append("#craft")
            case _:
                pass
        return tags