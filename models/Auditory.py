from sqlalchemy import Column, Integer, String, ForeignKey

from models.Base import Base


class Auditory(Base):
    __tablename__ = "auditory"
    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)
    name = Column(String(120))
    tag = Column(String(32))

