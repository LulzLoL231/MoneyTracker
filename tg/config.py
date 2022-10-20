# -*- coding: utf-8 -*-
#
#  MoneyTracker - Settings
#  Created by LulzLoL231 at 20/10/22
#
import logging
import platform

from pydantic import BaseSettings, Field, PostgresDsn


# Fixing .env file path for Docker.
if platform.system() == 'Linux':
    env_file = '/tg/.env'
else:
    env_file = '.env'


class Config(BaseSettings):
    VERSION: str = '0.1'
    DEBUG: bool = Field(False, env='BOT_DEBUG')
    admin_id: int = Field(265300852, env='BOT_ADMINID')
    token: str = Field(..., env='BOT_TOKEN')
    postgres_dsn: PostgresDsn = Field(..., env='BOT_POSTGRESDSN')

    class Config:
        env_file = env_file


cfg = Config()  # type: ignore
logging.basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) '
           '>> %(module)s.%(funcName)s: %(message)s',
    level=logging.DEBUG if cfg.DEBUG else logging.INFO
)
