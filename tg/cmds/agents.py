# -*- coding: utf-8 -*-
#
#  MoneyTracker cmds: defaults.
#  Created by LulzLoL231 at 20/10/22
#
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import cfg, check_admin
from runtimes import log, bot
from database.main import db as Database
from keyboards import Keyboards as keys


class AddAgent(StatesGroup):
    NAME = State()


@bot.callback_query_handler(lambda q: q.data == 'agents', state='*')
@check_admin()
async def agents(query: types.CallbackQuery, state: FSMContext):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    if state:
        await state.finish()
    agents = await Database.get_agents()
    if agents:
        cnt = 'Список агентов:\n\n'
        cnt += '\n'.join([f'#{a.uid} - {a.name}' for a in agents])
    else:
        cnt = 'Агенты отсутствуют. Добавьте нового!'
    await query.answer()
    await query.message.edit_text(cnt, reply_markup=keys.inline_agents())


@bot.callback_query_handler(lambda q: q.data == 'add_agent')
@check_admin()
async def add_agent(query: types.CallbackQuery):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    await AddAgent.NAME.set()
    await query.answer()
    await query.message.edit_text(
        'Добавление нового агента.\n\nОтправьте имя агента.',
        reply_markup=keys.back('agents', 'Отмена')
    )


@bot.message_handler(
    content_types=types.ContentTypes.TEXT, state=AddAgent.NAME
)
@check_admin()
async def add_agent_finish(msg: types.Message, state: FSMContext):
    log.info(f'Called by {msg.chat.mention} ({msg.chat.id})')
    await state.finish()
    agent = await Database.add_agent(msg.text)
    await msg.answer(
        f'Агент #{agent.uid} - Добавлен!',
        reply_markup=keys.back('agents', 'К агентам')
    )


@bot.callback_query_handler(lambda q: q.data == 'del_agents')
@check_admin()
async def del_agent_start(query: types.CallbackQuery):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    agents = await Database.get_agents()
    if not agents:
        await query.answer('Агенты отсутствуют. Нечего удалять.')
    else:
        await query.answer()
        await query.message.edit_text(
            'Выберите агента для удаления.',
            reply_markup=keys.del_agent(agents)
        )


@bot.callback_query_handler(lambda q: q.data.startswith('del_agent'))
@check_admin()
async def del_agent_end(query: types.CallbackQuery):
    log.info(
        f'Called by {query.message.chat.mention} ({query.message.chat.id})'
    )
    agent_uid = int(query.data.split('#')[1])
    await Database.del_agent(agent_uid)
    await query.answer(f'Агент #{agent_uid} - удален!')
    await agents(query, None)
