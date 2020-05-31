import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Добавление записи в список records."""
        self.records.append(record)

    def get_today_stats(self):
        """Получение суммы затрат на сегодня."""
        return sum(record.amount
                   for record in self.records
                   if record.date == dt.date.today())

    def get_week_stats(self):
        """Получение суммы затрат за последнюю неделю."""
        week_ago = dt.date.today() - dt.timedelta(days=7)
        return sum(record.amount
                   for record in self.records
                   if dt.date.today() >= record.date >= week_ago)

    def get_today_remained(self):
        """Получение доступного остатка на сегодня."""
        remain_sum = self.limit - self.get_today_stats()
        return remain_sum


class CashCalculator(Calculator):
    USD_RATE = 71.20
    EURO_RATE = 78.30

    def get_today_cash_remained(self, currency):
        currency_list = {
            'rub': ['руб', 1],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]
        }
        """Подсчёт оставшихся на сегодня денег в валюте."""
        spent_sum = self.get_today_stats()
        currency_name, currency_rate = currency_list.get(currency)
        remain_sum = abs(self.get_today_remained() / currency_rate)
        if currency in currency_list:
            if spent_sum > self.limit:
                return f'Денег нет, держись: твой долг - {remain_sum:.2f} {currency_name}'
            elif spent_sum == self.limit:
                return 'Денег нет, держись'
            else:
                return f'На сегодня осталось {remain_sum:.2f} {currency_name}'
        else:
            raise Exception('Валюта не входит в список допустимых')


class CaloriesCalculator(Calculator):
    @property
    def get_calories_remained(self):
        """Подсчёт оставшихся на сегодня калорий."""
        spent_sum = self.get_today_stats()
        remain_sum = self.get_today_remained()
        if spent_sum >= self.limit:
            return 'Хватит есть!'
        return f'Сегодня можно съесть что-нибудь ещё, ' \
               f'но с общей калорийностью не более {remain_sum} кКал'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = int(amount)
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment
