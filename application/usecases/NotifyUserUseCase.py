from application.ports.out import MessagingPort


class NotifyUserUseCase:

    def __init__(self, messaging: MessagingPort):
        self.messaging = messaging

    async def execute(self, user_id: str, message: str)->None:
        await self.messaging.send_text(user_id, message)
