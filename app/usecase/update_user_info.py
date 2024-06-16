from fastapi import Depends
from app.repository.userStorage.user_storage import UserStorageRepository
from app.service.replyMessenger.reply_message import ReplyMessageService
from abc import ABC, abstractmethod
from app.entities.io.io import WebhookInput
from typing import Any, List, Tuple
import logging

logging.basicConfig(level=logging.DEBUG)


class UpdateUserInfo(ABC):
    @abstractmethod
    def excute(self, input: WebhookInput) -> Tuple[Any, Exception]:
        pass
    
class UpdateUserInfoImpl(UpdateUserInfo):
    def __init__(self, user_storage_repo: UserStorageRepository, reply_message_service: ReplyMessageService):
        self.user_storage_repo = user_storage_repo
        self.reply_message_service = reply_message_service
        
    def excute(self, input: WebhookInput) -> Tuple[Any, Exception]:
        logging.debug(f'input.user_text: {input.user_text}')
        try:
            if input.user_text in ['男性', '女性', 'その他']:
                self.user_storage_repo.update_user_info(
                    user_id=input.user_id,
                    update_values={"gender": input.user_text}
                )
                options = ['立命館大学BKCキャンパス', '立命館大学OICキャンパス', 'その他の大学']
                reply = self.reply_message_service.create_quick_reply_message(
                    categories=options,
                    reply_text='所属している大学を選択してください'
                )
                result = self.reply_message_service.quick_reply_message(
                    reply_token=input.reply_token,
                    reply=reply
                )
                return result, None
            elif input.user_text in ['立命館大学BKCキャンパス', '立命館大学OICキャンパス', 'その他の大学']:
                self.user_storage_repo.update_user_info(
                    user_id=input.user_id,
                    update_values={"univ": input.user_text}
                )
                options = ['1回生', '2回生', '3回生', '4回生', '院生']
                reply = self.reply_message_service.create_quick_reply_message(
                    categories=options,
                    reply_text='学年を選択してください'
                )
                result = self.reply_message_service.quick_reply_message(
                    reply_token=input.reply_token,
                    reply=reply
                )
                return result, None
            elif input.user_text in ['1回生', '2回生', '3回生', '4回生', '院生']:
                self.user_storage_repo.update_user_info(
                    user_id=input.user_id,
                    update_values={"grade": input.user_text}
                )
                result = self.reply_message_service.reply_message(
                    reply_token=input.reply_token,
                    reply_text='ご回答いただきありがとうございました！\nクーポンの利用が可能になりました🐸'
                )
                return result, None
            elif input.user_text == 'クーポンを取得':
                if not self.user_storage_repo.is_user_exist(user_id=input.user_id):
                    result = self.reply_message_service.reply_message(
                        reply_token=input.reply_token,
                        reply_text='クーポンのご利用にはアンケートへの回答が必須です'
                    )
                    logging.debug(f'result: {result}')
                    return result, None
                options = ['BKCエリアのクーポン', 'OICエリアのクーポン']
                reply = self.reply_message_service.create_quick_reply_message(
                    categories=options,
                    reply_text='どのエリアの店舗のクーポンを取得しますか？'
                )
                result = self.reply_message_service.quick_reply_message(
                    reply_token=input.reply_token,
                    reply=reply
                )
                return result, None
        except Exception as e:
            return None, e
                
    
def NewUpdateUserInfo(
    user_storage_repo: UserStorageRepository = Depends(UserStorageRepository),
    reply_message_service: ReplyMessageService = Depends(ReplyMessageService)) -> UpdateUserInfo:
    return UpdateUserInfoImpl(
        user_storage_repo=user_storage_repo,
        reply_message_service=reply_message_service
        )