from sqlalchemy.orm import  relationship
from sqlalchemy.sql import expression

from  app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)

    title = Column(String(100), nullable=False)
    content = Column(String(250), nullable=False)
    published = Column(Boolean,  nullable=True, server_default=expression.true(), default=1)
    created_at = Column(TIMESTAMP(timezone= True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,  ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False )

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String(20))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE" ), primary_key=True)

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
