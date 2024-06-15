import os
from pymongo import MongoClient
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from linebot import LineBotApi, WebhookHandler
from app.repository.line_repository import LineRepository
from app.usecase.line_use_case import LineUseCase
from app.repository.userStorage.mongodb.mongodb import  UserStorageRepository, NewUserStorageRepository
from app.service.replyMessenger.line.line import ReplyMessageService, NewReplyMessageService
from app.handler.health.health import healthHandler
from dotenv import load_dotenv
from typing import Tuple
import logging

load_dotenv()

line_channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_channel_secret = os.getenv("LINE_CHANNEL_SECRET")

def newMongoClient() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_URI"))
    return client

def newLineClient() -> Tuple[LineBotApi, WebhookHandler]:
    api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
    return api, handler
    

userStorageRepo:UserStorageRepository = NewUserStorageRepository(newMongoClient())
replyMessengerService:ReplyMessageService = NewReplyMessageService(*newLineClient())

line_repository = LineRepository(*newLineClient())

line_use_case = LineUseCase(line_repository)

logging.basicConfig(level=logging.INFO)


healthRouter = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

app = FastAPI()

@healthRouter.get("/")
async def health():
    return healthHandler()

@app.post("/webhook")
async def callback(request: Request):
    data = await request.json()
    logging.info(data)
    
    if line_repository.is_event_exist(data):
        user_message = data['events'][0]['message']['text']
        reply_token = data['events'][0]['replyToken']
        try:
            # 店舗情報
            if user_message == '店舗情報一覧を取得':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['大阪茨木キャンパス(OIC)', 'びわこ草津キャンパス(BKC)'],
                    reply_text='ご自身が在籍しているキャンパスを選択してください。'
                )
            elif user_message == '大阪茨木キャンパス(OIC)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメン', 'カフェ', 'デート'],
                    reply_text='大阪茨木キャンパスの情報を取得します。\nどのジャンルの店舗情報をお探しですか？'
                )
            elif user_message == 'びわこ草津キャンパス(BKC)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメン', 'カフェ', 'デート'],
                    reply_text='びわこ草津キャンパスの情報を取得します。\nどのジャンルの店舗情報をお探しですか？'
                )
            elif user_message == 'あいうえお':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=None,
                    reply_text='あいうえおの次の文字を選択してください。'
                )

            # クーポン情報
            elif user_message == 'クーポンを取得':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['OIC', 'BKC'],
                    reply_text='在籍中のキャンパスを選択してください。'
                )  
                
            elif user_message in ['OIC', 'BKC']:
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメンクーポン', 'カフェクーポン', 'デートクーポン'],
                    reply_text=f'{user_message}のクーポン情報を取得します。\nどのジャンルのクーポン情報をお探しですか？'
                )
        except IndexError:
            return Exception("Invalid message")
    return {"Error": "Event not found"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(healthRouter)