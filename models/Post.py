from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='posts', cascade="all, delete")
    categorys = relationship('Category', secondary='post_category', back_populates='posts')