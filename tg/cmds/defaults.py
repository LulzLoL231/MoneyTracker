# -*- coding: utf-8 -*-
#
#  MoneyTracker cmds: defaults.
#  Created by LulzLoL231 at 20/10/22
#
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from config import cfg
from runtimes import log, bot
from database.main import db as Database
from keyboards import Keyboards as keys


log.info('Cmds "defaults" loaded!')


@bot.message_handler(commands=['/start'])
async def start_bot(msg: types.Message):
    log.info(f'Called by {msg.chat.mention} ({msg.chat.id})')
    # await state.finish()
    if msg.chat.id == cfg.admin_id:
        orders = await Database.get_orders()
        cnt = f'Привет {msg.chat.first_name}!\n\n'
        if orders:
            cnt += 'Текущие заказы:\n'
            full_price = 0
            for ord in filter((lambda o: not o.end_date), orders):
                cnt += f'{ord.get_short_str()}\n'
                full_price += ord.price
            cnt += f'\nИтого: {full_price} руб.'
        else:
            cnt += 'Все заказы выполнены.'
        await msg.answer(cnt, reply_markup=keys.start())
    else:
        log.warning(
            f'Unknown user {msg.chat.mention} ({msg.chat.id}) '
            'trying get access to bot.'
        )
        await msg.answer('<code>В доступе отказано.</code>')


@bot.callback_query_handler(lambda q: q.data == 'about')
async def about(query: types.CallbackQuery):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    cnt = 'MoneyTracker\nОтслеживаем оплату заказов.\n\n' \
          f'Автор: @LulzLoL231\nВерсия: {cfg.VERSION}'
    await query.answer(cnt, True)
