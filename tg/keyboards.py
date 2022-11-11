# -*- coding: utf-8 -*-
#
#  MoneyTracker - Keyboards.
#  Created by LulzLoL231 at 20/10/22
#
from aiogram import types

from database.types import Agent, Order


class Keyboards:
    @staticmethod
    def start() -> types.InlineKeyboardMarkup:
        '''Returns start keyboard.

        Returns:
            types.InlineKeyboardButton: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup()
        key.insert(types.InlineKeyboardButton(
            'Заказы',
            callback_data='orders'
        ))
        key.insert(types.InlineKeyboardButton(
            'Агенты',
            callback_data='agents'
        ))
        key.row()
        key.add(types.InlineKeyboardButton(
            'О боте',
            callback_data='about'
        ))
        return key

    @staticmethod
    def back(
        data: str = 'start',
        text: str = 'Назад'
    ) -> types.InlineKeyboardMarkup:
        '''Returns inline keyboard with back btn.

        Args:
            data (str): callback_data.
            text (str): btn text.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton(
            text, callback_data=data
        ))
        return key

    @staticmethod
    def inline_agents() -> types.InlineKeyboardMarkup:
        '''Inline keyboard "add" & "remove" agent.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        key.insert(types.InlineKeyboardButton(
            'Добавить',
            callback_data='add_agent'
        ))
        key.insert(types.InlineKeyboardButton(
            'Удалить',
            callback_data='del_agents'
        ))
        key.add(types.InlineKeyboardButton(
            'Назад',
            callback_data='start'
        ))
        return key

    @staticmethod
    def del_agent(
        agents: list[Agent]
    ) -> types.InlineKeyboardMarkup:
        '''Inline keyboard with keys for delete agent.

        Args:
            agents (list[Agent]): Array of agents.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        for agent in agents:
            key.insert(types.InlineKeyboardButton(
                agent.name,
                callback_data=f'del_agent#{agent.uid}'
            ))
        key.row()
        key.add(types.InlineKeyboardButton(
            'Назад',
            callback_data='agents'
        ))
        return key

    @staticmethod
    def orders(
        orders: list[Order],
        with_his: bool = True
    ) -> types.InlineKeyboardMarkup:
        '''Returns orders short names keyboard.

        Args:
            orders (list[Order]): Array of orders.
            with_his (bool, optional): Add histofy btn? Defaults to True.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        for ord in orders:
            key.insert(types.InlineKeyboardButton(
                f'Заказ #{ord.uid}',
                callback_data=f'order#{ord.uid}'
            ))
        key.row()
        key.insert(types.InlineKeyboardButton(
            'Добавить',
            callback_data='add_order'
        ))
        if with_his:
            key.insert(types.InlineKeyboardButton(
                'История',
                callback_data='ordres_history'
            ))
        key.row()
        key.add(types.InlineKeyboardButton(
            'Назад',
            callback_data='start'
        ))
        return key

    @staticmethod
    def order_ctrl(uid: int) -> types.InlineKeyboardMarkup:
        '''Returns order control keyboard.

        Args:
            uid (int): Order UID.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        key.insert(types.InlineKeyboardButton(
            'Оплачен',
            callback_data=f'end_order#{uid}'
        ))
        key.insert(types.InlineKeyboardButton(
            'Удалить',
            callback_data=f'del_order#{uid}'
        ))
        key.add(types.InlineKeyboardButton(
            'Назад',
            callback_data='orders'
        ))
        return key

    @staticmethod
    def order_history() -> types.InlineKeyboardButton:
        '''returns orders history keyboard.

        Returns:
            types.InlineKeyboardButton: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton(
            'Информация о заказе',
            callback_data='order_info'
        ))
        key.add(types.InlineKeyboardButton(
            'Экспорт',
            callback_data='export_order_history'
        ))
        key.add(types.InlineKeyboardButton(
            'Назад',
            callback_data='orders'
        ))
        return key

    @staticmethod
    def add_order_agents(agents: list[Agent]) -> types.InlineKeyboardMarkup:
        '''Returns keyboard with agents.

        Args:
            agents (list[Agent]): Array of agents.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        for agent in agents:
            key.insert(types.InlineKeyboardButton(
                agent.name, callback_data=f'agent_order#{agent.uid}'
            ))
        key.row()
        key.add(types.InlineKeyboardButton(
            'Отмена', callback_data='orders'
        ))
        return key

    @staticmethod
    def inline_verify_order() -> types.InlineKeyboardMarkup:
        '''Yes/No inline keyboard.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        key.insert(types.InlineKeyboardButton(
            'Да', callback_data='verify_order'
        ))
        key.insert(types.InlineKeyboardButton(
            'Нет', callback_data='cancel'
        ))
        return key

    @staticmethod
    def order_btn(uid: int) -> types.InlineKeyboardMarkup:
        '''Returns keyboard with order and back btns.

        Args:
            uid (int): Order UID.

        Returns:
            types.InlineKeyboardMarkup: Tg inline keyboard.
        '''
        key = types.InlineKeyboardMarkup(2)
        key.insert(types.InlineKeyboardButton(
            f'Заказ #{uid}',
            callback_data=f'order#{uid}'
        ))
        key.row()
        key.add(types.InlineKeyboardButton(
            'Назад',
            callback_data='orders'
        ))
        return key
