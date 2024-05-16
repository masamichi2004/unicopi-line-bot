import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from linebot import LineBotApi, WebhookHandler
from app.repositories.line_repository import LineRepository
from app.use_cases.line_use_case import LineUseCase
from dotenv import load_dotenv

load_dotenv()

line_channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_channel_secret = os.getenv("LINE_CHANNEL_SECRET")

line_repository = LineRepository(
    line_bot_api=LineBotApi(line_channel_access_token), 
    handler=WebhookHandler(line_channel_secret)
    )

line_use_case = LineUseCase(line_repository)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/")
async def callback(request: Request):
    body = await request.body()
    data = json.loads(body)
    
    if line_repository.is_event_exist(data):
        try:
            return await line_use_case.reply_store_info_message(data)
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
