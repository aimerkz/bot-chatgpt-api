from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.enums import BotEnvEnum


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    bot_env: BotEnvEnum = BotEnvEnum.DEV
    admin_id: int
    debug_mode: bool = False

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: SecretStr

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_file_encoding='utf-8',
        extra='forbid',
    )

    @property
    def redis_dsn(self) -> str:
        password = self.redis_password.get_secret_value()
        return f'redis://:{password}@{self.redis_host}:{self.redis_port}/{self.redis_db}'


settings = Settings()  # type: ignore
