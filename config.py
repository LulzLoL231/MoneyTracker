# -*- coding: utf-8 -*-
#
#  MoneyTracker - Settings
#  Created by LulzLoL231 at 27/06/22
#
import logging

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    VERSION: str = '0.3.1'
    DEBUG: bool = Field(False, env='BOT_DEBUG')
    TOKEN: str = Field(..., env='BOT_TOKEN')

    class Config:
        env_file = '.env'


cfg = Config()
logging.basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) >> %(module)s.%(funcName)s: %(message)s',
    level=logging.DEBUG if cfg.DEBUG else logging.INFO
)
