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

    class Config:
        orm_mode = True


class Order(BaseModel):
    uid: int
    name: str
    price: int | None = None
    agent_uid: int
    agent: Agent
    start_date: date
    end_date: date | None = None

    class Config:
        orm_mode = True

    def get_full_str(self) -> str:
        tmp_cnt = '''Заказ #{}
Цель: {}
Цена: {}
Агент: {}
{}'''
        tmp_sd = 'Начало: {}'
        tmp_sd_ed = 'Начало: {}\nКонец: {}'
        if not self.price:
            price = 'Не установлена'
        else:
            price = str(self.price) + ' руб.'
        if not self.end_date:
            return tmp_cnt.format(
                self.uid, self.name, price,
                self.agent.name, tmp_sd.format(
                    str(self.start_date)
                )
            )
        else:
            return tmp_cnt.format(
                self.uid, self.name, price,
                self.agent.name, tmp_sd_ed.format(
                    str(self.start_date), str(self.end_date)
                )
            )

    def get_short_str(self) -> str:
        if not self.price:
            price = 'на не установленную сумму.'
        else:
            price = f'на сумму {self.price} руб.'
        tmp_cnt = 'Заказ #{} {}'
        return tmp_cnt.format(self.uid, price)
