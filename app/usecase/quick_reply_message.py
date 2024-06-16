from fastapi import Depends
from typing import Any
from app.service.replyMessenger.reply_message import ReplyMessageService
from abc import ABC, abstractmethod

class QuickReplyMessage(ABC):
    @abstractmethod
    def excute(self, user: Any) -> Any:
        pass
    
class QuickReplyMessageImpl(QuickReplyMessage):
    def __init__(self, reply_message_service: ReplyMessageService):
        self.reply_message_service = reply_message_service
        
    def excute(self, user: Any) -> Any:
        pass
    
def NewQuickReplyMessage(reply_message_service: ReplyMessageService) -> QuickReplyMessage:
    return QuickReplyMessageImpl(reply_message_service=reply_message_service)