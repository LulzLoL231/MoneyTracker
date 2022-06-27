# -*- coding: utf-8 -*-
#
#  MoneyTracker
#  Created by LulzLoL231 at 27/06/22
#
import logging

from vkbottle import Bot

from config import cfg
from cmds import labelers
from database.main import Database


log = logging.getLogger('MoneyTracker')
log.info(f'Loading v{cfg.VERSION}...')
bot = Bot(cfg.TOKEN)

for bl in labelers:
    bot.labeler.load(bl)

if __name__ == '__main__':
    bot.loop.create_task(Database._create_tables())
    bot.run_forever()
