from fastapi import APIRouter, Depends, UploadFile, Body, File, Form
from sqlalchemy.orm import Session
from database.database import get_connection
from api import service
from dto import word, user, favorite_word
from pydantic import BaseModel

class FileRequestBody(BaseModel):
    file_path: str

routers = APIRouter()

@routers.head('/')
@routers.get('/')
async def init():
    return {'message', 'connected successfuly'}

@routers.post('/', tags=['word'])
async def add_word(word: word.Word, db: Session = Depends(get_connection)):
    return service.add_word(data = word, db = db)

@routers.post('/{id}', tags=['word'])
async def update_word(word: word.Word, id: int = None, db: Session = Depends(get_connection)):
    return service.update_word(data = word, id = id, db = db)

@routers.get('/words', tags=['word'])
async def get_all_words(page: int = 0, size: int = 100, db: Session = Depends(get_connection)):
    return service.get_all_words(db = db, page = page, size=size)

@routers.get('/words_count', tags=['word'])
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
async def register_new_user(data: user.User, db: Session = Depends(get_connection)):
    return service.register_user(data=data, db=db)

@routers.get('/user/', tags=['auth'])
async def get_user(email: str, password: str, db: Session = Depends(get_connection)):
    return service.get_user(email=email, password=password, db=db)

@routers.get('/user/{user_id}', tags=['auth'])
async def get_user_by_id(user_id: int, db: Session = Depends(get_connection)):
    return service.get_user_by_id(user_id=user_id, db=db)

@routers.get('/favorite_words/', tags=['favorites'])
async def get_favorite_words(user_id: int, db: Session = Depends(get_connection)):
    return service.get_favorite_words(user_id=user_id, db=db)

@routers.post('/add_favorite_word/', tags=['favorites'])
async def add_favorite_word(favorite_word: favorite_word.FavoriteWord, db: Session = Depends(get_connection)):
    return service.add_to_favorites(data=favorite_word, db=db)

@routers.delete('/delete_favorite_word/', tags=['favorites'])
async def remove_favorite(user_id: int, word_id: int, db: Session = Depends(get_connection)):
    return service.remove_from_favorites(user_id=user_id, word_id=word_id, db=db)
