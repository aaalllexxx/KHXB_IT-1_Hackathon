import os
from hashlib import sha256
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder

from main import ScheduleGenerator
from models.Group import Group
from models.Lesson import Lesson
from models.User import User
from pydantic import BaseModel
from settings import *

app = FastAPI()


class GroupReq(BaseModel):
    group: int


class TeacherReq(BaseModel):
    teacher: str


class RegisterReq(BaseModel):
    login: str
    password: str
    name: str
    OAuth: Optional[str] = ""
    group: str


@app.post("/get_group_lessons")
async def get_lessons(data: GroupReq):
    if data and hasattr(data, "group"):
        group = session.query(Group).where(Group.id == data.group).first()
        if not group:
            return {"status_code": 404, "message": "Not found"}
        lessons = session.query(Lesson).where(Lesson.group == group.id).all()
        resp = []
        for l in lessons:
            resp.append(jsonable_encoder(l))
        return resp
    return {"status_code": 401, "message": "Bad request"}


@app.post("/get_teacher_lessons")
async def get_lessons(data: TeacherReq):
    if data and hasattr(data, "teacher"):
        teacher = session.query(User).where(User.name == data.teacher).first()
        if not teacher:
            return {"status_code": 404, "message": "Not found"}
        lessons = session.query(Lesson).where(Lesson.teacher == teacher.id).all()
        resp = []
        for l in lessons:
            resp.append(jsonable_encoder(l))
        return resp
    return {"status_code": 401, "message": "Bad request"}


@app.get("/generate")
def generate():
    sg = ScheduleGenerator()
    a = sg.generate_all()
    print(a)
    if a is not None:
        return {"status_code": 404, "message": "Failed"}
    return {"status_code": 200, "message": "Success"}


@app.post("/user/register")
def register(model: RegisterReq):
    if model.login and model.password and model.name and model.group:
        login = model.login
        password = model.password
        name = model.name
        group = model.group
        group = session.query(Group).filter_by(name=group).first()
        if not group:
            return {"status_code": 404, "message": "Group not found"}
        group = group.id
        oauth = model.OAuth
        user = User(role=1, name=name, OAuth=oauth, login=login, password=sha256(password.encode("utf-8")).hexdigest(),
                    group=group)
        session.add(user)
        session.commit()
        return {"status_code": 200, "message": "Success"}
    return {"status_code": 401, "message": "Bad request"}


@app.get("/user/get/{user_id}")
def get_user_by_id(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        return {"status_code": 404, "message": "Not found"}
    return jsonable_encoder(user)


@app.delete("/user/delete/{user_id}")
def delete_user_by_id(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        return {"status_code": 404, "message": "Not found"}
    session.delete(user)
    return {"status_code": 200, "message": "Success"}


if __name__ == "__main__":
    os.system("uvicorn app:app")
