import datetime

class Meeting:
    def __init__(self, name, date, start_time, duration):
        self.name = name
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.participants = []

    @property
    def end_time(self):
        # Преобразуем start_time в datetime, добавив фиктивную дату
        start_datetime = datetime.datetime.combine(self.date, self.start_time)
        # Прибавляем длительность
        end_datetime = start_datetime + datetime.timedelta(minutes=self.duration)
        # Извлекаем время
        return end_datetime.time()

    def get_participants(self):
        result = [participant.name for participant in self.participants]
        return result

class Employee:
    def __init__(self, name):
        self.name = name
        self.schedule = []

    def add_meeting(self, new_meeting):
        for meeting in self.schedule:
            # Проверяем пересечение встреч
            if (meeting.date == new_meeting.date and
                new_meeting.start_time < meeting.end_time and
                new_meeting.end_time > meeting.start_time):
                return False
            

        # Если пересечений нет, добавляем встречу
        self.schedule.append(new_meeting)
        new_meeting.participants.append(self)
        return True

    def get_schedule(self):
        # Сортируем встречи по дате и времени начала
        sorted_schedule = sorted(
            self.schedule,
            key=lambda meeting: datetime.datetime.combine(meeting.date, meeting.start_time)
        )

        # Форматируем встречи в строки
        result = []
        for meeting in sorted_schedule:
            schedule_entry = (
                f"{meeting.date} "
                f"{meeting.start_time.strftime('%H:%M')} - "
                f"{meeting.end_time.strftime('%H:%M')}: "
                f"{meeting.name}"
            )
            result.append(schedule_entry)

        return result
