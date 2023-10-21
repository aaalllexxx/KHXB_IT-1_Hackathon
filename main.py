import datetime
import json
from hashlib import sha256

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
from datetime import timedelta


class ScheduleGenerator:
    def __init__(self):
        self.generated = []

    def generate_all(self):
        session.query(Lesson).delete()
        session.commit()
        groups = session.query(Group).all()
        for grp in groups:
            self.generate_for_group(grp.name)

    def generate_for_group(self, group):
        group = session.query(Group).filter_by(name=group).first()
        subjects = session.query(Subject).filter_by(group=group.id).all()
        if sem == 1:
            start = sem_1_starts
            end = sem_1_finishes
            length = (end - start).days
        elif sem == 2:
            start = sem_2_starts
            end = sem_2_finishes
            length = (end - start).days
        else:
            if date.today() < sem_1_finishes:
                start = sem_1_starts
                end = sem_1_finishes
                length = (end - start).days
            else:
                start = sem_2_starts
                end = sem_2_finishes
                length = (end - start).days

        for subject in subjects:
            req = subject.count
            step = length // subject.count
            step_inc = 1
            d = start + timedelta(days=step * step_inc)
            while check_holiday(d):
                d = d + timedelta(days=1)
            for month in range(start.month, end.month + 1):
                for day in range(1, month_list[month - 1] + 1):
                    if check_holiday(date(this_year, month, day)):
                        continue
                    current_date = date(this_year, month, day)
                    if current_date == d:
                        ctime = current_date.strftime('%Y-%m-%d')
                        pair = 1
                        while pair < max_pairs_per_day:
                            identifier = f"{ctime}-{pair}"
                            same_lessons = session.query(Lesson).where(Lesson.position == identifier).where(
                                Lesson.teacher == subject.teacher_id).all()
                            day_lessons = session.query(Lesson).where(Lesson.group == subject.group).where(
                                Lesson.position.startswith(ctime)).all()
                            if same_lessons or pair < len(day_lessons):
                                pair += 1
                                continue
                            break
                        else:
                            d = d + timedelta(days=1)
                            while check_holiday(d):
                                d = d + timedelta(days=1)
                            if d > end:
                                d = d - timedelta(days=1)
                                while check_holiday(d):
                                    d = d - timedelta(days=1)
                            continue

                        auditories = session.query(Auditory).where(Auditory.size >= group.students).where(
                            Auditory.tag == (subject.tags or None)).all()
                        auditories = sorted(auditories, key=lambda x: x.size)
                        if auditories:
                            ind = 0
                            for a in range(len(auditories)):
                                same_aud = session.query(Lesson).where(Lesson.position.startswith(identifier)).where(
                                    Lesson.auditory == auditories[a].id).all()
                                if not same_aud:
                                    ind = a
                                    break
                            else:
                                while check_holiday(d):
                                    d = d + timedelta(days=1)
                                if d > end:
                                    d = d - timedelta(days=1)
                                    while check_holiday(d):
                                        d = d - timedelta(days=1)
                                continue

                            les = Lesson(position=identifier, name=subject.name, auditory=auditories[ind].id,
                                         tag=subject.tags, group=group.id, teacher=subject.teacher_id)
                            session.add(les)
                            session.commit()
                            step_inc += 1
                            req -= 1
                            d = start + timedelta(days=step * step_inc)
                            while check_holiday(d):
                                d = d + timedelta(days=1)
                            if d > end:
                                d = d - timedelta(days=1)
                                while check_holiday(d):
                                    d = d - timedelta(days=1)
                        else:
                            d = start + timedelta(days=step * step_inc)
                            while check_holiday(d):
                                d = d + timedelta(days=1)
                            if d > end:
                                d = d - timedelta(days=1)
                                while check_holiday(d):
                                    d = d - timedelta(days=1)
                    else:
                        d = start + timedelta(days=step * step_inc)
                        while check_holiday(d):
                            d = d + timedelta(days=1)
                        if d > end:
                            d = d - timedelta(days=1)
                            while check_holiday(d):
                                d = d - timedelta(days=1)
        data_lesson = session.query(Lesson).where(Lesson.group == group.id).all()
        subjects = session.query(Subject).where(Subject.group == group.id).all()
        subjects = [sub.count for sub in subjects]
        if sum(subjects) > len(data_lesson):
            return False


if __name__ == "__main__":
    sg = ScheduleGenerator()
    sg.generate_all()
    group = session.query(Group).filter_by(name="K0409-22").first()
    sch = session.query(Lesson).filter_by(group=group.id).all()
    count = 0
    for i in sch:
        data = session.query(Lesson).where(Lesson.position == i.position).where(Lesson.teacher == i.teacher).all()
        if len(data) > 1:
            count += 1
    print(count)
