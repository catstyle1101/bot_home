from typing import Any

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class HostBaseAuth(BaseModel):
    HOST: str = "http://somehosthere"
    LOGIN: str
    PASSWORD: str


class Webhook(BaseModel):
    PATH: str = "/webhook"
    SSL_CERT: str = "./certs/YOURPUBLIC.pem"
    SSL_PRIV: str = "./certs/YOURPRIVATE.key"
    SECRET: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    TRANSMISSION: HostBaseAuth
    QBITTORRENT: HostBaseAuth
    RUTRACKER: HostBaseAuth
    WEBHOOK: Webhook
    DEBUG: bool = False

    BOT_TOKEN: str
    DOMAIN: str
    FREEDOMIST_TOKEN: str
    ADMINS: str | int | set[int] = ""
    ADMIN_LIST: set[int] = set()
    TORRENT_API: str = "https://api.exfreedomist.com"

    WEB_SERVER_HOST: str = "bot"
    WEB_SERVER_PORT: int = 8080
    SHOW_TORRENTS_PAGE_SIZE: int = 10
    FIND_TORRENTS_LIMIT: int = 15
    FIND_TORRENTS_TRACKERS: list[str] = ["rutracker"]

    def model_post_init(self, __context: Any) -> None:
        if isinstance(self.ADMINS, str):
            self.ADMIN_LIST = set(int(i) for i in self.ADMINS.strip().split(","))
        elif isinstance(self.ADMINS, int):
            self.ADMIN_LIST = {self.ADMINS}
        elif isinstance(self.ADMINS, set):
            self.ADMIN_LIST = self.ADMINS

    def user_is_admin(self, user_id: int | str) -> bool:
        return int(user_id) in set(int(i) for i in self.ADMIN_LIST)


settings = Settings()  # type: ignore

if __name__ == "__main__":
    print(settings)
