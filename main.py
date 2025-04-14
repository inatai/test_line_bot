from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.staticfiles import StaticFiles

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# staticディレクトリを /static でアクセス可能にする
app.mount("/static", StaticFiles(directory="static"), name="static")


# 環境変数からトークン・シークレットを読み込む
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply = TextSendMessage(text=f"オウム返し: {user_message}")
    line_bot_api.reply_message(event.reply_token, reply)
