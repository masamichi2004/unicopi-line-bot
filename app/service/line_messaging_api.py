from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from typing import Dict, Any

class LineMessagingApi:
    def __init__(self, line_bot_api: LineBotApi, handler: WebhookHandler):
        self.line_bot_api = line_bot_api
        self.handler = handler
        
    def is_event_exist(self, data: Dict[str, Any]) -> bool:
        return data['events']
    
    def reply_message(self, reply_token: Any, reply: TextSendMessage):
        self.line_bot_api.reply_message(reply_token, reply)