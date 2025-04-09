from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    avatar = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True)

    posts = relationship('Post', back_populates='owner', cascade="all, delete")
