# -*- coding: utf-8 -*-
#
#  MoneyTracker: Database - Types.
#  Created by LulzLoL231 27/06/22
#
from datetime import date

from pydantic import BaseModel


class Agent(BaseModel):
    uid: int
    name: str


class Order(BaseModel):
    uid: int
    name: str
    price: int
    agent_uid: int
    agent: Agent
    start_date: date
    end_date: date | None

    def get_full_str(self) -> str:
        tmp_cnt = '''Заказ #{}
Цель: {}
Цена: {} руб.
Агент: {}
{}'''
        tmp_sd = 'Начало: {}'
        tmp_sd_ed = 'Начало: {}\nКонец: {}'
        if self.end_date:
            return tmp_cnt.format(
                self.uid, self.name, self.price,
                self.agent.name, tmp_sd.format(
                    str(self.start_date)
                )
            )
        else:
            return tmp_cnt.format(
                self.uid, self.name, self.price,
                self.agent.name, tmp_sd_ed.format(
                    str(self.start_date), str(self.end_date)
                )
            )

    def get_short_str(self) -> str:
        tmp_cnt = 'Заказ #{} на сумму {} руб.'
        return tmp_cnt.format(self.uid, self.price)