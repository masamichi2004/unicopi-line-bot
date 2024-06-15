from app.service.replyMessenger.reply_message import ReplyMessengerService
from linebot import LineBotApi, WebhookHandler
from linebot.models import QuickReply, QuickReplyButton, MessageAction
from typing import List


class ReplyMessengerServiceImpl(ReplyMessengerService):
    def __init__(self, api: LineBotApi, handler: WebhookHandler):
        self.api = api
        self.handler = handler
    
    def create_quick_reply(self, categories: List[str]) -> QuickReply:
        quick_reply_buttons = [
            QuickReplyButton(
                action=MessageAction(label=category, text=category)
            )
            for category in categories
        ]
        return QuickReply(items=quick_reply_buttons)
    
    

    
    
def NewReplyMessageService(api: LineBotApi, handler: WebhookHandler) -> ReplyMessengerService:
    return ReplyMessengerServiceImpl(
        api=api,
        handler=handler
    )