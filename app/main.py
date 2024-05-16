import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from dotenv import load_dotenv

load_dotenv()

line_channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_channel_secret = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/")
async def callback(request: Request):
    body = await request.body()
    data = json.loads(body)
    
    if data['events']:
        try:
            await handle_message(data)
        except IndexError:
            return Exception("Invalid message")
    return {"Error": "Event not found"}



async def handle_message(data):
    incoming_text = data['events'][0]['message']['text']
    reply_token = data['events'][0]['replyToken']
    
    if incoming_text == '店舗情報一覧を取得':
        reply_text = 'はい、何の店舗情報を取得しますか？'
        answer_with_quick_reply = TextSendMessage(
            text=reply_text,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="ラーメン", text="ラーメン")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="カフェ", text="カフェ")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="洋食", text="洋食")
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, answer_with_quick_reply)
        return
        

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
