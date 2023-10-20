import json

from db_init import init
from models.Base import Base
from models.Subject import Subject
from settings import *
from models.User import User
from models.Access import Access
from models.Auditory import Auditory
from models.Lesson import Lesson
from models.Group import Group
from holidays_ru import check_holiday


class ScheduleGenerator:
    def __init__(self):
        self.generated = []

    def generate_all(self):
        pass

    def generate_for_group(self):
        plan = session.query(Subject).all()
        for months in range(12):
            for day in range(month_list[months]):
                if check_holiday(date(date.today().year, months, day)):
                    continue




if __name__ == "__main__":
    init()
