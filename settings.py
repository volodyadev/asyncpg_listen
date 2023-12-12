from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_ECHO: bool = False

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgres",
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            path=f"/{self.DB_NAME}",
        )

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    DB_LISTENER_CHANNEL_GROUPS: str = "notify_channel"


settings = Settings()
