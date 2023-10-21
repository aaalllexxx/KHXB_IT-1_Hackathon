import os

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from models.Group import Group
from models.Lesson import Lesson
from settings import *

app = FastAPI()


@app.get("/get_lessons")
def get_lessons():
    groups = session.query(Group).all()
    resp = {}

    for group in groups:
        lessons = session.query(Lesson).filter_by(group=group.id).all()
        for l in lessons:
            pass
        resp[group.name] = None
    return resp


if __name__ == "__main__":
    os.system("uvicorn app:app")
