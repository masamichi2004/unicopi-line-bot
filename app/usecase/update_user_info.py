from fastapi import Depends
from app.repository.userStorage.user_storage import UserStorageRepository
from app.service.replyMessenger.reply_message import ReplyMessageService
from abc import ABC, abstractmethod
from app.entities.io.io import WebhookInput
from typing import Any, List, Tuple


class UpdateUserInfo(ABC):
    @abstractmethod
    def excute(self, user: WebhookInput) -> Tuple[Any, Exception]:
        pass
    
class UpdateUserInfoImpl(UpdateUserInfo):
    def __init__(self, user_storage_repo: UserStorageRepository, reply_message_service: ReplyMessageService):
        self.user_storage_repo = user_storage_repo
        self.reply_message_service = reply_message_service
        
    def excute(self, input: WebhookInput) -> Tuple[Any, Exception]:
        pass    
    
def NewUpdateUserInfo(
    user_storage_repo: UserStorageRepository = Depends(UserStorageRepository),
    reply_message_service: ReplyMessageService = Depends(ReplyMessageService)) -> UpdateUserInfo:
    return UpdateUserInfoImpl(
        user_storage_repo=user_storage_repo,
        reply_message_service=reply_message_service
        )