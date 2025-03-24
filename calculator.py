"""
Опишите класс Calculator, который будет реализовывать следующие методы и поля:
sum(self, a, b) - сложение чисел a и b
sub(self, a, b) - вычитание
mul(self, a, b) - умножение
div(self, a, b, mod=False) - деление. Если параметр mod == True, то метод должен возвращать
 остаток от деления вместо деления. По умолчанию mod=False.
history(self, n) - этот метод должен возвращать строку с операцией по ее номеру
 относительно текущего момента (1 - последняя, 2 - предпоследняя). Формат вывода: sum(5, 15) == 20
 (Не нужно форматировать результат операции). История операция своя у каждого объекта калькулятора.
last - строка того же формата, что в предыдущем пункте, в которой содержится
 информация о последней операции по всем созданным объектам калькулятора. Т.е. это
 последняя операция последнего использованного объекта калькулятор. Если операций пока не было, то None.
clear(cls) - метод, который очищает last, т.е. присваивает ему значение None.
"""

class Calculator:
    _all = []
    last = None

    def __init__(self):
        self._all = []

    @classmethod
    def _last(cls, op):
        cls.last = op

    def sum(self, a, b):
        result = f"sum({a}, {b}) == {a + b}"
        self._all.append(result)
        self._last(result)
        return a + b

    def sub(self, a, b):
        result = f"sub({a}, {b}) == {a - b}"
        self._all.append(result)
        self._last(result)
        return a - b

    def mul(self, a, b):
        result = f"mul({a}, {b}) == {a * b}"
        self._all.append(result)
        self._last(result)
        return a * b

    def div(self, a, b, mod=False):
        if mod:
            result = f"div({a}, {b}) == {a % b}"
            self._all.append(result)
            self._last(result)
            return a % b
        else:
            result = f"div({a}, {b}) == {a / b}"
            self._all.append(result)
            self._last(result)
            return a / b

    def history(self, n):
        if len(self._all) < n:
            return None
        else:
            return self._all[-n]

    @classmethod
    def clear(cls):
        cls.last = None


# Создаем экземпляр класса Calculator
calc1 = Calculator()

# Вызываем метод sum и div у экземпляра calc1
calc1.sum(5, 10)
calc1.div(10, 3, mod=True)

# Выводим последнюю операцию
print(calc1.last)  # Вывод: div(10, 3) == 1

calc2 = Calculator()
calc2.sum(50, 10)

# Обратите внимание, что метод last возвращает информацию о последней операции по всем созданным объектам калькулятора
print(calc2.last)  # Вывод: sum(50, 10) == 60
print(calc1.last)  # Вывод: sum(50, 10) == 60 (т.к. last - общий)

# Выводим последний и предпоследний элементы истории операций для экземпляра calc1
print(calc1.history(1))  # Вывод: div(10, 3) == 1
print(calc1.history(2))  # Вывод: sum(5, 10) == 15

# У другого экземпляра calc2 своя история операций
print(calc2.history(1))  # Вывод: sum(50, 10) == 60

# Очищаем историю всех экземпляров класса Calculator
calc1.clear()
print(calc1.last)  # Вывод: None
print(calc2.last)  # Вывод: None (т.к. last - общий)