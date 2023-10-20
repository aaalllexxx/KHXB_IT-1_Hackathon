from sqlalchemy import Column, Integer, String, ForeignKey

from models.Base import Base


class Access(Base):
    __tablename__ = "access"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))

