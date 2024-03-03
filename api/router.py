from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_connection
from api import service
from dto import word as wordDto

routers = APIRouter()

@routers.post('/', tags=['word'])
async def add_word(data: wordDto.Word, db: Session = Depends(get_connection)):
    return service.add_word(data, db)

@routers.get('/words', tags=['word'])
async def get_all_words(db: Session = Depends(get_connection)):
    return service.get_all_words(db)

@routers.get('/{id}', tags=['word'])
async def get_word_by_id(id: int = None, db: Session = Depends(get_connection)):
    return service.get_word_by_id(id, db)

@routers.get('/words/{name}', tags=['word'])
async def get_words_by_name(name: str, db: Session = Depends(get_connection)):
    return service.get_word_by_name(name, db)

@routers.delete('/{id}', tags=['word'])
async def delete_word(id: int = None, db: Session = Depends(get_connection)):
    return service.delete_word(id, db)

@routers.put('{id}', tags=['word'])
async def update_word(data: wordDto.Word, id: int = None, db: Session = Depends(get_connection)):
    return service.update_word(data, id, db)