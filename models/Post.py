from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='posts', cascade="all, delete")
    categorys = relationship('Category', secondary='post_category', back_populates='posts')