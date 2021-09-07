from pydantic import BaseSettings
from pydantic.networks import PostgresDsn

class Settings(BaseSettings):
    DB_DSN: PostgresDsn = None
