from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text
from database.database import Base

class FavoriteWord(Base):
    __tablename__ = "users_favorite_words"

    id = Column(Integer, name="id", primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, name="user_id", index=True)
    word_id = Column(Integer, name="word_id", index=True)