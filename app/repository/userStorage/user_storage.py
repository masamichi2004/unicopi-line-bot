from abc import ABC, abstractmethod
from app.model.user.user import User
from typing import Any

class UserStorageRepository(ABC):
    @abstractmethod
    def register_user(self, user: User) -> Any:
        pass
    
    