from typing import Any
from app.controller.v1.register_user_from_line import registerUserFromLineController
from app.controller.v1.update_user_info import updateUserInfoController
from app.controller.v1.quick_reply_message import quickReplyMessageController
from app.entities.io.io import WebhookInput


def messageContoller(data: Any) -> Any:
    if not data['events']:
        return 'No event'
    
    user = WebhookInput(
        user_id = data['events'][0]['source']['userId'],
        user_text = data['events'][0]['message']['text'],
        reply_token = data['events'][0]['replyToken']
    )
    
    if user.user_text == 'アンケートに回答する':
        return registerUserFromLineController(user)
    
    elif user.user_text in all_enquete_options:
        return updateUserInfoController(user)
    
    elif user.user_text in all_quick_reply_options:
        return quickReplyMessageController(user)
    
    else: 
        return {"detail": "No event found"}
    
all_enquete_options = ['男性', '女性', 'その他', '立命館大学(BKC)', '立命館大学(BKC以外)', 'その他の大学', '1回生', '2回生', '3回生', '4回生']
all_quick_reply_options = ['立命館大学BKCエリア', '立命館大学OICエリア','BKCエリアのクーポン', 'OICエリアのクーポン']

# all_answer_options = [
#     'ラーメン(BKC)', 'カフェ(BKC)', 'デート(BKC)', 
#     'ラーメン(OIC)', 'カフェ(OIC)', 'デート(OIC)', 
#     'ラーメンクーポン(BKC)', 'カフェクーポン(BKC)', 'デートクーポン(BKC)', 
#     'ラーメンクーポン(OIC)', 'カフェクーポン(OIC)', 'デートクーポン(OIC)'
#     ]
