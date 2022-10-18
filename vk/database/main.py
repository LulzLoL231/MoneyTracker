# -*- coding: utf-8 -*-
#
#  MoneyTracker: Database - Main.
#  Created by LulzLoL231 27/06/22
#
import logging
import platform
from asyncio import Lock
from datetime import date
from typing import Literal

import aiosqlite

from .types import Agent, Order


DB_LOCK = Lock()
# Fixing .env file path for Docker.
if platform.system() == 'Linux':
    DB_FILE = '/vk/database/bot.db'
else:
    DB_FILE = './vk/database/bot.db'


class Database:
    TABLES = [
        'CREATE TABLE IF NOT EXISTS "agents" '
        '("uid" INTEGER PRIMARY KEY, "name" TEXT)',
        'CREATE TABLE IF NOT EXISTS "orders" '
        '("uid" INTEGER PRIMARY KEY, "name" TEXT, "price" INTEGER, '
        '"agent_uid" TEXT, "start_date" TEXT, "end_date" TEXT)'
    ]
    log = logging.getLogger('MoneyTracker Database')

    @classmethod
    async def _dbcall_commit(cls, sql: str, params: tuple = tuple()) -> int:
        '''Makes a DB call.

        Args:
            sql (str): SQL statement.
            params (tuple, optional): SQL params. Defaults to tuple().

        Returns:
            int: Last row id.
        '''
        cls.log.debug(f'Called with args: ({sql}, {params})')
        async with aiosqlite.connect(DB_FILE) as db:
            cur = await db.execute(sql, params)
            await db.commit()
            return cur.lastrowid

    @classmethod
    async def _dbcall_fetchone(cls,
                               sql: str,
                               params: tuple = tuple()) -> dict | None:
        '''Fetching 1 row from DB.

        Args:
            sql (str): SQL statement.
            params (tuple, optional): SQL params. Defaults to tuple().

        Returns:
            dict | None: Row data if exists.
        '''
        cls.log.debug(f'Called with args: ({sql}, {params})')
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(sql, params)
            fetch = await cur.fetchone()
            if fetch:
                return dict(fetch)
            return None

    @classmethod
    async def _dbcall_fetchall(cls,
                               sql: str,
                               params: tuple = tuple()) -> list[dict] | None:
        '''Fetching all rows from DB.

        Args:
            sql (str): SQL statement.
            params (tuple, optional): SQL params. Defaults to tuple().

        Returns:
            list[dict] | None: Array of rows data if exists.
        '''
        cls.log.debug(f'Called with args: ({sql}, {params})')
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(sql, params)
            return [dict(i) for i in (await cur.fetchall())]

    @classmethod
    async def _create_tables(cls):
        '''Creates tables.
        '''
        cls.log.debug('Creating tables...')
        for sql in cls.TABLES:
            await cls._dbcall_commit(sql)

    @classmethod
    async def add_agent(cls, name: str) -> Agent:
        '''Add a new agent to DB.

        Args:
            name (str): Agent name.

        Returns:
            Agent: A created Agent.
        '''
        cls.log.debug(f'Called with args: ({name})')
        sql = 'INSERT INTO agents (name) VALUES (?)'
        params = (name,)
        uid = await cls._dbcall_commit(sql, params)
        return Agent(uid=uid, name=name)

    @classmethod
    async def get_agent_by_uid(cls, uid: int) -> Agent | None:
        '''Returns agent by UID.

        Args:
            uid (int): Agent UID.

        Returns:
            Agent | None: Agent if exists.
        '''
        cls.log.debug(f'Called with args: ({uid})')
        sql = 'SELECT * FROM agents WHERE uid=?'
        params = (uid,)
        agent = await cls._dbcall_fetchone(sql, params)
        if agent:
            return Agent(**agent)
        return None

    @classmethod
    async def get_orders(cls) -> list[Order]:
        '''Returns all orders.

        Returns:
            list[Order]: Array of orders.
        '''
        cls.log.debug('Called!')
        orders = []
        sql = 'SELECT * FROM orders'
        fetch = await cls._dbcall_fetchall(sql)
        if fetch:
            for ord in fetch:
                agent = await cls.get_agent_by_uid(ord['agent_uid'])
                if agent:
                    orders.append(Order(
                        uid=ord['uid'],
                        name=ord['name'],
                        price=ord['price'],
                        agent_uid=ord['agent_uid'],
                        agent=agent,
                        start_date=ord['start_date'],
                        end_date=ord.get('end_date', None)
                    ))
                else:
                    cls.log.error(
                        f'Order #{ord["uid"]} have nonexistent '
                        f'Agent UID #{ord["agent_uid"]}')
        return orders

    @classmethod
    async def del_agent(cls, uid: int) -> Literal[True]:
        '''Deletes Agent from DB.

        Args:
            uid (int): Agent UID.

        Returns:
            Literal[True]: Always True.
        '''
        cls.log.debug(f'Called with args: ({uid})')
        await cls._dbcall_commit(
            'DELETE FROM agents WHERE uid=?',
            (uid,)
        )
        return True

    @classmethod
    async def add_order(cls, name: str, price: int, agent_uid: int) -> Order:
        '''Add a new Order to DB.

        Args:
            name (str): Order name.
            price (int): Order price.
            agent_uid (int): Agent UID.

        Returns:
            Order: A created Order.
        '''
        cls.log.debug(f'Called with args: ({name}, {price}, {agent_uid})')
        sql = 'INSERT INTO orders (name, price, agent_uid, start_date) '\
              'VALUES (?,?,?,?)'
        params = (name, price, agent_uid, str(date.today()))
        uid = await cls._dbcall_commit(sql, params)
        agent = await cls.get_agent_by_uid(agent_uid)
        return Order(
            uid=uid, name=name, price=price, agent_uid=agent_uid,
            agent=agent, start_date=params[3]  # type: ignore
        )

    @classmethod
    async def get_agents(cls) -> list[Agent]:
        '''Returns all agents.

        Returns:
            list[Agents]: Array of agents.
        '''
        cls.log.debug('Called!')
        sql = 'SELECT * FROM agents'
        fetch = await cls._dbcall_fetchall(sql)
        return [Agent(**i) for i in fetch]  # type: ignore

    @classmethod
    async def get_order_by_uid(cls, uid: int) -> Order | None:
        '''Returns Order by UID.

        Args:
            uid (int): Order UID.

        Returns:
            Order | None: Order if exists.
        '''
        cls.log.debug(f'Called with args: ({uid})')
        sql = 'SELECT * FROM orders WHERE uid=?'
        params = (uid,)
        fetch = await cls._dbcall_fetchone(sql, params)
        if fetch:
            agent = await cls.get_agent_by_uid(fetch['agent_uid'])
            if agent:
                return Order(
                    uid=fetch['uid'],
                    name=fetch['name'],
                    price=fetch['price'],
                    agent_uid=fetch['agent_uid'],
                    agent=agent,
                    start_date=fetch['start_date'],
                    end_date=fetch.get('end_date', None)
                )
            else:
                cls.log.error(
                    f'Order #{fetch["uid"]} have nonexistent '
                    f'Agent UID #{fetch["agent_uid"]}')
        return None

    @classmethod
    async def end_order(cls, uid: int) -> Literal[True]:
        '''Set end_date to Order by provided uid.

        Args:
            uid (int): Order UID.

        Returns:
            Literal[True]: Always True.
        '''
        cls.log.debug(f'Called with args: ({uid})')
        sql = 'UPDATE orders SET end_date=? WHERE uid=?'
        params = (date.today(), uid)
        await cls._dbcall_commit(sql, params)
        return True

    @classmethod
    async def del_order(cls, uid: int) -> Literal[True]:
        '''Deletes order from DB.

        Args:
            uid (int): Order UID.

        Returns:
            Literal[True]: Always True.
        '''
        cls.log.debug(f'Called with args: ({uid})')
        sql = 'DELETE FROM orders WHERE uid=?'
        params = (uid,)
        await cls._dbcall_commit(sql, params)
        return True
