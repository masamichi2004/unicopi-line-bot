from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import json

options = ['カフェ', 'ラーメン', '洋食']

def generate_quick_reply(options):
        return [
        QuickReplyButton(action=MessageAction(label=label, text=label))
        for label in options
    ]

