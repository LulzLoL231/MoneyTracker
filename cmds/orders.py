# -*- coding: utf-8 -*-
#
#  MoneyTracker: cmds - Orders
#  Created by LulzLoL231 at 28/06/22
#
import json
import logging

from vkbottle.bot import Message
from vkbottle import BaseStateGroup, BotBlueprint
from vkbottle.dispatch.rules.base import FuncRule, StateRule

from config import cfg
from keyboards import Keyboards as keys
from database.main import Database, DB_LOCK


log = logging.getLogger('MoneyTracker')
bp = BotBlueprint('orders')


class AddOrder(BaseStateGroup):
    NAME = 'name'
    PRICE = 'price'
    AGENT = 'agent'
    VERIFY = 'verify'


@bp.on.private_message(payload={'command': 'orders'})
async def orders(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    async with DB_LOCK:
        orders = await Database.get_orders()
    inprog_orders = list(filter(
        (lambda o: not o.end_date),
        orders
    ))
    if not inprog_orders:
        cnt = 'Все заказы выполнены. Добавьте новый!'
    elif not orders:
        cnt = 'Заказы отсутствуют. Добавьте новый!'
    else:
        cnt = 'Текущие заказы:\n\n'
        cnt += '\n'.join([o.get_short_str() for o in inprog_orders])
    await msg.answer(cnt, keyboard=keys.orders(inprog_orders, bool(orders)))


@bp.on.private_message(payload={'command': 'add_order'})
async def start_add_order(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    await bp.state_dispenser.set(msg.peer_id, AddOrder.NAME)
    await msg.answer(
        'Добавление заказа\n\nВведите цель заказа.',
        keyboard=keys.back('orders')
    )


@bp.on.message(StateRule(AddOrder.NAME))
async def add_order_name(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    if msg.text.lower() == 'назад':
        await bp.state_dispenser.delete(msg.peer_id)
        log.info(f'User #{msg.peer_id} canceled adding order.')
        await orders(msg)
        return
    await bp.state_dispenser.set(msg.peer_id, AddOrder.PRICE, name=msg.text)
    await msg.answer(
        'Введите цену заказа.',
        keyboard=keys.back('orders')
    )


@bp.on.message(StateRule(AddOrder.PRICE))
async def add_order_price(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    if msg.text.lower() == 'назад':
        await bp.state_dispenser.delete(msg.peer_id)
        log.info(f'User #{msg.peer_id} canceled adding order.')
        await orders(msg)
        return
    elif not msg.text.isdigit():
        await msg.answer(
            'ОШИБКА: В качестве цены должно выступать цифровое значение!\nПовторите ввод.',
            keyboard=keys.back('orders')
        )
        return
    async with DB_LOCK:
        agents = Database.get_agents()
    if agents:
        await bp.state_dispenser.set(msg.peer_id, AddOrder.AGENT, price=int(msg.text))
        cnt = 'Выберите агента'
        key = keys.add_order_agents(agents)
    else:
        await bp.state_dispenser.delete(msg.peer_id)
        cnt = 'Нету доступных агентов. Сначала добавьте хотя-бы одного.'
        key = keys.back('start')
    await msg.answer(cnt, keyboard=key)
