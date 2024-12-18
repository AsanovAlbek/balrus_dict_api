import hashlib
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
import hashlib
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
import paramiko.ssh_gss
from sqlalchemy.orm import Session
from sqlalchemy import func
from dto import word, suggest_word
from model import mail_sender
from model.word import Word
from model.suggest_word import SuggestWord
from fastapi import UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse, Response
from datetime import datetime
import traceback
import paramiko
import base64
from dto import word, user
from model.user import User
from dto import word, user
from model.user import User

stfp_hostname = "31.41.63.47"
stfp_port = "7637"
stfp_username = "albek"
stfp_password = "albek8888"
audio_folder_url = "sftp://albek@31.41.63.47:7637/balrusapi/audio/"

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
    deleted_word = db.query(Word).filter(Word.id == id).first()
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=stfp_hostname, port=stfp_port, username=stfp_username, password=stfp_password)
        stfp_connection = ssh.open_sftp()
        if deleted_word.audio_url.split('/')[-1] in stfp_connection.listdir('/balrusapi/audio/'):
            stfp_connection.remove(deleted_word.audio_url)
        if deleted_word.audio_url.split('/')[-1] in stfp_connection.listdir('/balrusapi/audio/'):
            stfp_connection.remove(deleted_word.audio_url)
        stfp_connection.close()
        ssh.close()
        db.query(Word).filter(Word.id == id).delete()
        db.commit()
    except Exception as e:
        traceback.print_exc()
        traceback.print_stack()
    return deleted_word

    db.query(Word).filter(Word.id == id).delete()
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

# Добавить файл на сервер по sftp. Так же добавляет полученный url в соответствующую запись
def upload_file(file: UploadFile):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=stfp_hostname, port=stfp_port, username=stfp_username, password=stfp_password)
        stfp_connection = ssh.open_sftp()

        str_date_time = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        file_path: str = '/balrusapi/audio/' + str_date_time + '_rusbal_' + file.filename
        file_path: str = '/balrusapi/audio/' + str_date_time + '_rusbal_' + file.filename
        file_path = file_path.replace(' ', '_')
        stfp_connection.putfo(file.file, file_path)

        stfp_connection.close()
        ssh.close()
        return {'file_path': file_path}
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return {'file_path': f'error file_url {e}'}
    

#Получение файла по его пути
def get_file(file_path: str):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=stfp_hostname, port=stfp_port, username=stfp_username, password=stfp_password)
        stfp_connection = ssh.open_sftp()

        with stfp_connection.open(file_path, "rb") as remote_file:
            audio_bytes = remote_file.read()
            contents = base64.b64encode(audio_bytes).decode()

        stfp_connection.close()
        ssh.close()
        
        return {'filename' : file_path.split('/')[-1], 'contents': contents}

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return {'error': f'exception is {e}'}



#Удаление файла и очищение url в записи
def delete_file(word_id: int, db: Session):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=stfp_hostname, port=stfp_port, username=stfp_username, password=stfp_password)
        stfp_connection = ssh.open_sftp()

        word = db.query(Word).filter(Word.id == word_id).first()
        file_path = ''
        if word:
            print('word founded for delete')
            print('word founded for delete')
            file_path = word.audio_url
            if word.audio_url.split('/')[-1] in stfp_connection.listdir('/balrusapi/audio/'):
                stfp_connection.remove(file_path)
            word1 = word
            word1.audio_url = ''
            if word.audio_url.split('/')[-1] in stfp_connection.listdir('/balrusapi/audio/'):
                stfp_connection.remove(file_path)
            word1 = word
            word1.audio_url = ''

            db.add(word1)
            db.add(word1)
            db.commit()
            db.refresh(word1)
            db.refresh(word1)
        else:
            print('word not founded')
        stfp_connection.close()
        ssh.close()
        return {'file_path': file_path}
    except Exception as e:
        return {'file_path': 'error file_path'}
    
#Шифрование пароля
def hash_password(password: str):
    salt = 'user_password_salt'
    return hashlib.sha512(password.encode() + salt.encode()).hexdigest()
    

