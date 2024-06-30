from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from app.service.line_messaging_api import LineMessagingApi
from typing import Dict, Any, List, Optional

class LineUseCase:
    def __init__(self, line_messaging_api: LineMessagingApi):
        self.line_messaging_api = line_messaging_api
        
    def create_quick_reply(self, categories: Optional[List[str]] = None) -> QuickReply:
        if not categories:
            return None
        quick_reply_buttons = [
            QuickReplyButton(
                action=MessageAction(label=category, text=category)
            )
            for category in categories
        ]
        return QuickReply(items=quick_reply_buttons)
    
    def get_quick_reply_message(self, reply_text: str, quick_reply: QuickReply) -> TextSendMessage:
        return TextSendMessage(text=reply_text, quick_reply=quick_reply)
    
    
    async def quick_reply_message(self, reply_token: Any, options: List[str], reply_text: str) -> None:
        quick_reply = self.create_quick_reply(options)
        answer_with_quick_reply = self.get_quick_reply_message(reply_text, quick_reply)
        self.line_messaging_api.reply_message(reply_token, answer_with_quick_reply)
        return
        
