# -*- coding: utf-8 -*-
#
#  MoneyTracker - Settings
#  Created by LulzLoL231 at 27/06/22
#
import logging
import platform

from pydantic import BaseSettings, Field


# Fixing .env file path for Docker.
if platform.system() == 'Linux':
    env_file = '/vk/.env'
else:
    env_file = './vk/.env'


class Config(BaseSettings):
    VERSION: str = '0.5.1'
    DEBUG: bool = Field(False, env='BOT_DEBUG')
    TOKEN: str = Field(..., env='BOT_TOKEN')

    class Config:
        env_file = env_file


cfg = Config()  # type: ignore
logging.basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) '
           '>> %(module)s.%(funcName)s: %(message)s',
    level=logging.DEBUG if cfg.DEBUG else logging.INFO
)
