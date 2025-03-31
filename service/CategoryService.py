from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.CategorySchema import CreateCategory
from schemas.BaseSchema import ResponseMessage
from models.Category import Category
from models.Post import Post

class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category: CreateCategory):
        db_category = self.db.query(Category).filter(Category.name == category.name).first()
    
        if db_category:
            raise HTTPException(status_code=400, detail="Категория уже существует")
        
        category = Category(name=category.name)

        self.db.add(category)
        self.db.commit()

        return ResponseMessage(message='Категория успешно создана')
    
    def show_categorys(self):
        return self.db.query(Category).all()
    
    def delete_category(self, id: int):
        category = self.db.query(Category).filter(Category.id == id).first()

        if not category:
            raise HTTPException(status_code=400, detail="Категория уже не существует")

        self.db.delete(category)
        self.db.commit()

        return ResponseMessage(message='Категория успешно удалена')
    
    def append_category(self, post_id: int, category_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Поста не существует")
        
        category = self.db.query(Category).filter(Category.id == category_id).first()

        if not category:
            raise HTTPException(status_code=404, detail="Категории не существует")
        
        if post in category.posts:
            raise HTTPException(status_code=400, detail="Категория уже присвоена посту")

        category.posts.append(post)
        self.db.commit()

        return ResponseMessage(message='Категория успешно присвоена')
    
    def remove_category(self, post_id: int, category_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Поста не существует")
        
        category = self.db.query(Category).filter(Category.id == category_id).first()

        if not category:
            raise HTTPException(status_code=404, detail="Категории не существует")
        
        if not post in category.posts:
            raise HTTPException(status_code=400, detail="Категория поста уже удалена")

        category.posts.remove(post)
        self.db.commit()

        return ResponseMessage(message='Категория успешно удалена с поста')
    
    def check_category_post(self, category_id: int):
        category = self.db.query(Category).filter(Category.id == category_id).first()

        if not category:
            raise HTTPException(status_code=400, detail="Категории не существует")

        return category.posts