from fastapi import Depends
from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from app.repository.userStorage.user_storage import UserStorageRepository
from app.service.replyMessenger.reply_message import ReplyMessageService
from app.entities.user.user import User
from app.entities.io.io import WebhookInput


class RegisterUserFromLine(ABC):
    @abstractmethod
    def exceute(self, input: WebhookInput) -> Any:
        pass
    
    
class RegisterUserFromLineImpl(RegisterUserFromLine):
    def __init__(self, user_storage_repo: UserStorageRepository, reply_message_service: ReplyMessageService):
        self.user_storage_repo = user_storage_repo
        self.reply_message_service = reply_message_service
    
    def exceute(self, input: WebhookInput) -> Tuple[Any, Exception]:
        try:
            if self.user_storage_repo.is_user_exist(user_id=input.user_id):
                result = self.reply_message_service.reply_message(
                    reply_token=input.reply_token,
                    reply_text='アンケートの回答は1度までです'
                    ) 
                return result, None
            user = User(
                user_id=input.user_id,
                gender=None,
                univ=None,
                grade=None,
                answered_enquete=True 
                )
            self.user_storage_repo.register_user_from_line(user=user)
            
            # アンケート１問目のクイックリプライ
            options = ['男性', '女性', 'その他']
            reply = self.reply_message_service.create_quick_reply_message(
                categories=options,
                reply_text='性別を選択してください'
                )
            result = self.reply_message_service.quick_reply_message(
                reply_token=input.reply_token,
                reply=reply
                )     
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