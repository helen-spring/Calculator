import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Добавление записи в список records.
    def add_record(self, record):
        self.records.append(record)

    # Получение суммы затрат на сегодня.
    def get_today_stats(self):
        daily_sum = 0
        for record in self.records:
            if record.date == dt.date.today():
                daily_sum += record.amount
        return daily_sum

    # Получение суммы затрат за последнюю неделю.
    def get_week_stats(self):
        week_stats = 0
        week_ago = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if dt.date.today() >= record.date >= week_ago:
                week_stats += record.amount
        return week_stats

    # Получение доступного остатка на сегодня.
    def get_today_remained(self):
        remain_sum = self.limit - self.get_today_stats()
        return remain_sum


class CashCalculator(Calculator):
    USD_RATE = 70.93
    EURO_RATE = 78.20

    # Подсчёт оставшихся на сегодня денег в валюте.
    def get_today_cash_remained(self, currency):
        spent_sum = super().get_today_stats()
        remain_sum = abs(super().get_today_remained())
        # рубли
        if currency == 'rub':
            if spent_sum > self.limit:
                return f'Денег нет, держись: твой долг - {remain_sum} руб'
            elif spent_sum == self.limit:
                return f'Денег нет, держись'
            else:
                return f'На сегодня осталось {remain_sum} руб'
        # доллары
        elif currency == 'usd':
            remain_currency = float('{0:.2f}'.format(remain_sum / self.USD_RATE))
            if spent_sum > self.limit:
                return f'Денег нет, держись: твой долг - {remain_currency} USD'
            elif spent_sum == self.limit:
                return f'Денег нет, держись'
            else:
                return f'На сегодня осталось {remain_currency} USD'
        # евро
        elif currency == 'eur':
            remain_currency = float('{0:.2f}'.format(remain_sum / self.EURO_RATE))
            if spent_sum > self.limit:
                return f'Денег нет, держись: твой долг - {remain_currency} Euro'
            elif spent_sum == self.limit:
                return f'Денег нет, держись'
            else:
                return f'На сегодня осталось {remain_currency} Euro'
        else:
            return f'Неопознанная валюта'


class CaloriesCalculator(Calculator):
    # Подсчёт оставшихся на сегодня калорий.
    def get_calories_remained(self):
        spent_sum = super().get_today_stats()
        remain_sum = super().get_today_remained()
        if spent_sum >= self.limit:
            return f'Хватит есть!'
        else:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remain_sum} кКал'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = int(amount)
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


r1 = Record(amount=145, comment="Безудержный шопинг", date="29.05.2020")
r2 = Record(amount=1568, comment="Наполнение потребительской корзины", date="22.05.2020")
r3 = Record(amount=691, comment="Катание на такси", date="08.03.2019")

r4 = Record(amount=1186, comment="Кусок тортика. И ещё один.", date="29.05.2020")
r5 = Record(amount=20, comment="Йогурт.", date="28.05.2020")
r6 = Record(amount=1140, comment="Баночка чипсов.")

if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)
    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_week_stats())
    print(cash_calculator.get_today_cash_remained('eur'))

    calories_calculator = CaloriesCalculator(5000)
    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)
    print(calories_calculator.get_today_stats())
    print(calories_calculator.get_week_stats())
    print(calories_calculator.get_calories_remained())



