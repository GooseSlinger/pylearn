from database import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

post_category = Table(
    'post_category',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('category_id', Integer, ForeignKey('categorys.id'))
)

class Category(Base):
    __tablename__ = 'categorys'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True ,index=True)

    posts = relationship('Post', secondary='post_category', back_populates='categorys')
