from sqlalchemy.orm import Session
from dto import word
from model.word import Word

#Все слова
def get_all_words(db: Session):
    return db.query(Word).all()

def get_word_by_id(id: int, db: Session):
    return db.query(Word).filter(Word.id == id).first()

def add_word(data: word.Word, db: Session):
    new_word = __word_from_dto(data)
    try:
        db.add(new_word)
        db.commit()
        db.refresh(new_word)
    except Exception as e:
        print(e)
    return new_word

def delete_word(id: int, db: Session):
    deleted_word = db.query(Word).filter(Word.id == id).delete()
    db.commit()
    return deleted_word

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



def __word_from_dto(dto_model: word.Word, model: Word = None):
    if model:
        model.name = dto_model.name
        model.meaning = dto_model.meaning
        return model
    else:
        return Word(
        id = dto_model.id,
        word = dto_model.name,
        meaning = dto_model.meaning
        )
