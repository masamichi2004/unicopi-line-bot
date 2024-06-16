from app.service.replyMessenger.reply_message import ReplyMessageService
from linebot import LineBotApi, WebhookHandler
from linebot.models import QuickReply, QuickReplyButton, MessageAction, TextSendMessage
from typing import List, Any


class ReplyMessageServiceImpl(ReplyMessageService):
    def __init__(self, api: LineBotApi, handler: WebhookHandler):
        self.api = api
        self.handler = handler
    
    def create_quick_reply_message(self, categories: List[str], reply_text: str) -> TextSendMessage:
        quick_reply_buttons = [
            QuickReplyButton(
                action=MessageAction(label=category, text=category)
            )
            for category in categories
        ]
        quick_reply = QuickReply(items=quick_reply_buttons)
        
        return TextSendMessage(text=reply_text, quick_reply=quick_reply)
    
    def quick_reply_message(self, reply_token: str, reply: TextSendMessage) -> None:
        self.api.reply_message(reply_token, reply)
        return
    
    def reply_message(self, reply_token: Any, reply_text: str) -> None:
        self.api.reply_message(reply_token, TextSendMessage(text=reply_text))
        return
        
    
    

    
    
def NewReplyMessageService(api: LineBotApi, handler: WebhookHandler) -> ReplyMessageService:
    return ReplyMessageServiceImpl(
        api=api,
        handler=handler
    )