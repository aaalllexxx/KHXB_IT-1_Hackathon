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
days_in_year = 366 if isleap(date.today().year) else 365
