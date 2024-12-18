from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, Body, File, Form
from sqlalchemy.orm import Session
from database.database import get_connection
from api import service
from dto import word as wordDto
from dto import user as userDto
from dto import suggest_word as suggestDto
from pydantic import BaseModel

class FileRequestBody(BaseModel):
    file_path: str

routers = APIRouter()

@routers.head('/')
@routers.get('/', tags=['start'])
async def start():
    return {'message', 'successfuly connected'}

@routers.post('/', tags=['word'])
async def add_word(word: wordDto.Word, db: Session = Depends(get_connection)):
    return service.add_word(data = word, db = db)

@routers.post('/{id}', tags=['word'])
async def update_word(word: wordDto.Word, id: int = None, db: Session = Depends(get_connection)):
    return service.update_word(data = word, id = id, db = db)

@routers.get('/words/', tags=['word'])
async def get_all_words(page: int = 0, size: int = 100, db: Session = Depends(get_connection)):
    return service.get_all_words(db = db, page = page, size=size)

@routers.get('/words_count/', tags=['word'])
async def all_words_count(db: Session = Depends(get_connection)):
    return service.words_count(db)

@routers.get('/words_count/{name}', tags=['word'])
async def words_count_by_name(name: str, db: Session = Depends(get_connection)):
    return service.words_count_by_name(name, db)

@routers.get('/get_words/{name}', tags=['word'])
async def words(name: str, db: Session = Depends(get_connection), page: int = 0, size: int = 100):
    return service.get_words(name, db, page, size)

@routers.get('/{id}', tags=['word'])
async def get_word_by_id(id: int = None, db: Session = Depends(get_connection)):
    return service.get_word_by_id(id, db)

@routers.get('/words/{name}', tags=['word'])
async def get_words_by_name(name: str, page: int = 0, size: int = 100, db: Session = Depends(get_connection)):
    return service.get_word_by_name(name=name, db=db, page=page, size=size)

@routers.post('/suggest_word/', tags=['suggest'])
async def suggest_word(suggest: suggestDto.SuggestWord, db: Session = Depends(get_connection)):
    return service.add_suggets_word(data = suggest, db = db)

@routers.get('/suggests_count/', tags=['suggest'])
async def suggest_count(name: str, db: Session = Depends(get_connection)):
    return service.suggest_size(name, db)

@routers.get('/suggests/', tags=['suggest'])
async def suggests(name: str = '', page: int = 0, size: int = 15, db: Session = Depends(get_connection)):
    return service.get_suggest_words(name, db, page, size)

@routers.post('/reject_suggest/', tags=['suggest'])
async def reject_suggest(id: int, db: Session = Depends(get_connection)):
    return service.reject_suggest_word(id, db)

@routers.post('/accept_suggest/', tags=['suggest'])
async def accept_suggest(id: int, db: Session = Depends(get_connection)):
    return service.accept_suggest_word(id, db)

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

@routers.get('/send_restore_code/', tags=['auth'])
async def send_password_restore_code(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_connection)):
    return await service.send_restore_code(email=email, background_tasks=background_tasks, db=db)

@routers.post('/update_password/', tags=['auth'])
async def update_user_password(email: str, password: str, db: Session = Depends(get_connection)):
    return service.update_user_password(email=email, password=password, db=db)

@routers.get('/hash_password/', tags=['helpers'])
async def hash_password(password: str):
    return service.hash_password(password=password)