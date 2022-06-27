# -*- coding: utf-8 -*-
#
#  MoneyTracker: cmds - Defaults
#  Created by LulzLoL231 at 27/06/22
#
import logging

from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import FuncRule

from config import cfg
from database.main import Database, DB_LOCK


log = logging.getLogger('MoneyTracker')
bl = BotLabeler()


@bl.message(FuncRule(lambda m: m.text.lower() in ['/start', 'начать']))
@bl.message(payload={'command': 'start'})
async def start_bot(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    async with DB_LOCK:
        orders = await Database.get_orders()
    cnt = f'Привет {user.first_name}!\n\n'
    if orders:
        cnt += 'Текущие заказы:\n'
        for ord in filter((lambda o: o.end_date), orders):
            cnt += f'{ord.get_short_str()}\n'
    else:
        cnt += 'Все заказы выполнены.'
    await msg.answer(cnt)


@bl.message(FuncRule(lambda m: m.text.lower() in ['/about', 'о боте']))
@bl.message(payload={'command': 'about'})
async def about_bot(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    cnt = f'MoneyTracker\nОтслеживаем оплату заказов.\n\nСоздатель: @0x403\nВерсия: {cfg.VERSION}'
    await msg.answer(cnt)
