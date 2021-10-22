import logging
from functools import lru_cache

from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl, PostgresDsn


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = None
    OPENAPI_PREFIX: str = ''
    SHARE_LINK_TEMPLATE: AnyHttpUrl = 'https://shopping.dyakov.space/{share_id}'
    SHARE_QR_LINK_TEMPLATE: AnyHttpUrl = (
        'https://api.qrserver.com/v1/create-qr-code/?data=https://shopping.dyakov.space/{share_id}'
    )


@lru_cache()
def get_settings():
    settings = Settings()
    logging.info(settings)
    return settings
