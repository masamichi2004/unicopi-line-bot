from app.repository.userStorage.user_storage import UserStorageRepository
from app.entities.user.user import User
from pymongo import MongoClient
from typing import Any

class UserStorageRepositoryImpl(UserStorageRepository):
    def __init__(self, cli: MongoClient):
        self.cli = cli
    
    def register_user_from_line(self, user: User) -> Any:
        collection = self.cli['LINE']['User']
        return collection.insert_one(user.__dict__)
    
    def update_user_info(self, user: User) -> Any:
        collection = self.cli['LINE']['User']
        return collection.update_one({'user_id': user.user_id}, {'$set': user.__dict__})    
        
    
def NewUserStorageRepository(cli: MongoClient) -> UserStorageRepository:
    return UserStorageRepositoryImpl(cli=cli)