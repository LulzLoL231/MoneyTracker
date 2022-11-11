# -*- coding: utf-8 -*-
#
#  MoneyTracker: cmds - Defaults
#  Created by LulzLoL231 at 27/06/22
#
import logging

from vkbottle.bot import BotBlueprint, Message
from vkbottle.dispatch.rules.base import FuncRule

from config import cfg
from keyboards import Keyboards as keys
from database.main import db as Database


log = logging.getLogger('MoneyTracker')
bp = BotBlueprint('defaults')


@bp.on.message(FuncRule(lambda m: m.text.lower() in ['/start', 'начать']))
@bp.on.message(payload={'command': 'start'})
async def start_bot(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    orders = await Database.get_inprogress_orders()
    cnt = f'Привет {user.first_name}!\n\n'
    if orders:
        cnt += 'Текущие заказы:\n'
        full_price = 0
        for ord in orders:
            cnt += f'{ord.get_short_str()}\n'
            full_price += ord.price
        cnt += f'\nИтого: {full_price} руб.'
    else:
        cnt += 'Все заказы выполнены.'
    await msg.answer(cnt, keyboard=keys.start())


@bp.on.message(payload={'command': 'about'})
async def about_bot(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    cnt = f'MoneyTracker\nОтслеживаем оплату заказов.\n\n' \
          f'Создатель: @0x403\nВерсия: {cfg.VERSION}'
    await msg.answer(cnt, keyboard=keys.start())