def register_user(data: user.User, db: Session):
    data.password = hash_password(data.password)
    new_user = __user_from_dto(data)
    try:
       is_user_exist = db.query(db.query(User).filter(User.email == new_user.email).exists()).scalar()
       if is_user_exist:
           return None
       if new_user.id == 0:
           new_user.id = None
       db.add(new_user)
       db.commit()
       db.refresh(new_user)
    except Exception as e:
       print(e)
    return new_user
    
def get_user(email: str, password: str, db: Session):
    u = db.query(User).filter(User.email == email).first()
    if u:
        hashed_password = hash_password(password)
        print(f'hashed password = {hashed_password} user password = {u.password}')
        if hashed_password == u.password:
            return u
    return None

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

async def send_restore_code(email: str, background_tasks: BackgroundTasks, db: Session):
    code = None
    try:
        # генерация 6ти значного кода
        code = random.randint(100000, 999999)
        # составление сообщения
        message = MessageSchema(
            subject='Код для восстановления пароля',
            body=f'Ваш код восстановления пароля {code}',
            recipients=[email],
            subtype=MessageType.plain
        )
        # создание отправителя сообщений
        sender = FastMail(mail_sender.mailconf)
        # отправка сообщения, бэкграунд таск для того,
        # чтобы не ожидать отправки сообщения
        # оно отправится даже после завершения функции
        background_tasks.add_task(sender.send_message, message)
    except Exception as e:
        print(e)
        raise e
    # Возвращаем код
    return {'restore_password_code' : code}

def update_user_password(email: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            hashed_password = hash_password(password)
            user.password = hashed_password
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            raise HTTPException(status_code=404, detail='Пользователь не найден')
    except Exception as e:
        print(e)
        raise e
        
def add_suggets_word(data: suggest_word.SuggestWord, db: Session):
    try:
        suggest = SuggestWord(
            id=0,
            word=data.word,
            meaning=data.meaning,
            user_id=data.user_id
        )
        db.add(suggest)
        db.commit()
        db.refresh(suggest)
        return suggest
    except Exception as e:
        print(e)
        raise e

def reject_suggest_word(id: int, db: Session):
    try:
        suggest = db.query(SuggestWord).filter(SuggestWord.id == id).first()
        db.query(SuggestWord).filter(SuggestWord.id == id).delete()
        db.commit()
        return suggest
    except Exception as e:
        print(e)
        raise e
    
def accept_suggest_word(id: int, db: Session):
    try:
        suggest = db.query(SuggestWord).filter(SuggestWord.id == id).first()
        if suggest:
            word = Word(
                name=suggest.word,
                meaning=suggest.meaning,
                audio_url = ''
            )
            db.add(word)
            db.query(SuggestWord).filter(SuggestWord.id == id).delete(synchronize_session=False)
            db.commit()
            db.refresh(word)
            return word
        else:
            return None
    except Exception as e:
        print(e)
        raise e
        
def get_suggest_words(name: str, db: Session, page: int= 0, size: int = 15):
    try:
        skip = page * size
        return db.query(SuggestWord).filter(SuggestWord.word.ilike(name + '%')).order_by(SuggestWord.word).offset(skip).limit(size).all()
    except Exception as e:
        print(e)
        raise e

def suggest_size(name: str, db: Session):
    return db.query(func.count(SuggestWord.id)).filter(SuggestWord.word.ilike(name + '%')).scalar()
        


#Копирование структуры word. Если слово model уже есть, то изменяем его
#Иначе создаём новый экземпляр
def __word_from_dto(dto_model: word.Word, model: Word = None):
    if model:
        model.name = dto_model.name
        model.meaning = dto_model.meaning
        model.audio_url = dto_model.audio_url
        return model
    else:
        return Word(
            id = dto_model.id,
            name = dto_model.name,
            meaning = dto_model.meaning,
            audio_url = dto_model.audio_url
        )

def __user_from_dto(dto_model: user.User, model: User = None):
    if model:
        model.username = dto_model.username
        model.email = dto_model.email
        model.password = dto_model.password
        model.imei = dto_model.imei
        return model
    else:
        return User(
            id = dto_model.id,
            username = dto_model.username,
            email = dto_model.email,
            password = dto_model.password,
            imei = dto_model.imei
        )
