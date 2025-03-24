"""
Написать классы, которые будут использованы как счета в банке. Каждый счет - в своей валюте.
 Соответственно, у каждого объекта счета должны быть атрибуты с суммой денег, хранящихся на нём,
  и название кошелька. Каждый класс счета должен в себе хранить коэффициент отношения стоимости
   своей валюты к базовой валюте.

Нам понадобится один базовый класс BaseWallet, в котором будут реализованы общие для всех
 валютных счетов методы, и три класса для конкретных валютных счетов: RubleWallet, DollarWallet, EuroWallet.
  Будем считать коэффициентами отношения валют к базовой валюте:

Рубль: 1
Доллар: 60
Евро: 70

Протокол взаимодействия объектов следующий:

RubleWallet("Первый кошелек", 10), где "Первый кошелек" - это название кошелька, а 10 - сумма денег на нём.
аналогичные конструкторы для других счетов
RubleWallet("X", 10) + 20 == RubleWallet("X", 30) - при сложении с числом считаем, что это та же валюта.
RubleWallet("X", 10) += 20 - должен поддерживаться и такой синтаксис
20 + RubleWallet("X", 10) == RubleWallet("X", 30) - radd для чисел
RubleWallet("X", 20) + DollarWallet("D", 10) == RubleWallet("X", 620) - конвертация валюты при сложении счетов.
DollarWallet("D", 2) + RubleWallet("X", 60) == DollarWallet("D", 3) - результат - в валюте первого слагаемого.
DollarWallet("D", 2) += RubleWallet("X", 60) - здесь тоже должен поддерживаться этот синтаксис.
предыдущие 6 пунктов реализовать и для вычитания
RubleWallet("X", 10) * 20 == RubleWallet("X", 200) - умножение на число
RubleWallet("X", 10) *= 20 - тоже с таким синтаксисом
те же 2 пункта для деления
20 * RubleWallet("X", 10) == RubleWallet("X", 200) - умножение числа на кошелек
DollarWallet("A", 15) == DollarWallet("B", 15): два объекта равны, если у них совпадает тип кошелька и сумма на счете.
RubleWallet("X", 100).spend_all() - для любого типа кошелька релизовать функцию, которая обнуляет баланс, если он положительный
DollarWallet("X", 1).to_base() == 60 - эта функция должна возвращать число денег в кошельке в базовой валюте
print(DollarWallet("Q", 150)) - должна выводить строку: 'Dollar Wallet Q 150' (и аналогично Ruble и Euro для остальных кошельков)

У каждого объекта должны быть доступны атрибуты:
name - название кошелька
amount - количество денег на счете
exchange_rate - коэффициент стоимости валюты к базовой

Пример использования
# Создаем объект RubleWallet кошелька
ruble_wallet = RubleWallet("Первый кошелек", 10)

# Добавляем 20 к кошельку (та же валюта)
result = ruble_wallet + 20
print(result)  # Выводит: Ruble Wallet Первый кошелек 30

# Создаем объект DollarWallet кошелька и добавляем его к RubleWallet кошельку (конвертация валют)
dollar_wallet = DollarWallet("D", 10)
result = ruble_wallet + dollar_wallet
print(result)  # Выводит: Ruble Wallet Первый кошелек 610
"""


class BaseWallet:
    currency = "Base"
    exchange_rate = 1

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def spend_all(self):
        if self.amount > 0:
            self.amount = 0

    def to_base(self):
        return self.amount * self.exchange_rate

    def __str__(self):
        return self.currency + " Wallet " + self.name + " " + str(self.amount)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            new_amount = self.amount + other.amount
        elif isinstance(other, BaseWallet):
            new_amount = self.amount + other.to_base() / self.exchange_rate
        else:
            new_amount = self.amount + float(other)
        return self.__class__(self.name, new_amount)

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self.amount += other.amount
        elif isinstance(other, BaseWallet):
            self.amount += other.to_base() / self.exchange_rate
        else:
            self.amount += other
        return self

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            new_amount = self.amount - other.amount
        elif isinstance(other, BaseWallet):
            new_amount = self.amount - other.to_base() / self.exchange_rate
        else:
            new_amount = self.amount - float(other)
        return self.__class__(self.name, new_amount)

    def __rsub__(self, other):
        if isinstance(other, self.__class__):
            new_amount = other.amount - self.amount
        elif isinstance(other, BaseWallet):
            new_amount = other.to_base() / self.exchange_rate - self.amount
        else:
            new_amount = int(other) - self.amount
        return self.__class__(self.name, new_amount)

    def __isub__(self, other):
        if isinstance(other, self.__class__):
            self.amount = self.amount - other.amount
        elif isinstance(other, BaseWallet):
            self.amount = self.amount - other.to_base() / self.exchange_rate
        else:
            self.amount = self.amount - float(other)
        return self

    def __mul__(self, other):
        new_amount = self.amount * float(other)
        return self.__class__(self.name, new_amount)

    __rmul__ = __mul__

    def __imul__(self, other):
        self.amount = self.amount * float(other)
        return self

    def __truediv__(self, other):
        new_amount = self.amount / float(other)
        return self.__class__(self.name, new_amount)

    def __rtruediv__(self, other):
        new_amount = float(other) / self.amount
        return self.__class__(self.name, new_amount)

    def __itruediv__(self, other):
        self.amount = self.amount / float(other)
        return self

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.amount == other.amount:
            return True
        else:
            return False


class RubleWallet(BaseWallet):
    def __init__(self, name, amount):
        super(RubleWallet, self).__init__(name, amount)
        self.currency = "Ruble"
        self.exchange_rate = 1


class DollarWallet(BaseWallet):
    def __init__(self, name, amount):
        super(DollarWallet, self).__init__(name, amount)
        self.currency = "Dollar"
        self.exchange_rate = 60


class EuroWallet(BaseWallet):
    def __init__(self, name, amount):
        super(EuroWallet, self).__init__(name, amount)
        self.currency = "Euro"
        self.exchange_rate = 70


# Создаем объект RubleWallet кошелька
ruble_wallet = RubleWallet("Первый кошелек", 10)

# Добавляем 20 к кошельку (та же валюта)
result = ruble_wallet + 20
print(result)  # Выводит: Ruble Wallet Первый кошелек 30

ruble_wallet += 15
result = ruble_wallet
print(result) # Выводит: Ruble Wallet Первый кошелек 25

# Создаем объект DollarWallet кошелька и добавляем его к RubleWallet кошельку (конвертация валют)
dollar_wallet = DollarWallet("D", 10)
result = ruble_wallet + dollar_wallet
print(result)  # Выводит: Ruble Wallet Первый кошелек 625