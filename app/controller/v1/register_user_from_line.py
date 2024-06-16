from fastapi import Depends
from typing import Any, List
from app.usecase.register_user_from_line import RegisterUserFromLine, NewRegisterUserFromLine
from app.entities.io.io import WebhookInput

def registerUserFromLineController(input: WebhookInput, usecase:RegisterUserFromLine = Depends(NewRegisterUserFromLine)):
    return usecase.exceute(input)