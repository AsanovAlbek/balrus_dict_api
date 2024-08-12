from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text
from database.database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, name="id", primary_key=True, index=True, autoincrement=True)
    name = Column(Text, name="name", index=True)
    email = Column(Text, name="email", index=True)
    password = Column(Text, name="password", index=True)
    imei = Column(Text, name="imei", index=True)