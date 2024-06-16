from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    user_id: str
    gender: Optional[str] = None
    univ: Optional[str] = None
    grade: Optional[str] = None
    answered_enquete: Optional[bool] = False