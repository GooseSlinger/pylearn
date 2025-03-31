from sqlalchemy.orm import Session
from models.User import User
from schemas.UserSchema import UserCreate, UserPatch
from schemas.BaseSchema import ResponseMessage
from fastapi import HTTPException, UploadFile
import os
import uuid
from typing import List


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(name=user.name, email=user.email)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def get_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        return user

    def get_all_users(self):
        return self.db.query(User).all()

    def update_user(self, user_id: int, user: UserCreate):
        db_user = self.db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        db_user.name = user.name
        db_user.email = user.email

        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def patch_user(self, user_id: int, user: UserPatch):
        db_user = self.db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if user.name:
            db_user.name = user.name
        if user.email:
            db_user.email = user.email
            
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
    
    def delete_user(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        self.db.delete(db_user)
        self.db.commit()

        return ResponseMessage(message='Пользователь успешно удален')
    
    async def upload_avatar(self, id: int, file):
        db_user = self.db.query(User).filter(User.id == id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        directory = "storage/avatars"
        os.makedirs(directory, exist_ok=True)

        for item in file:
            _, ext = os.path.splitext(item.filename)
            ext = ext.lower()
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            file_location = os.path.join(directory, unique_filename)

            content = await item.read()
            with open(file_location, "wb") as f:
                f.write(content)

        # Сохраняем путь в БД
        db_user.avatar = f"/avatars/{unique_filename}"
        self.db.commit()
            
        return ResponseMessage(message=f'Аватар успешно загружен по пути {file_location}')
    
    async def save_uploaded_files(self, files: List[UploadFile]):
        directory = "storage/uploads"
        os.makedirs(directory, exist_ok=True)

        for file in files:
            _, ext = os.path.splitext(file.filename)
            ext = ext.lower()
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            file_location = os.path.join(directory, unique_filename)

            content = await file.read()
            with open(file_location, "wb") as f:
                f.write(content)

        return ResponseMessage(message="Изображения успешно загружены")

