from pydantic import BaseModel

class FavoriteWord(BaseModel):
    id: int
    user_id: int
    word_id: int