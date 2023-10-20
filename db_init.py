from settings import *
from models.Base import Base
from models.Group import Group
import json


def init():
    try:
        Base.metadata.create_all(db)
    except:
        Base.metadata.drop_all(db)
        Base.metadata.create_all(db)
    with open("plan.json", "r") as file:
        data = json.loads(file.read())

    for group in list(data):
        grp = Group(name=group)
        if not session.query(Group).filter_by(name=group):
            session.add(grp)
    session.commit()
