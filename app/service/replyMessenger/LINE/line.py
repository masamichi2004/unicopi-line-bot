from app.service.replyMessenger.reply_message import ReplyMessageService
from linebot import LineBotApi, WebhookHandler
from linebot.models import QuickReply, QuickReplyButton, MessageAction
from typing import List


class ReplyMessageServiceImpl(ReplyMessageService):
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
    
    def reply_message(self, reply_token: str, message: str) -> None:
        self.api.reply_message(reply_token, message)
        return
    
    

    
    
def NewReplyMessageService(api: LineBotApi, handler: WebhookHandler) -> ReplyMessageService:
    return ReplyMessageServiceImpl(
        api=api,
        handler=handler
    )