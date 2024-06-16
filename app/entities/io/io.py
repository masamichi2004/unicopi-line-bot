from pydantic import BaseModel

class WebhookInput(BaseModel):
    user_id: str
    user_text: str
    reply_token: str