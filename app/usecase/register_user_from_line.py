from fastapi import Depends
from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from app.repository.userStorage.user_storage import UserStorageRepository
from app.entities.user.user import User


class RegisterUserFromLine(ABC):
    @abstractmethod
    def exceute(self, user: User) -> Any:
        pass
    
    
class RegisterUserFromLineImpl(RegisterUserFromLine):
    def __init__(self, user_storage_repo: UserStorageRepository):
        self.user_storage_repo = user_storage_repo
    
    def exceute(self, user: User) -> Tuple[Any, Exception]:
        try:
            result = self.user_storage_repo.register_user_from_line(user)
            return result, None
        except Exception as e:
            return None, e
        
def NewRegisterUserFromLine(user_storage_repo: UserStorageRepository) -> RegisterUserFromLine:
    return RegisterUserFromLineImpl(user_storage_repo=user_storage_repo)