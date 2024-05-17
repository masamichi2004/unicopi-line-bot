from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from app.repositories.line_repository import LineRepository
from typing import Dict, Any, List

class LineUseCase:
    def __init__(self, line_repository: LineRepository):
        self.line_repository = line_repository
        
    def create_quick_reply(self, categories: List[str]) -> QuickReply:
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
        self.line_repository.reply_message(reply_token, answer_with_quick_reply)
        return
        
