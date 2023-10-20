from sqlalchemy import Column, Integer, String, ForeignKey

from models.Base import Base


class UserToSubject(Base):
    __tablename__ = "user_to_subject"
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"))
