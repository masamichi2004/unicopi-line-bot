from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    line_id: str
    answered_enquete: Optional[bool] = False