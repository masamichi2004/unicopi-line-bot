from abc import ABC, abstractmethod
from app.entities.user.user import User
from typing import Any, Dict

class UserStorageRepository(ABC):
    @abstractmethod
    def register_user_from_line(self, user: User) -> Any:
        pass
    
    @abstractmethod
    def is_user_exist(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def update_user_info(self, query: str, update_values: Dict[str, str]) -> Any:
        pass