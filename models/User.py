from sqlalchemy import Column, String, Integer, ForeignKey

from models.Base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    role = Column(Integer, ForeignKey("access.id", ondelete="CASCADE"))
    name = Column(String(128), nullable=False)
    OAuth = Column(String(256))
    login = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    group = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"))
