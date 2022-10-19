# -*- coding: utf-8 -*-
#
#  MoneyTracker - Settings
#  Created by LulzLoL231 at 27/06/22
#
import logging
import platform

from pydantic import BaseSettings, Field, PostgresDsn


# Fixing .env file path for Docker.
if platform.system() == 'Linux':
    env_file = '/vk/.env'
else:
    env_file = '.env'


class Config(BaseSettings):
    VERSION: str = '1.0'
    DEBUG: bool = Field(False, env='BOT_DEBUG')
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
