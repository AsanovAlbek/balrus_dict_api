from sqlalchemy.orm import Session
from sqlalchemy import func
from dto import word
from model.word import Word

#Все слова
def get_all_words(db: Session, page: int = 0, size: int = 100):
    skip = page * size
    return db.query(Word).order_by(Word.name).offset(skip).limit(size).all()

#Количество записей в бд
def words_count(db: Session):
    return db.query(func.count(Word.id)).scalar()

#Количество записей в бд, включающих в себя name
def words_count_by_name(name: str, db: Session):
    return db.query(func.count(Word.id)).filter(Word.name.ilike(name + '%')).scalar()

#Найти слово по id
def get_word_by_id(id: int, db: Session):
    return db.query(Word).filter(Word.id == id).first()

#Поиск слова
def get_word_by_name(name: str, db: Session, page: int = 0, size: int = 100):
    skip = page * size
    return db.query(Word).filter(Word.name.ilike(name + '%')).order_by(Word.name).offset(skip).limit(size).all()

#Добавить слово
def add_word(data: word.Word, db: Session):
    new_word = __word_from_dto(data)
    try:
        db.add(new_word)
        db.commit()
        db.refresh(new_word)
    except Exception as e:
        print(e)
    return new_word

#Удалить слово
def delete_word(id: int, db: Session):
    deleted_word = db.query(Word).filter(Word.id == id).delete()
    db.commit()
    return deleted_word

#Обновить (изменить) слово
def update_word(data: word.Word, id: int, db: Session):
    wd = db.query(Word).filter(Word.id == id).first()
    wd = __word_from_dto(data, wd)
    try:
        db.add(wd)
        db.commit()
        db.refresh(wd)
    except Exception as e:
        print(e)

    return wd


#Копирование структуры word. Если слово model уже есть, то изменяем его
#Иначе создаём новый экземпляр
def __word_from_dto(dto_model: word.Word, model: Word = None):
    if model:
        model.name = dto_model.name
        model.meaning = dto_model.meaning
        return model
    else:
        return Word(
            id = dto_model.id,
            name = dto_model.name,
            meaning = dto_model.meaning
        )
