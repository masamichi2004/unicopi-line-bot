from app.repository.userStorage.user_storage import UserStorageRepository
from app.entities.user.user import User
from pymongo import MongoClient
from typing import Any, Dict

class UserStorageRepositoryImpl(UserStorageRepository):
    def __init__(self, cli: MongoClient):
        self.cli = cli
        
    def is_user_exist(self, user_id: str) -> bool:
        collection = self.cli['LINE']['User']
        user = collection.find_one({'user_id': user_id})
        if user:
            return True
        return False
    
    def register_user_from_line(self, user: User) -> Any:
        collection = self.cli['LINE']['User']
        return collection.insert_one(user.__dict__)
    
    def update_user_info(self, query: str, update_values: Dict[str, str]) -> Any:
        collection = self.cli['LINE']['User']
        return collection.update_one({'user_id': query}, {'$set': update_values})    
        
    
def NewUserStorageRepository(cli: MongoClient) -> UserStorageRepository:
    return UserStorageRepositoryImpl(cli=cli)