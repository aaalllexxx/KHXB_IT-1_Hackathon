import os

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from models.Lesson import Lesson
from settings import *

app = FastAPI()


@app.get("/get_lessons")
def get_lessons():
    lessons = session.query(Lesson).all()
    resp = []
    for l in lessons:
        resp.append(jsonable_encoder(l))
    return resp


if __name__ == "__main__":
    os.system("uvicorn app:app")
