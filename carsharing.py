"""
В данной задаче мы создаем логику для сервиса каршеринга, позволяющего пользователям
 арендовать автомобили на определенное время и расстояние. Для реализации этой логики
 нам необходимо определить классы User, Car. Сервис предлагает как стандартные автомобили
 с бензиновым двигателем, так и электромобили. Чтобы учесть специфику каждого типа автомобиля,
 нам понадобятся классы StandardCar и ElectricCar, которые будут наследовать от базового класса
 Car. Необходимо реализовать данные классы, а также обеспечить корректную работу системы аренды
 с учетом ограничений.

Класс User:
user_id: уникальный идентификатор пользователя.
name: имя пользователя.
balance: текущий баланс пользователя.
rental_history: история аренд пользователя. (Список словарей формата
 {"car": {Объект автомобиля},"duration": {Длительность поездки},"distance": {Дистанция поездки}})
top_up_balance(amount): метод для пополнения баланса пользователя.
 (Условимся, что пополнение баланса происходит через внешнюю платежную систему, и метод
 просто обновляет баланс пользователя на полученную сумму)
rent_car(car, duration_minutes, distance_km): метод для аренды автомобиля. Возвращает True,
 если аренда возможна, и False в противном случае. Если аренда возможна - списывается стоимость аренды с баланса.
end_rental(): метод для завершения аренды.

Абстрактный класс Car:
model: модель автомобиля.
registration_number: регистрационный номер.
price_per_minute: стоимость аренды в минуту.
status: available (доступен) или rented (в аренде).
refill(): абстрактный метод для пополнения топлива/заряда до максимальной емкости
 (Должен быть переопределен в дочерних классах).

Класс StandardCar:
Наследуется от Car.
fuel_capacity: емкость топливного бака в литрах.
fuel_consumption: расход топлива в литрах на 100 км.
current_fuel: текущий уровень топлива.
refill(): метод для пополнения уровня топлива до максимальной емкости.
 (Условимся, что вызывая данный метод, сотрудник нашего сервиса заправляет автомобиль до полного бака)

Класс ElectricCar:
Наследуется от Car.
battery_capacity: емкость аккумулятора в киловатт-часах.
energy_consumption: расход энергии в киловатт-часах на 100 км.
current_charge: текущий уровень заряда.
refill(): метод для пополнения уровня заряда до максимальной емкости.
 (Условимся, что вызывая данный метод, сотрудник нашего сервиса заряжает автомобиль до полного заряда аккумулятора)

Логика аренды автомобиля:
Система аренды автомобилей (метод rent_car) работает следующим образом:
Пользователь выбирает автомобиль для аренды (car) и указывает требуемое кол-во минут
 и километров (duration_minutes и distance_km).
Система проверяет, выполнены ли следующие условия для успешной аренды:
Баланс пользователя: Баланс пользователя должен быть неотрицательным. Если
 баланс отрицательный, то аренда невозможна. Пользователь должен пополнить свой
 баланс, чтобы он стал неотрицательным, прежде чем сможет взять новый автомобиль в
 аренду. (Условимся, что если пользователь долго будет с отрицательным балансом - пойдем выбивать долги)
Отсутствие активной аренды: У пользователя не должно быть активной аренды.
Доступность автомобиля: Выбранный автомобиль должен быть доступен для аренды (статус "available").
Достаточность топлива/заряда: Автомобиль должен иметь достаточный уровень топлива/заряда, чтобы
 преодолеть указанное расстояние.
Если все условия выполнены, аренда оформляется (у пользователя начинается активная аренда,
 а автомобиль становиится недоступен для аренды другими пользователями), пока не
 будет завершена пользователем (не будет вызван метод end_rental). При успешной
 аренде у пользователя должен уменьшиться баланс на сумму стоимости аренды
 (Стоимость аренды = длительность поездки * стоимость аренды в минуту).
После завершения аренды у автомобиля должен убавиться уровень топлива или заряда
 в соответствии с пройденным расстоянием.


# Создание пользователя
user = User(user_id=1, name="Борис", balance=1000)

# Создание автомобилей
car = StandardCar(model="Toyota Camry", registration_number="A123BB", price_per_minute=10,
 fuel_capacity=60, fuel_consumption=8, current_fuel=60)

# Баланс пользователя и кол-во топлива в автомобиле до аренды
print(user.balance) # 1000
print(car.current_fuel) # 60

# Попытка аренды автомобиля
user.rent_car(car, duration_minutes=30, distance_km=20)

# Завершение аренды
user.end_rental()

# Изменения после завершения аренды
print(user.balance) # 700
print(car.current_fuel) # 58.4

# Пополнение баланса пользователя и заправка автомобиля
user.top_up_balance(500)
car.refill()

# Изменения после пополнения топлива и баланса пользователя
print(user.balance) # 1200
print(car.current_fuel) # 60

"""
from abc import ABC, abstractmethod

