from models.Base import Base
from settings import *
from models.User import User
from models.Access import Access
from models.Auditory import Auditory
from models.Lesson import Lesson
from models.Group import Group

class Teacher:
    def __init__(self, name):
        self.name = name
        self.lessons = []

    def __repr__(self):
        return f'Teacher({self.name})'


class Lesson:
    def __init__(self, name, teacher, position, auditory=0):
        self.name = name
        self.teacher = teacher
        self.position = position
        teacher.lessons.append(position)
        self.auditory = auditory

    def __repr__(self):
        return f"Lesson({self.name}, {self.teacher}, {self.position}, {self.auditory})"


class Day:
    def __init__(self, *lessons):
        self.__items = list(lessons)

    def append(self, value) -> None:
        self.__items.append(value)

    def pop(self, index) -> Lesson:
        return self.__items.pop(index)

    def insert(self, index, value) -> None:
        if index < len(self.__items):
            self.__items.insert(index, value)
        else:
            for i in range(len(self.__items), index):
                self.append(0)
            self.append(value)

    def __setitem__(self, key, value):
        self.__items[key] = value

    def __getitem__(self, item) -> Lesson:
        return self.__items[item]

    def __repr__(self):
        return f"Day({[i for i in self.__items if i is not None]})"


class Week:
    def __init__(self, monday=None, tuesday=None, wednesday=None, thursday=None, friday=None, saturday=None,
                 sunday=None):
        self.__days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        self.list = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday

    def __setattr__(self, item, value):
        self.__dict__[item] = value
        if item in self.__days:
            self.list[self.__days.index(item)] = value

    def __repr__(self):
        return f"Week({self.list})"


class PlanElement:
    def __init__(self, name, count):
        self.name = name
        self.count = count


class Plan:
    def __init__(self, plan: list[PlanElement]):
        self.plan = plan


class Schedule:
    def __init__(self, schedule):
        self.schedule = schedule


class ScheduleGenerator:
    def __init__(self):
        self.generated = []

    def generate_all(self) -> list[Schedule]:
        pass

    def generate_for_group(self, group_name) -> Schedule:
        pass


if __name__ == "__main__":
    if env.get("MODE") == "TEST":
        Base.metadata.drop_all(db)
    Base.metadata.create_all(db)
