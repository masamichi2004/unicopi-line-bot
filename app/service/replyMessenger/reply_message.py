from abc import ABC, abstractmethod

class ReplyMessengerService(ABC):
    @abstractmethod
    def create_quick_reply(self, message: str) -> str:
        pass