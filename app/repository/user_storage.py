from pymongo import MongoClient
from app.entities.user.user import User
from typing import Any


class UserStorageRepository:
    def __init__(self, cli: MongoClient):
        self.cli = cli
        self.db = self.cli['LINE']
        self.user_collection = self.db['AnsweredUser-2024']
        
    def find_user(self, line_id: str) -> Any:
        return self.user_collection.find_one({'line_id': line_id})
    
    def register_user(self, line_id: str) -> None:
        self.user_collection.insert_one(
            User(line_id=line_id, answered_enquete=True).__dict__
        )
        return "OK"