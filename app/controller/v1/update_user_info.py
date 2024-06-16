from fastapi import Depends
from typing import Any
from app.usecase.update_user_info import UpdateUserInfo, NewUpdateUserInfo
from app.entities.io.io import WebhookInput

def updateUserInfoController(input: WebhookInput, usecase: UpdateUserInfo = Depends(NewUpdateUserInfo)):
    return usecase.excute(input)