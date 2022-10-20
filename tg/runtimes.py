# -*- coding: utf-8 -*-
#
#  MoneyTracker
#  Created by LulzLoL231 at 20/10/22
#
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import cfg
from database.main import db


log = logging.getLogger('MoneyTracker')
bot = Dispatcher(Bot(cfg.token, parse_mode='HTML'), storage=MemoryStorage())
exec = executor.Executor(bot)
privateChatCmds = [
    BotCommand('/start', 'Запустить бота'),
    BotCommand('/add_order', 'Добавить новый заказ'),
    BotCommand('/about', 'О боте.')
]


async def startup_task(dp: Dispatcher):
    log.info(f'Loading v{cfg.VERSION}...')
    db._create_tables()
    await db.connect()
    await dp.bot.set_my_commands(
        privateChatCmds, BotCommandScopeAllPrivateChats()
    )


async def shutdown_task(_):
    log.info('Shutting down...')
    await db.disconnect()


exec.on_startup(startup_task)
exec.on_shutdown(shutdown_task)
