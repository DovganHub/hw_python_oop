import datetime as dt
from typing import Optional


class Record:
    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount: int = amount
        self.date = (dt.datetime.now().date()
                     if date is None
                     else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment: str = comment


class Calculator:
    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.records = []

    def add_record(self, record) -> None:
        """
        Добавляет запись класса Record к листу-аттрибуту self.records

        """
        self.records.append(record)

    def get_today_stats(self) -> float:
        """
        Возвращает расход за текущий день.
        """
        return sum([i.amount for i in self.records
                    if i.date == dt.datetime.now().date()])

    def get_week_stats(self) -> float:
        """
        Возвращает сумму amount по всем записям за последнюю неделю
        """
        start = dt.datetime.now().date() - dt.timedelta(days=7)
        end = dt.datetime.now().date()
        return sum([i.amount for i in self.records if start <= i.date <= end])


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def __init__(self, limit) -> None:
        super().__init__(limit)

        self.currency_dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        self.rates_dict = {'rub': 1, 'usd': self.USD_RATE,
                           'eur': self.EURO_RATE}

    def get_today_cash_remained(self, currency) -> str:
        """
        Возвращает остаток денег в заданной валюте на текущий день.
        """
        remnant = self.limit - self.get_today_stats()
        remnant = round(remnant / self.rates_dict[currency], 2)

        if remnant > 0:
            return (f'На сегодня осталось {remnant}'
                    + f' {self.currency_dict[currency]}')
        elif remnant == 0:
            return 'Денег нет, держись'
        else:
            return (f'Денег нет, держись: твой долг - {abs(remnant)}'
                    + f' {self.currency_dict[currency]}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        remnant = self.limit - self.get_today_stats()
        if remnant <= 0:
            return 'Хватит есть!'
        else:
            return ('Сегодня можно съесть что-нибудь ещё, но'
                    + f' с общей калорийностью не более {remnant} кКал')
