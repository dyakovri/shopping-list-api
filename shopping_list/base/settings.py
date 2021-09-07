import logging
from functools import lru_cache

from pydantic import BaseSettings
from pydantic.networks import PostgresDsn


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = None


@lru_cache()
def get_settings():
    settings = Settings()
    logging.info(settings)
    return settings
