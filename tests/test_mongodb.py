from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional, Any

load_dotenv()


class User(BaseModel):
    line_id: str
    answered_enquete: Optional[bool] = False


class TestUserStorageRepository:
    def __init__(self, cli: MongoClient):
        self.cli = cli
        self.db = self.cli["LINE"]
        self.user_collection = self.db["User"]

    def find_user(self, line_id: str) -> Any:
        return self.user_collection.find_one({"user_id": line_id})

    def register_user(self, line_id: str) -> None:
        self.user_collection.insert_one(
            User(line_id=line_id, answered_enquete=True).__dict__
        )
        return "OK"


def testMongoClient() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_URI"), tlsallowinvalidcertificates=True)
    return client

user_storage = TestUserStorageRepository(testMongoClient())

tmp = user_storage.find_user("aaaa")
print(tmp)
