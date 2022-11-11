# -*- coding: utf-8 -*-
#
#  MoneyTracker - Settings
#  Created by LulzLoL231 at 20/10/22
#
import logging
import platform
from functools import wraps

from aiogram import types
from pydantic import BaseSettings, Field, PostgresDsn


# Fixing .env file path for Docker.
if platform.system() == 'Linux':
    env_file = '/tg/.env'
else:
    env_file = '.env'


class Config(BaseSettings):
    VERSION: str = '0.3.1'
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
__seclog = logging.getLogger('moneytracker.check_admin')


def check_admin():
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            if isinstance(args[0], types.CallbackQuery):
                msg = args[0].message
            elif isinstance(args[0], types.Message):
                msg = args[0]
            else:
                __seclog.error(
                    f'Unknown event type: {args[0]}!'
                )
                return
            if msg.chat.id == cfg.admin_id:
                __seclog.debug(
                    f'User {msg.chat.mention} ({msg.chat.id}) '
                    'is authenticated!'
                )
                return await func(*args, **kwargs)
            else:
                __seclog.warning(
                    f'Unknown user {msg.chat.mention} ({msg.chat.id}) '
                    'trying get access to bot!'
                )
                if msg.from_user.is_bot:
                    await msg.delete()
                await msg.answer('<b>В доступе отказано!</b>')
        return wrapped
    return wrapper
