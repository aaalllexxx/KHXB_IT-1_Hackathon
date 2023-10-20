from calendar import isleap
from datetime import date

import dotenv
from holidays_ru import check_holiday
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

env = dotenv.dotenv_values(".env")
uri = env.get("DATABASE_URI")
db = create_engine(uri)
Session = sessionmaker(db)
session = Session()
db.connect()
month_list = [31, 28 if isleap(date.today().year) else 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
this_year = date.today().year
days_in_year = 366 if isleap(this_year) else 365

sem_1_starts = date(this_year, 9, 1)
sem_1_finishes = date(this_year, 12, 31)
sem_2_starts = date(this_year, 1, 23)
sem_2_finishes = date(this_year, 6, 30)
sem_1_step = -1 if sem_1_finishes.month < sem_1_starts.month else 1
sem_2_step = -1 if sem_2_finishes.month < sem_2_starts.month else 1

holidays_1 = [check_holiday(date(this_year, m, d)) for m in
              range(sem_1_finishes.month, sem_1_finishes.month, sem_1_step) for d in
              month_list[m]].count(True)

holidays_2 = [check_holiday(date(this_year, m, d)) for m in
              range(sem_2_finishes.month, sem_2_finishes.month, sem_2_step) for d in
              month_list[m]].count(True)

sem = 1 if sem_1_starts <= date.today() <= sem_1_finishes else 2 if sem_2_starts <= date.today() <= sem_2_finishes else 0
