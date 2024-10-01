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
        line_id = data['events'][0]['source']['userId']

        user = user_storage.find_user(line_id)

        try:
            # 店舗情報
            if user_message == '店舗情報一覧を取得':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['大阪エリア', '京都エリア', '滋賀エリア'],
                    reply_text='探したい店舗のエリアを指定してください'
                )
            elif user_message == '滋賀エリア':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['草津'],
                    reply_text='滋賀のどのエリアを検索しますか？'
                )
            elif user_message == '大阪エリア':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['茨木',],
                    reply_text='大阪のどのエリアを検索しますか？'
                )
            elif user_message == '京都エリア':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['衣笠', '円町', '二条', '今出川', '一乗寺'],
                    reply_text='京都のどのエリアを検索しますか？'
                )
            elif user_message == 'あいうえお':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=None,
                    reply_text='あいうえおの次の文字を選択してください。'
                )

            # クーポン情報
            elif user_message == 'クーポンを取得':
                if user is None:
                    return line_messaging_api.reply_message(
                        reply_token,
                        TextSendMessage(text='アンケートに回答していただくとクーポン情報を取得できます')
                    )
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['大阪エリア(クーポン)', '京都エリア(クーポン)', '滋賀エリア(クーポン)'],
                    reply_text='取得したい店舗クーポンのエリアを指定してください'
                )  

            elif user_message == '滋賀エリア(クーポン)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['草津クーポン',],
                    reply_text='滋賀のどのエリアの店舗クーポン情報を取得しますか？'
                )

            elif user_message == '大阪エリア(クーポン)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['茨木クーポン',],
                    reply_text='大阪のどのエリアの店舗クーポン情報を取得しますか？'
                )
            elif user_message == '京都エリア(クーポン)':
                return await line_use_case.quick_reply_message(
                    reply_token,
                    options=['今出川クーポン', '円町クーポン', '二条クーポン'],
                    reply_text='京都のどのエリアの店舗クーポン情報を取得しますか？'
                )

            # アンケート回答
            elif user_message == 'アンケートに回答する':
                if user:
                    return line_messaging_api.reply_message(
                        reply_token,
                        TextSendMessage(text='アンケートは既に回答済みです。')
                    )

                result = user_storage.register_user(line_id)
                if result == 'OK':
                    return line_messaging_api.reply_message(
                        reply_token,
                        TextSendMessage(
                            text="現在使用率を調査するためにアンケートを実施しております。\nアンケートにご回答いただくとメニューからクーポンの取得が可能になります！\n下記Google Formのリンクからアンケートにご回答いただくようお願いいたします。\n\nhttps://forms.gle/Kno4FDATosZN8n4T6"
                        ),
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
