import datetime as dt
from typing import Optional
DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount: int = amount
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
            # Привет! Вынес формат в константу за пределами класса, но ведь
            # когда класс импортируют, там этой переменной не будет, как быть?
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
        return sum(record.amount for record in self.records
                   if record.date == dt.datetime.now().date())

    def get_week_stats(self) -> float:
        """
        Возвращает сумму amount по всем записям за последнюю неделю
        """
        end = dt.datetime.now().date()
        start = end - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if start <= record.date <= end)

    def get_remnant(self) -> float:
        """
        Возвращает остаток amount на текущий момент
        """
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 300.0
    EURO_RATE = 500.0

    def get_today_cash_remained(self, currency) -> str:
        """
        Возвращает остаток денег в заданной валюте на текущий день.
        """
        currency_dict = {'rub': ('руб', 1), 'usd': ('USD', self.USD_RATE),
                         'eur': ('Euro', self.EURO_RATE)}
        remnant = round(self.get_remnant() / currency_dict[currency][1], 2)
        currency_text = currency_dict[currency][0]
        if remnant == 0:
            return 'Денег нет, держись'
        elif remnant > 0:
            return (f'На сегодня осталось {remnant}'
                    f' {currency_text}')
        else:
            return (f'Денег нет, держись: твой долг - {abs(remnant)}'
                    f' {currency_text}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        remnant = self.get_remnant()
        if remnant <= 0:
            return 'Хватит есть!'
        # else был избыточен, т.к. ничего не менял
        return ('Сегодня можно съесть что-нибудь ещё, но'
                f' с общей калорийностью не более {remnant} кКал')
