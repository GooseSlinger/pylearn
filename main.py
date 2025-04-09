from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
import routes.UserRoute as User
import routes.PostRoute as Post
import routes.CategoryRoute as Category

app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Монтируем папку с аватарами
app.mount("/avatars", StaticFiles(directory="storage/avatars"), name="avatars")

# Подключаем роутеры
app.include_router(User.router, prefix="/user", tags=["User"])
app.include_router(Post.router, prefix="/post", tags=["Post"])
app.include_router(Category.router, prefix="/category", tags=["Category"])

# Простой рут
@app.get("/")
async def root():
    return {"message": "Hello world!"}
