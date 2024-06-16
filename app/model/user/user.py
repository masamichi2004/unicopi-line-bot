from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    gender: str
    univ: str
    grade: str