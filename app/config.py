from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ACCESS_TOKEN_EXPIRATION: int = 60 * 60  # permenit
    REFRESH_TOKEN_EXPIRATION: int   # 24 jam
    VERIFICATION_EXPIRATION: int = 1

    # EMAIL: EmailStr
    # PASSWORD: str
    # SECRET: str

    PRIVATEKEY: str
    PUBLICKEY: str
    REFRESHPRIVATEKEY: str

    DB: str
    DB_POOL_SIZE: int = 20
    DB_POOL_PRE_PING: bool = True
    DB_POOL_RECYCLE: int = 1800
    DB_ECHO: int = False

    wh_key: str
    class Config:
        env_file = '.env'


@lru_cache
def get_config():
    return Config()  # type: ignore


config = get_config()
