from fastapi import APIRouter, Depends
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from service.CategoryService import CategoryService
from schemas.BaseSchema import ResponseMessage
from schemas.CategorySchema import CreateCategory, ShowCategoty
from schemas.PostSchema import ShowPosts

router = APIRouter()

def get_category_service(db: Session = Depends(get_db)):
  return CategoryService(db)

@router.post('/create', response_model=ResponseMessage)
async def create_category(category: CreateCategory, service: CategoryService = Depends(get_category_service)):
  return service.create_category(category)

@router.get('/show_all', response_model=List[ShowCategoty])
async def show_categorys(service: CategoryService = Depends(get_category_service)):
  return service.show_categorys()

@router.delete('/delete/{id}', response_model=ResponseMessage)
async def delete_category(id: int, service: CategoryService = Depends(get_category_service)):
  return service.delete_category(id)

@router.post('/append/category/{category_id}/post/{post_id}', response_model=ResponseMessage)
async def append_category(post_id: int, category_id: int, service: CategoryService = Depends(get_category_service)):
  return service.append_category(post_id, category_id)

@router.post('/remove/category/{category_id}/post/{post_id}', response_model=ResponseMessage)
async def remove_category(category_id: int, post_id: int, service: CategoryService = Depends(get_category_service)):
  return service.remove_category(category_id, post_id)

@router.post('/check_category_post/{category_id}', response_model=List[ShowPosts])
async def check_category_post(category_id: int, service: CategoryService = Depends(get_category_service)):
  return service.check_category_post(category_id)