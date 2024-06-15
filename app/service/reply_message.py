from abc import ABC, abstractmethod

class ReplyMessageRepository(ABC):
    @abstractmethod
    def reply(self, message: str) -> str:
        pass