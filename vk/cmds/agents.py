# -*- coding: utf-8 -*-
#
#  MoneyTracker: cmds - Agents
#  Created by LulzLoL231 at 28/06/22
#
import json
import logging

from vkbottle.bot import Message
from vkbottle import BaseStateGroup, BotBlueprint
from vkbottle.dispatch.rules.base import FuncRule, StateRule

from database.main import db as Database
from keyboards import Keyboards as keys


log = logging.getLogger('MoneyTracker')
bp = BotBlueprint('agents')


class AddAgent(BaseStateGroup):
    NAME = 'name'


def is_del_agent_cmd(payload: str | None) -> bool:
    if payload:
        pd = json.loads(payload)
        return pd.get('command', '').startswith('del_agent#')
    return False


@bp.on.private_message(FuncRule(
    lambda m: m.text.lower() in ['/agents', 'агенты']
))
@bp.on.private_message(payload={'command': 'agents'})
async def agents(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    agents = await Database.get_agents()
    if agents:
        cnt = 'Список агентов:\n\n'
        cnt += '\n'.join([f'#{a.uid} - {a.name}' for a in agents])
    else:
        cnt = 'Агенты отсутствуют. Добавьте нового!'
    await msg.answer(cnt, keyboard=keys.agents(bool(agents)))


@bp.on.private_message(payload={'command': 'add_agent'})
async def add_agent_start(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    await bp.state_dispenser.set(msg.peer_id, AddAgent.NAME)
    await msg.answer('Добавление нового агента.\n\nОтправьте имя агента.')


@bp.on.private_message(StateRule(AddAgent.NAME))
async def add_agent_end(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    if msg.text.lower() == 'назад':
        await bp.state_dispenser.delete(msg.peer_id)
        log.info(f'User #{msg.peer_id} canceled adding agent.')
        await agents(msg)
        return
    agent = await Database.add_agent(msg.text)
    Database.get_agent_by_uid.cache_clear()
    await bp.state_dispenser.delete(msg.peer_id)
    await msg.answer(
        f'Агент #{agent.uid} - Добавлен!',
        keyboard=keys.back('agents')
    )


@bp.on.private_message(payload={'command': 'del_agent'})
async def del_agent_start(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    agents = await Database.get_agents()
    if not agents:
        await msg.answer(
            'Агенты отсутствуют. Нечего удалять.',
            keyboard=keys.back('agents')
        )
    else:
        await msg.answer(
            'Выберите агента для удаления.',
            keyboard=keys.del_agent(agents)
        )


@bp.on.private_message(FuncRule(lambda m: is_del_agent_cmd(m.payload)))
async def del_agent_end(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} ({user.id})')
    msg_payload_json: dict = msg.get_payload_json()  # type: ignore
    agent_uid = int(msg_payload_json['command'].split('#')[1])
    await Database.del_agent(agent_uid)
    Database.get_agent_by_uid.cache_clear()
    await msg.answer(
        f'Агент #{agent_uid} - удален!',
        keyboard=keys.back('agents')
    )
