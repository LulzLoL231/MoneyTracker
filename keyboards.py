# -*- coding: utf-8 -*-
#
#  MoneyTracker: VK Keyboards
#  Created by LulzLoL231 at 28/06/22
#
from vkbottle import Keyboard, KeyboardButtonColor, Text

from database.types import Agent, Order


class Keyboards:
    YES_TEXTS = [
        'Да', 'да', 'y', 'yes', 'Yes', 'д'
    ]

    @staticmethod
    def start() -> str:
        '''Returns start keyboard.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        key.add(
            Text(
                'Заказы', {'command': 'orders'}
            ),
            KeyboardButtonColor.PRIMARY
        )
        key.add(
            Text(
                'Агенты', {'command': 'agents'}
            ),
            KeyboardButtonColor.PRIMARY
        )
        key.row()
        key.add(
            Text(
                'О боте', {'command': 'about'}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()

    @staticmethod
    def back(command: str = 'start') -> str:
        '''Returns back keyboard with provided command.

        Args:
            command (str, optional): Button command. Defaults to 'start'.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        key.add(
            Text(
                'Назад',
                {'command': command}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()

    @staticmethod
    def agents(with_del: bool = True) -> str:
        '''Returns agents keyboard.

        Args:
            with_del (bool): Add a del_agent btn? Defaults is True.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        if with_del:
            key.add(
                Text(
                    'Удалить агента', {'command': 'del_agent'}
                ),
                KeyboardButtonColor.NEGATIVE
            )
        key.add(
            Text(
                'Добавить агента', {'command': 'add_agent'}
            ),
            KeyboardButtonColor.POSITIVE
        )
        key.row()
        key.add(
            Text(
                'Назад', {'command': 'start'}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()

    @staticmethod
    def del_agent(agents: list[Agent]) -> str:
        '''Returns keyboards with agents IDs and names.

        Args:
            agents (list[Agent]): Array of Agents.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        for agent in agents:
            key.add(
                Text(
                    agent.name,
                    {'command': f'del_agent#{agent.uid}'}
                ),
                KeyboardButtonColor.NEGATIVE
            )
            key.row()
        key.add(
            Text(
                'Назад',
                {'command': 'agents'}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()

    @staticmethod
    def orders(orders: list[Order], with_his: bool = True) -> str:
        '''Returns orders short names keyboard.

        Args:
            orders (list[Order]): Array of orders.
            with_his (bool): Add history btn? Defaults is True.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        flag = False
        for ord in orders:
            key.add(
                Text(
                    f'Заказ #{ord.uid}',
                    {'command': f'order#{ord.uid}'}
                ),
                KeyboardButtonColor.PRIMARY
            )
            if flag:
                flag = False
                key.row()
            else:
                flag = True
        if flag:
            key.row()
        key.add(
            Text(
                'Добавить',
                {'command': 'add_order'}
            ),
            KeyboardButtonColor.POSITIVE
        )
        if with_his:
            key.add(
                Text(
                    'История',
                    {'command': 'orders_history'}
                ),
                KeyboardButtonColor.PRIMARY
            )
        key.row().add(
            Text(
                'Назад',
                {'command': 'start'}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()

    @staticmethod
    def order_ctrl(uid: int) -> str:
        '''Returns order control keyboard.

        Args:
            uid (int): Order UID.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        key.add(
            Text(
                'Оплачен',
                {'command': f'end_order#{uid}'}
            ),
            KeyboardButtonColor.POSITIVE
        )
        key.add(
            Text(
                'Удалить',
                {'command': f'del_order#{uid}'}
            ),
            KeyboardButtonColor.NEGATIVE
        ).row()
        key.add(
            Text(
                'Назад',
                {'command': 'orders'}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()

    @staticmethod
    def orders_history() -> str:
        '''Returns orders history keyboard.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        key.add(Text(
            'Информация о заказе',
            {'command': 'order_info'}
        ), KeyboardButtonColor.PRIMARY)
        key.add(Text(
            'Экспорт',
            {'command': 'orders_history_export'}
        ), KeyboardButtonColor.POSITIVE)
        key.row().add(Text(
            'Назад',
            {'command': 'orders'}
        ), KeyboardButtonColor.SECONDARY)
        return key.get_json()

    @staticmethod
    def add_order_agents(agents: list[Agent]) -> str:
        '''Returns keyboard with agents.

        Args:
            agents (list[Agent]): Array of agents.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        for agent in agents:
            key.add(
                Text(
                    agent.name,
                    {'agent_uid': agent.uid}
                ),
                KeyboardButtonColor.PRIMARY
            ).row()
        key.add(
            Text(
                'Назад',
                {'command': 'orders'}
            )
        )
        return key.get_json()

    @staticmethod
    def verify() -> str:
        '''Yes/No keyboard.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        key.add(
            Text('Да'),
            KeyboardButtonColor.POSITIVE
        )
        key.add(
            Text('Нет'),
            KeyboardButtonColor.NEGATIVE
        )
        return key.get_json()

    @staticmethod
    def order_btn(uid: int) -> str:
        '''Returns keyboard with order and back btns.

        Args:
            uid (int): Order UID.

        Returns:
            str: JSON string.
        '''
        key = Keyboard(True)
        key.add(
            Text(
                f'Заказ #{uid}',
                {'command': f'order#{uid}'}
            ),
            KeyboardButtonColor.POSITIVE
        ).row()
        key.add(
            Text(
                'Назад',
                {'command': 'orders'}
            ),
            KeyboardButtonColor.SECONDARY
        )
        return key.get_json()
