# -*- coding: utf-8 -*-
#
#  MoneyTracker: Database models.
#  Created by LulzLoL231 at 19/10/22
#
from datetime import date

import sqlalchemy as sa


metadata = sa.MetaData()

order = sa.Table(
    'orders',
    metadata,
    sa.Column('uid', sa.INTEGER, primary_key=True),
    sa.Column('name', sa.TEXT),
    sa.Column('price', sa.INTEGER),
    sa.Column(
        'agent_uid', sa.INTEGER,
        sa.ForeignKey('agents.uid'), nullable=True, default=None
    ),
    sa.Column('start_date', sa.DATE, default=date.today),
    sa.Column('end_date', sa.DATE, nullable=True, default=None),
)

agent = sa.Table(
    'agents',
    metadata,
    sa.Column('uid', sa.INTEGER, primary_key=True),
    sa.Column('name', sa.TEXT)
)
