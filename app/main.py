import os
from pymongo import MongoClient
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from linebot import LineBotApi, WebhookHandler
from app.entities.io.io import WebhookInput
from app.controller.v1.register_user_from_line import registerUserFromLineController
from app.controller.v1.update_user_info import updateUserInfoController
from app.controller.v1.quick_reply_message import quickReplyMessageController
from app.repository.userStorage.mongodb.mongodb import  UserStorageRepository, NewUserStorageRepository
from app.service.replyMessenger.LINE.line import ReplyMessageService, NewReplyMessageService
from app.usecase.register_user_from_line import NewRegisterUserFromLine
from app.usecase.update_user_info import NewUpdateUserInfo
from app.usecase.quick_reply_message import NewQuickReplyMessage
from app.controller.health.health import healthController
from dotenv import load_dotenv
from typing import Tuple, Any
import logging

load_dotenv()

def newMongoClient() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_URI"))
    return client

def newLineClient() -> Tuple[LineBotApi, WebhookHandler]:
    api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
    return api, handler

userStorageRepo:UserStorageRepository = NewUserStorageRepository(newMongoClient())
replyMessageService:ReplyMessageService = NewReplyMessageService(*newLineClient())

logging.basicConfig(level=logging.INFO)

healthRouter = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

v1Router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

@healthRouter.get("/")
async def health():
    return healthController()

@v1Router.post("/webhook")
async def callback(request: Request):
    return messageManager(request)
    
app = FastAPI()
app.include_router(healthRouter)
app.include_router(v1Router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def messageManager(data: Any) -> Any:
    data = await data.json()
    if not data['events']:
        return 'No event'
    
    webhookInput = WebhookInput(
        user_id = data['events'][0]['source']['userId'],
        user_text = data['events'][0]['message']['text'],
        reply_token = data['events'][0]['replyToken']
    )
    
    if webhookInput.user_text == 'アンケートに回答する':
        return registerUserFromLineController(
            webhookInput, 
            usecase=NewRegisterUserFromLine(user_storage_repo=userStorageRepo, reply_message_service=replyMessageService))
    
    elif webhookInput.user_text in all_enquete_options:
        return updateUserInfoController(
            webhookInput, 
            usecase=NewUpdateUserInfo(user_storage_repo=userStorageRepo, reply_message_service=replyMessageService)
            )
    
    elif webhookInput.user_text in all_quick_reply_options:
        return quickReplyMessageController(
            webhookInput,
            usecase=NewQuickReplyMessage(reply_message_service=replyMessageService)
            )
    
    else: 
        return {"detail": "No event found"}
    
all_enquete_options = ['男性', '女性', 'その他', '立命館大学(BKC)', '立命館大学(BKC以外)', 'その他の大学', '1回生', '2回生', '3回生', '4回生']
all_quick_reply_options = ['立命館大学BKCエリア', '立命館大学OICエリア','BKCエリアのクーポン', 'OICエリアのクーポン']
