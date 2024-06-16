from fastapi import Depends
from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from app.repository.userStorage.user_storage import UserStorageRepository
from app.service.replyMessenger.reply_message import ReplyMessageService
from app.entities.user.user import User


class RegisterUserFromLine(ABC):
    @abstractmethod
    def exceute(self, user: User) -> Any:
        pass
    
    
class RegisterUserFromLineImpl(RegisterUserFromLine):
    def __init__(self, user_storage_repo: UserStorageRepository, reply_message_service: ReplyMessageService):
        self.user_storage_repo = user_storage_repo
        self.reply_message_service = reply_message_service
    
    def exceute(self, user: User) -> Tuple[Any, Exception]:
        try:
            result = self.user_storage_repo.register_user_from_line(user)
            return result, None
        except Exception as e:
            return None, e
 
        
def NewRegisterUserFromLine(
    user_storage_repo:UserStorageRepository = Depends(UserStorageRepository),
    reply_message_service:ReplyMessageService = Depends(ReplyMessageService)) -> RegisterUserFromLine:
    return RegisterUserFromLineImpl(
        user_storage_repo=user_storage_repo,
        reply_message_service=reply_message_service
        )