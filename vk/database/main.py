# -*- coding: utf-8 -*-
#
#  MoneyTracker: Database - Main.
#  Created by LulzLoL231 27/06/22
#
import logging
from datetime import date
from typing import Literal

import sqlalchemy as sa
from async_lru import alru_cache
from databases import DatabaseURL, Database as DB

from config import cfg
from . import models
from .types import Agent, Order


database = DB(str(cfg.postgres_dsn))


class Database:
    log = logging.getLogger('MoneyTrackerDB')

    def __init__(self) -> None:
        self.db = database

    @classmethod
    def _create_tables(cls):
        '''Creates tables from metadata.
        '''
        cls.log.debug('Creating tables...')
        dsn = DatabaseURL(str(cfg.postgres_dsn)).replace(driver='psycopg2')
        engine = sa.create_engine(str(dsn), echo=cfg.DEBUG)
        models.metadata.create_all(engine)

    async def connect(self):
        '''Connect to PostgreSQL.
        '''
        await self.db.connect()

    async def disconnect(self):
        '''Disconnect from PostgreSQL.
        '''
        await self.db.disconnect()

    @database.transaction()
    async def add_agent(self, name: str) -> Agent:
        '''Add a new agent to DB.

        Args:
            name (str): Agent name.

        Returns:
            Agent: A created Agent.
        '''
        self.log.debug(f'Called with args: ({name})')
        stmt1 = models.agent.insert().values(name=name)
        uid = await self.db.execute(stmt1, {'name': name})
        return Agent(uid=uid, name=name)

    @alru_cache
    async def get_agent_by_uid(self, uid: int) -> Agent | None:
        '''Returns agent by UID.

        Args:
            uid (int): Agent UID.

        Returns:
            Agent | None: Agent if exists.
        '''
        self.log.debug(f'Called with args: ({uid})')
        stmt = models.agent.select().where(models.agent.c.uid == uid)
        res = await self.db.fetch_one(stmt)
        if res:
            return Agent.from_orm(res)
        return None

    async def get_orders(self) -> list[Order]:
        '''Returns all orders.

        Returns:
            list[Order]: Array of orders.
        '''
        self.log.debug('Called!')
        orders = []
        stmt = models.order.select()
        fetch = await self.db.fetch_all(stmt)
        if fetch:
            for ord in fetch:
                agent = await self.get_agent_by_uid(ord.agent_uid)
                if agent:
                    orders.append(Order(
                        uid=ord.uid,
                        name=ord.name,
                        price=ord.price,
                        agent_uid=ord.agent_uid,
                        agent=agent,
                        start_date=ord.start_date,
                        end_date=ord.end_date
                    ))
                else:
                    self.log.error(
                        f'Order #{ord.uid} have nonexistent '
                        f'Agent UID #{ord.agent_uid}')
        return orders

    async def get_inprogress_orders(self) -> list[Order]:
        '''Returns all not ended orders.

        Returns:
            list[Order]: Array of orders.
        '''
        self.log.debug('Called!')
        orders = []
        stmt = models.order.select().where(
            models.order.c.end_date == None  # noqa
        )
        fetch = await self.db.fetch_all(stmt)
        if fetch:
            for ord in fetch:
                agent = await self.get_agent_by_uid(ord.agent_uid)
                if agent:
                    orders.append(Order(
                        uid=ord.uid,
                        name=ord.name,
                        price=ord.price,
                        agent_uid=ord.agent_uid,
                        agent=agent,
                        start_date=ord.start_date,
                        end_date=ord.end_date
                    ))
                else:
                    self.log.error(
                        f'Order #{ord.uid} have nonexistent '
                        f'Agent UID #{ord.agent_uid}')
        return orders

    @database.transaction()
    async def del_agent(self, uid: int) -> Literal[True]:
        '''Deletes Agent from DB.

        Args:
            uid (int): Agent UID.

        Returns:
            Literal[True]: Always True.
        '''
        self.log.debug(f'Called with args: ({uid})')
        stmt = models.agent.delete().where(models.agent.c.uid == uid)
        await self.db.execute(stmt, {'uid': uid})
        return True

    @database.transaction()
    async def add_order(self, name: str, price: int, agent_uid: int) -> Order:
        '''Add a new Order to DB.

        Args:
            name (str): Order name.
            price (int): Order price.
            agent_uid (int): Agent UID.

        Returns:
            Order: A created Order.
        '''
        self.log.debug(f'Called with args: ({name}, {price}, {agent_uid})')
        values = {
            'name': name, 'price': price, 'agent_uid': agent_uid,
            'start_date': date.today()
        }
        stmt = models.order.insert().values(**values)
        uid = await self.db.execute(stmt, values)
        agent = await self.get_agent_by_uid(agent_uid)
        return Order(
            uid=uid, name=name, price=price, agent_uid=agent_uid,
            agent=agent, start_date=values['start_date']
        )

    async def get_agents(self) -> list[Agent]:
        '''Returns all agents.

        Returns:
            list[Agents]: Array of agents.
        '''
        self.log.debug('Called!')
        stmt = models.agent.select()
        fetch = await self.db.fetch_all(stmt)
        return [Agent.from_orm(i) for i in fetch]

    @alru_cache
    async def get_order_by_uid(self, uid: int) -> Order | None:
        '''Returns Order by UID.

        Args:
            uid (int): Order UID.

        Returns:
            Order | None: Order if exists.
        '''
        self.log.debug(f'Called with args: ({uid})')
        stmt = models.order.select().where(models.order.c.uid == uid)
        fetch = await self.db.fetch_one(stmt)
        if fetch:
            agent = await self.get_agent_by_uid(fetch.agent_uid)
            if agent:
                return Order(
                    uid=fetch.uid,
                    name=fetch.name,
                    price=fetch.price,
                    agent_uid=fetch.agent_uid,
                    agent=agent,
                    start_date=fetch.start_date,
                    end_date=fetch.end_date
                )
            else:
                self.log.error(
                    f'Order #{fetch.uid} have nonexistent '
                    f'Agent UID #{fetch.agent_uid}')
        return None

    @database.transaction()
    async def end_order(self, uid: int) -> Literal[True]:
        '''Set end_date to Order by provided uid.

        Args:
            uid (int): Order UID.

        Returns:
            Literal[True]: Always True.
        '''
        self.log.debug(f'Called with args: ({uid})')
        end_date = date.today()
        stmt = models.order.update().where(
            models.order.c.uid == uid
        ).values(
            end_date=end_date
        )
        await self.db.execute(stmt, {
            'uid': uid, 'end_date': end_date
        })
        return True

    @database.transaction()
    async def del_order(self, uid: int) -> Literal[True]:
        '''Deletes order from DB.

        Args:
            uid (int): Order UID.

        Returns:
            Literal[True]: Always True.
        '''
        self.log.debug(f'Called with args: ({uid})')
        stmt = models.order.delete().where(models.order.c.uid == uid)
        await self.db.execute(stmt, {'uid': uid})
        return True


db = Database()
