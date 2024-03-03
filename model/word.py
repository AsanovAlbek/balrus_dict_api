from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text
from database import Base

class Word(Base):
    __table_name__ = 'balk'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, name='Name', index=True)
    meaning = Column(Text, name='TOLK', index=True)