import paramiko.ssh_gss
from sqlalchemy.orm import Session
from sqlalchemy import func
from dto import word
from model.word import Word
from fastapi import UploadFile
from fastapi.responses import StreamingResponse, FileResponse, Response
from datetime import datetime
import traceback
import paramiko
import base64

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
        print(f'files {stfp_connection.listdir('/balrusapi/audio/')}')
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
        file_path: str = '/balrusapi/audio/' + str_date_time + '_' + file.filename
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
            file_path = word.audio_url
            if word.audio_url.split('/')[-1] in stfp_connection.listdir('/balrusapi/audio/'):
                stfp_connection.remove(file_path)
            word1 = word
            word1.audio_url = ''

            db.add(word1)
            db.commit()
            db.refresh(word1)
        else:
            print('word not founded')
        stfp_connection.close()
        ssh.close()
        return {'file_path': file_path}
    except Exception as e:
        #print(e)
        #print(traceback.format_exc())
        print(f'files = {stfp_connection.listdir_attr('/balrusapi/audio/')}')
        return {'file_path': 'error file_path'}


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
