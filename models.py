from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.schema import UniqueConstraint
from database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key = True)
    key = Column(String, unique = True, index = True)
    secret_key = Column(String, unique = True, index = True)
    target_url = Column(String, index = True, nullable = False)
    is_active = Column(Boolean, default = True)
    clicks = Column(Integer, default = 0)


    __table_args__ = (UniqueConstraint("target_url", name = "uq_target_url"),)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    user_name = Column(String, unique = True, index = True)
    email = Column(String, unique = True, index = True)
    hashed_password = Column(String, nullable = False)
    active = Column(Boolean, default = True)