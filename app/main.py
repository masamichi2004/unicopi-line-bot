import os
from pymongo import MongoClient
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from app.service.line_messaging_api import LineMessagingApi
from app.repository.user_storage import UserStorageRepository
from app.usecase.line_use_case import LineUseCase
from app.controller.health.health import healthController
from dotenv import load_dotenv
from typing import Tuple
import logging

load_dotenv()

def newMongoClient() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_URI"))
    return client

def newLineClient() -> Tuple[LineBotApi, WebhookHandler]:
    api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
    return api, handler
    

line_messaging_api = LineMessagingApi(*newLineClient())
user_storage = UserStorageRepository(newMongoClient())
line_use_case = LineUseCase(line_messaging_api)

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
    data = await request.json()
    logging.info(data)
    
    if line_messaging_api.is_event_exist(data):
        user_message = data['events'][0]['message']['text']
        reply_token = data['events'][0]['replyToken']
        try:
            # 店舗情報
            if user_message == '店舗情報一覧を取得':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['立命館大学BKCエリア', '立命館大学OICエリア'],
                    reply_text='取得したい大学エリアを指定してください'
                )
            elif user_message == '立命館大学BKCエリア':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメン(BKC)', 'カフェ(BKC)', 'デート(BKC)'],
                    reply_text='大阪茨木キャンパスの情報を取得します。\nどのジャンルの店舗情報をお探しですか？'
                )
            elif user_message == '立命館大学OICエリア':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメン(OIC)', 'カフェ(OIC)', 'デート(OIC)'],
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
                    options=['立命館大学BKCエリア(クーポン)', '立命館大学OICエリア(クーポン)'],
                    reply_text='取得したいクーポンの大学エリアを指定してください'
                )  
                
            elif user_message == '立命館大学BKCエリア(クーポン)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメンクーポン(BKC)', 'カフェクーポン(BKC)', 'デートクーポン(BKC)'],
                    reply_text='BKCエリアの店舗クーポン情報を取得します。\nどのジャンルのクーポン情報をお探しですか？'
                )
                
            elif user_message == '立命館大学OICエリア(クーポン)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['ラーメンクーポン(OIC)', 'カフェクーポン(OIC)', 'デートクーポン(OIC)'],
                    reply_text='OICエリアの店舗クーポン情報を取得します。\nどのジャンルのクーポン情報をお探しですか？'
                )
                
        except IndexError:
            return Exception("Invalid message")
    return {"Error": "Event not found"}

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
