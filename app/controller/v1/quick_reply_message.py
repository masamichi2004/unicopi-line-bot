from fastapi import Depends
from typing import Any
from app.usecase.quick_reply_message import QuickReplyMessage, NewQuickReplyMessage

def quickReplyMessageController(user: Any, usecase: QuickReplyMessage = Depends(NewQuickReplyMessage)):
    return usecase.excute(user)