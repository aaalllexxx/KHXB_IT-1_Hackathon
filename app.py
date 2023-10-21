import os
import uuid
from hashlib import sha256
from typing import Optional

import jwt
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder

from main import ScheduleGenerator
from models.Access import Access
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


class LoginReq(BaseModel):
    login: str
    password: str


class RegisterReq(BaseModel):
    login: str
    password: str
    name: str
    OAuth: Optional[str] = ""
    group: str


class LessonReq(BaseModel):
    position: str
    name: str
    auditory: int
    tag: str = ""
    group: int
    teacher: int


class SessionReq(BaseModel):
    token: str


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


@app.post("/user/login")
def login_user(data: LoginReq):
    user = session.query(User).filter_by(login=data.login).first()
    if user and sha256(data.password.encode()).hexdigest() == user.password:
        token = jwt.encode({"user_id": user.id, "pass": user.password}, jwt_secret, algorithm="HS256")
        return {"session": token}
    return {"status_code": 403, "message": "Unauthorized"}


@app.post("/user/login/oauth")
def login_oauth():
    pass


@app.post("/user/session/check")
def check_session(data: SessionReq):
    if data.token:
        data = jwt.decode(data.token, jwt_secret, algorithms=["HS256"])
        if isinstance(data, dict):
            user_id = data.get("user_id")
            password = data.get("pass")
            user = session.query(User).filter_by(id=user_id).first()
            if user and user.password == password:
                return {"status_code": 200, "message": "Success"}
        return {"status_code": 403, "message": "Unauthorized"}
    return {"status_code": 401, "message": "Bad request"}


@app.put("/user/edit/{lesson_id}")
async def edit_lesson(lesson_id: int, data: LessonReq):
    lesson = session.query(Lesson).filter_by(id=lesson_id).first()
    if not lesson:
        return {"status_code": 404, "message": "Not found"}
    if data.group:
        lesson.group = data.group
    if data.name:
        lesson.name = data.name
    if data.teacher:
        lesson.teacher = data.teacher
    if data.position:
        lesson.position = data.position
    if data.tag:
        lesson.tag = data.tag
    if data.auditory:
        lesson.auditory = data.auditory
    session.commit()
    return {"status_code": 200, "message": "Success"}


@app.delete("/user/delete/{user_id}")
def delete_user_by_id(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        return {"status_code": 404, "message": "Not found"}
    session.delete(user)
    return {"status_code": 200, "message": "Success"}


@app.get("/access/{ident}")
def get_access(ident: int):
    access = session.query(Access).filter_by(id=ident).first()
    return jsonable_encoder(access)


if __name__ == "__main__":
    os.system("uvicorn app:app")
