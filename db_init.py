from settings import *
from models.Base import Base
from models.Group import Group
import json


def init():
    if env.get("MODE") == "TEST":
        Base.metadata.drop_all(db)
    Base.metadata.create_all(db)
    with open("plan.json", "r") as file:
        data = json.loads(file.read())
    for group in list(data):
        grp = Group(name=group)
        session.add(grp)
    session.commit()
