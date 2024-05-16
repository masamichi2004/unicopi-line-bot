from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from typing import Dict, Any

class LineRepository:
    def __init__(self, line_bot_api: LineBotApi, handler: WebhookHandler):
        self.line_bot_api = line_bot_api
        self.handler = handler
        
    def is_event_exist(self, data: Dict[str, Any]) -> bool:
        return data['events']
    
    def reply_message(self, reply_token: Any, answer_with_quick_reply: TextSendMessage):
        self.line_bot_api.reply_message(reply_token, answer_with_quick_reply)