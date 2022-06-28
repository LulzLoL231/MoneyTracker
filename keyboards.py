# -*- coding: utf-8 -*-
#
#  MoneyTracker: VK Keyboards
#  Created by LulzLoL231 at 28/06/22
#
from vkbottle import Keyboard, KeyboardButtonColor, Text

from database.types import Agent


class Keyboards:
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
            KeyboardButtonColor.PRIMARY
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
