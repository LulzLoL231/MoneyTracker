# -*- coding: utf-8 -*-
#
#  MoneyTracker: cmds - Defaults
#  Created by LulzLoL231 at 27/06/22
#
import logging

from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import FuncRule

from config import cfg


log = logging.getLogger('MoneyTracker')
bl = BotLabeler()


@bl.message(FuncRule(lambda mt: mt.text.lower() in ['/about', 'о боте']))
async def about_bot(msg: Message):
    user = await msg.get_user()
    log.info(f'Called by {user.first_name} {user.last_name} (@{user.domain} #{user.id})')
    cnt = f'MoneyTracker\n\nСоздатель: @0x403\nВерсия: {cfg.VERSION}'
    await msg.answer(cnt)
