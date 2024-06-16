from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    user_id: str
    gender: Optional[str] = None
    univ: Optional[str] = None
    grade: Optional[str] = None
    answered_enquete: Optional[bool] = False

def newMongoClient() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_URI"), tlsAllowInvalidCertificates=True)
    return client


user = User(
    user_id='temp_test',
    gender='男性',
    univ='東京大学',
    grade='4回生'
)

client = newMongoClient()
db = client['LINE']

collection = db['User']

collection.insert_one(user.__dict__)