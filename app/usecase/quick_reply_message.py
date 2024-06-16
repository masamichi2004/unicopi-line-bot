from fastapi import Depends
from typing import Any, Tuple
from app.entities.io.io import WebhookInput
from app.service.replyMessenger.reply_message import ReplyMessageService
from abc import ABC, abstractmethod

class QuickReplyMessage(ABC):
    @abstractmethod
    def excute(self, input: WebhookInput) -> Tuple[Any, Exception]:
        pass
    
class QuickReplyMessageImpl(QuickReplyMessage):
    def __init__(self, reply_message_service: ReplyMessageService):
        self.reply_message_service = reply_message_service
        
    def excute(self, input: WebhookInput) -> Tuple[Any, Exception]:
        try:
            if input.user_text == '店舗情報一覧を取得する':
                categories=['立命館大学BKCエリア', '立命館大学OICエリア']
                reply_text='どちらのエリアの店舗情報をお探しですか？'                
            
            elif input.user_text == '立命館大学BKCエリア':
                categories=['ラーメン(BKC)', 'カフェ(BKC)', 'デート(BKC)']
                reply_text='店舗の情報を取得しています🌀\nどのカテゴリをお探してですか？'
                
            elif input.user_text == '立命館大学OICエリア':
                categories=['ラーメン(OIC)', 'カフェ(OIC)', 'デート(OIC)']
                reply_text='店舗の情報を取得しています🌀\nどのカテゴリをお探してですか？'
                
            elif input.user_text == 'BKCエリアのクーポン':
                categories=['ラーメンクーポン(BKC)', 'カフェクーポン(BKC)', 'デートクーポン(BKC)']
                reply_text='店舗の情報を取得しています🌀\nどのカテゴリをお探してですか？'
                
            elif input.user_text == 'OICエリアのクーポン':
                categories=['ラーメンクーポン(OIC)', 'カフェクーポン(OIC)', 'デートクーポン(OIC)']
                reply_text='店舗の情報を取得しています🌀\nどのカテゴリをお探してですか？'
                
            reply = self.reply_message_service.create_quick_reply_message(
                    categories=categories, 
                    reply_text=reply_text
                )
            self.reply_message_service.quick_reply_message(reply_token=input.reply_token, reply=reply)
            return 'success', None
        except Exception as e:
            return None, e
    
def NewQuickReplyMessage(reply_message_service: ReplyMessageService = Depends(ReplyMessageService)) -> QuickReplyMessage:
    return QuickReplyMessageImpl(reply_message_service=reply_message_service)