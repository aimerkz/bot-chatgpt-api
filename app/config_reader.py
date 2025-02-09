from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.enums import BotEnvEnum


class Settings(BaseSettings):
    bot_token: SecretStr = SecretStr('')
    api_key: SecretStr = SecretStr('')
    bot_env: BotEnvEnum = BotEnvEnum.DEV

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='forbid',
    )


config = Settings()
