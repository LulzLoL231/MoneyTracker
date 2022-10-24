# -*- coding: utf-8 -*-
#
#  MoneyTracker cmds: defaults.
#  Created by LulzLoL231 at 20/10/22
#
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from config import cfg, check_admin
from runtimes import log, bot
from database.main import db as Database
from keyboards import Keyboards as keys


@bot.message_handler(commands=['start'], state='*')
@check_admin()
async def start_bot(msg: types.Message, state: FSMContext, query=False):
    log.info(f'Called by {msg.chat.mention} ({msg.chat.id})')
    await state.finish()
    await types.ChatActions.typing()
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
    if query:
        await msg.edit_text(cnt, reply_markup=keys.start())
    else:
        await msg.answer(cnt, reply_markup=keys.start())


@bot.callback_query_handler(lambda q: q.data == 'start', state='*')
@check_admin()
async def query_start(query: types.CallbackQuery, state: FSMContext):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    await query.answer()
    await start_bot(query.message, state, True)


@bot.callback_query_handler(lambda q: q.data == 'about')
@check_admin()
async def query_about(query: types.CallbackQuery):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    cnt = 'MoneyTracker\nОтслеживаем оплату заказов.\n\n' \
          f'Автор: @LulzLoL231\nВерсия: {cfg.VERSION}'
    await query.answer(cnt, True)


@bot.message_handler(commands=['about'])
@check_admin()
async def about(msg: types.Message):
    log.info(f'Called by {msg.chat.mention} ({msg.chat.id})')
    cnt = 'MoneyTracker\nОтслеживаем оплату заказов.\n\n' \
        f'Автор: @LulzLoL231\nВерсия: {cfg.VERSION}'
    await msg.answer(cnt, reply_markup=keys.back_btn())
