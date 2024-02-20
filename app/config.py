from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    BOT_TOKEN: str
    WEBHOOK_SECRET: str
    DOMAIN: str
    TRANSMISSION_LOGIN: str
    TRANSMISSION_PASSWORD: str
    TRANSMISSION_HOST: str
    ADMINS: str | int | set[int] = ""

    WEB_SERVER_HOST: str = "bot"
    WEB_SERVER_PORT: int = 8080
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_SSL_CERT: str = "./certs/YOURPUBLIC.pem"
    WEBHOOK_SSL_PRIV: str = "./certs/YOURPRIVATE.key"
    PAGE_SIZE: int = 10

    def model_post_init(self, __context: Any) -> None:
        if isinstance(self.ADMINS, str):
            self.ADMINS = set(int(i) for i in self.ADMINS.strip().split(","))
        elif isinstance(self.ADMINS, int):
            self.ADMINS = {self.ADMINS}


    def user_is_admin(self, user_id: int | str) -> bool:
        return int(user_id) in  set(
            int(i) for i in self.ADMINS)


settings = Settings()

if __name__ == "__main__":
    print(settings)