class User:
    def __init__(self, user_id, name, balance):
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.rental_history = []
        self._isactive = False
        self._current_car = {}

    def top_up_balance(self, amount):
        self.balance += amount

    def rent_car(self, car, duration_minutes, distance_km):
        if (self.balance < 0 or
            self._isactive or
            car.status == "rented" or
            isinstance(car, StandardCar) and distance_km * car.fuel_consumption / 100 > car.current_fuel or
            isinstance(car, ElectricCar) and distance_km * car.energy_consumption / 100 > car.current_charge
        ):
            return False
        else:
            car.status = "rented"
            self._isactive = True
            self.balance -= duration_minutes * car.price_per_minute
            self._current_car = {
                 "car": car,
                 "duration": duration_minutes,
                 "distance": distance_km}
            return True


    def end_rental(self):
        if self._isactive:
            car = self._current_car["car"]
            distance = self._current_car["distance"]
            self.rental_history.append(self._current_car)
            car.status = "available"
            self._isactive = False
            if isinstance(car, StandardCar):
                car.current_fuel -= distance * car.fuel_consumption / 100
            elif isinstance(car, ElectricCar):
                car.current_charge -= distance * car.energy_consumption / 100


class Car(ABC):
    @abstractmethod
    def __init__(self, model, registration_number, price_per_minute):
        self.model = model
        self.registration_number = registration_number
        self.price_per_minute = price_per_minute
        self.status = "available"

    @abstractmethod
    def refill(self):
        pass

class StandardCar(Car):
    def __init__(self, model, registration_number, price_per_minute, fuel_capacity, fuel_consumption, current_fuel):
        super(StandardCar, self).__init__(model, registration_number, price_per_minute)
        self.fuel_capacity = fuel_capacity
        self.fuel_consumption = fuel_consumption
        self.current_fuel = current_fuel

    def refill(self):
        self.current_fuel = self.fuel_capacity


class ElectricCar(Car):
    def __init__(self, model, registration_number, price_per_minute, battery_capacity, energy_consumption, current_charge):
        super(ElectricCar, self).__init__(model, registration_number, price_per_minute)
        self.battery_capacity = battery_capacity
        self.energy_consumption = energy_consumption
        self.current_charge = current_charge

    def refill(self):
        self.current_charge = self.battery_capacity


# Создание пользователя
user = User(user_id=1, name="Борис", balance=1000)

# Создание автомобилей
car = StandardCar(model="Toyota Camry", registration_number="A123BB", price_per_minute=10,
 fuel_capacity=60, fuel_consumption=8, current_fuel=60)

# Баланс пользователя и кол-во топлива в автомобиле до аренды
print(user.balance) # 1000
print(car.current_fuel) # 60

# Попытка аренды автомобиля
user.rent_car(car, duration_minutes=30, distance_km=20)

# Завершение аренды
user.end_rental()

# Изменения после завершения аренды
print(user.balance) # 700
print(car.current_fuel) # 58.4

# Пополнение баланса пользователя и заправка автомобиля
user.top_up_balance(500)
car.refill()

# Изменения после пополнения топлива и баланса пользователя
print(user.balance) # 1200
print(car.current_fuel) # 60