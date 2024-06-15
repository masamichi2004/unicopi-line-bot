from abc import ABC, abstractmethod

class ReplyMessageService(ABC):
    @abstractmethod
    def create_quick_reply(self, message: str) -> str:
        pass
    
    @abstractmethod
    def reply_message(self, reply_token: str, message: str) -> None:
        pass