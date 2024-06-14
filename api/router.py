from fastapi import APIRouter, Depends, UploadFile, Body, File, Form
from sqlalchemy.orm import Session
from database.database import get_connection
from api import service
from dto import word as wordDto
from dto import user as userDto
from pydantic import BaseModel

class FileRequestBody(BaseModel):
    file_path: str

routers = APIRouter()

@routers.post('/', tags=['word'])
async def add_word(word: wordDto.Word, db: Session = Depends(get_connection)):
    return service.add_word(data = word, db = db)

@routers.post('/{id}', tags=['word'])
async def update_word(word: wordDto.Word, id: int = None, db: Session = Depends(get_connection)):
    return service.update_word(data = word, id = id, db = db)

@routers.get('/words', tags=['word'])
async def get_all_words(page: int = 0, size: int = 100, db: Session = Depends(get_connection)):
    return service.get_all_words(db = db, page = page, size=size)

@routers.get('/words_count', tags=['word'])
async def all_words_count(db: Session = Depends(get_connection)):
    return service.words_count(db)

@routers.get('/words_count/{name}', tags=['word'])
async def words_count_by_name(name: str, db: Session = Depends(get_connection)):
    return service.words_count_by_name(name, db)

@routers.get('/{id}', tags=['word'])
async def get_word_by_id(id: int = None, db: Session = Depends(get_connection)):
    return service.get_word_by_id(id, db)

@routers.get('/words/{name}', tags=['word'])
async def get_words_by_name(name: str, page: int = 0, size: int = 100, db: Session = Depends(get_connection)):
    return service.get_word_by_name(name=name, db=db, page=page, size=size)

@routers.delete('/{id}', tags=['word'])
async def delete_word(id: int = None, db: Session = Depends(get_connection)):
    return service.delete_word(id = id, db = db)

@routers.post('/upload_file/', tags=['files'])
async def upload_file(file: UploadFile):
    return service.upload_file(file=file)

@routers.get('/get_file/', tags=['files'])
async def get_file(file_path: str):
    return service.get_file(file_path=file_path)

@routers.post('/delete_file/', tags=['files'])
async def delete_file(word_id: int, db: Session = Depends(get_connection)):
    return service.delete_file(word_id=word_id, db=db)

@routers.post('/register/', tags=['auth'])
async def register_new_user(data: userDto.User, db: Session = Depends(get_connection)):
    return service.register_user(data=data, db=db)

@routers.get('/user/', tags=['auth'])
async def get_user(email: str, password: str, db: Session = Depends(get_connection)):
    return service.get_user(email=email, password=password, db=db)

@routers.get('/user/{user_id}', tags=['auth'])
async def get_user_by_id(user_id: int, db: Session = Depends(get_connection)):
    return service.get_user_by_id(user_id=user_id, db=db)