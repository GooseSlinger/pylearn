from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from schemas.UserSchema import UserCreate, GetUser, UserPatch
from schemas.BaseSchema import ResponseMessage
from typing import List
from service.UserService import UserService
from middleware.jwt import verify_token
from utils.FileValidator import FileValidator

router = APIRouter()

# DI функция для прокидывания UserService
def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

@router.post("/create")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks, service: UserService = Depends(get_user_service)):
    return service.create_user(user, background_tasks)

@router.get("/get/{id}", response_model=GetUser)
async def get_user(id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(id)

@router.get("/get_all", response_model=List[GetUser])
async def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.put("/update/{id}", response_model=GetUser)
async def update_user(id: int, user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.update_user(id, user)

@router.patch("/patch/{id}", response_model=GetUser)
async def patch_user(id: int, user: UserPatch, service: UserService = Depends(get_user_service)):
    return service.patch_user(id, user)

@router.delete("/delete/{user_id}", response_model=ResponseMessage)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)

@router.post("/{id}/upload_avatar", response_model=ResponseMessage)
async def upload_avatar(
    id: int,
    file: List[UploadFile] = Depends(FileValidator(allowed_extensions={"jpg"}, count=1)),
    service: UserService = Depends(get_user_service),
):
    return await service.upload_avatar(id, file)

@router.post("/upload_images", response_model=ResponseMessage, dependencies=[Depends(verify_token)])
async def upload_images(
    files: List[UploadFile] = Depends(FileValidator(allowed_extensions={"jpg"})),
    service: UserService = Depends(get_user_service)
):
    return await service.save_uploaded_files(files)
