from sqlalchemy import Column, Integer, ForeignKey, String

from models.Base import Base


class Lesson(Base):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True)
    position = Column(String(64), nullable=False)
    name = Column(String(64), nullable=False)
    auditory = Column(Integer)
    tag = Column(String(32))
    group = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"))
    teacher = Column(Integer)
