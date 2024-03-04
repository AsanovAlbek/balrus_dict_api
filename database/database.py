from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
import database.config as config
engine = create_engine(config.DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_connection():
    connection = Session()
    try:
        yield connection
    except Exception as e:
        print(e)
    finally:
        connection.close()

class Base(DeclarativeBase):
    ...