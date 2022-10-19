# -*- coding: utf-8 -*-
#
#  MoneyTracker
#  Created by LulzLoL231 at 27/06/22
#
import logging

from vkbottle import Bot

from config import cfg
from cmds import blueprints
from database.main import db


log = logging.getLogger('MoneyTracker')
bot = Bot(cfg.token)


async def startup_task():
    log.info(f'Loading v{cfg.VERSION}...')
    for bp in blueprints:
        bp.load(bot)
    db._create_tables()
    await db.connect()


async def shutdown_task():
    log.info('Shutting down...')
    await db.disconnect()


bot.loop_wrapper.on_startup.append(startup_task())
bot.loop_wrapper.on_shutdown.append(shutdown_task())


if __name__ == '__main__':
    bot.run_forever()
