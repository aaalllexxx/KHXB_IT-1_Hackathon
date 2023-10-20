from sqlalchemy import Column, Integer, String, ForeignKey

from models.Base import Base


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
