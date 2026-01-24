from abc import ABC, abstractmethod

class MessagingPort(ABC):

    @abstractmethod
    async def send_text(self, recipient_id: str, text: str):
        pass