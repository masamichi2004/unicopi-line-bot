from app.service.replyMessenger.reply_message import ReplyMessageService
from linebot.models import QuickReply, QuickReplyButton, MessageAction, TextSendMessage
from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class UpdateUserInfo(ABC):
    @abstractmethod
    def excute(self, user: Any) -> Tuple[Any, Exception]:
        pass
    
class UpdateUserInfoImpl(UpdateUserInfo):
    def __init__(self, reply_message_service: ReplyMessageService):
        self.reply_message_service = reply_message_service
        
    def excute(self, user: Any) -> Tuple[Any, Exception]:
        pass    
    
def NewUpdateUserInfo(reply_message_service: ReplyMessageService) -> UpdateUserInfo:
    return UpdateUserInfoImpl(reply_message_service=reply_message_service)