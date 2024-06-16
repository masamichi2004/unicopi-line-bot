from abc import ABC, abstractmethod
from app.entities.user.user import User
from typing import Any

class UserStorageRepository(ABC):
    @abstractmethod
    def register_user_from_line(self, user: User) -> Any:
        pass
    
    @abstractmethod
    def update_user_info(self, user: User) -> Any:
        pass