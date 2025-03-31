from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from service.PostService import PostService
from schemas.PostSchema import CreatePost
from schemas.BaseSchema import ResponseMessage
from typing import List


router = APIRouter()

def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)

@router.post("/create/{user_id}", response_model=ResponseMessage)
async def create_post(user_id: int, post: CreatePost, service: PostService = Depends(get_post_service)):
    return service.create_post(user_id, post)

@router.get("/show/{user_id}", response_model=List[CreatePost])
async def show_posts(user_id: int, service: PostService = Depends(get_post_service)):
    return service.show_posts(user_id)

@router.delete("/delete/{id}", response_model=ResponseMessage)
async def delete_post(id: int, service: PostService = Depends(get_post_service)):
    return service.delete_post(id)
