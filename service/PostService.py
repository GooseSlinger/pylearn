from sqlalchemy.orm import Session
from models.Post import Post
from models.User import User
from schemas.PostSchema import CreatePost
from schemas.BaseSchema import ResponseMessage
from fastapi import HTTPException

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, user_id: int, post: CreatePost):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        post = Post(title=post.title, content=post.content, user_id=user.id)

        self.db.add(post)
        self.db.commit()
        
        return ResponseMessage(message="Статья создана успешно")
    
    def show_posts(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        return user.posts
    
    def delete_post(self, id: int):
        post = self.db.query(Post).filter(Post.id == id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Статья не найдена")
        
        self.db.delete(post)
        self.db.commit()
        
        return ResponseMessage(message='Статья успешно удалена')
    
    def show_all_posts(self, page: int):
        limit = 5
        offset = (page -1) * limit
        posts = self.db.query(Post).offset(offset).limit(limit).all()

        return posts