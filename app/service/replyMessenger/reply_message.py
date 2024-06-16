from abc import ABC, abstractmethod
from linebot.models import TextSendMessage
from typing import Any, List

class ReplyMessageService(ABC):
    @abstractmethod
    def create_quick_reply_message(self, categories: List[str], reply_text: str) -> TextSendMessage:
        pass
    
    @abstractmethod
    def quicK_reply_message(self, reply_token: str, reply: TextSendMessage) -> None:
        pass
    
