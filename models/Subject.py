from sqlalchemy import Column, Integer, String, ForeignKey

from models.Base import Base


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    teacher_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    count = Column(Integer)
    tags = Column(String(32))
    group = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"))
