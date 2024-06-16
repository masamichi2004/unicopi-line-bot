from fastapi import Depends
from typing import Any
from app.usecase.quick_reply_message import QuickReplyMessage, NewQuickReplyMessage
from app.entities.io.io import WebhookInput

def quickReplyMessageController(input: WebhookInput, usecase: QuickReplyMessage = Depends(NewQuickReplyMessage)):
    return usecase.excute(input)