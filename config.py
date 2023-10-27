from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN_MANHATTAN: str
    ADMINS: str

    class Config:
        env_file = ".env"

    @property
    def ALLOWED_USERS(self):
        return [int(i) for i in self.ADMINS.split(',')]

    @property
    def SPECIAL_USER(self):
        return self.ALLOWED_USERS[1]

settings = Settings()
