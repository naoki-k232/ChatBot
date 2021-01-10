from time import time
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'k8PIpoSnrHcCojBBmMx+9I+r7LJXG2Dhw9QklNk6pTL17LX7tVSm0Dth0yqeG2EMej6GnaS6EifzMGtTvKxJ9UfE8HFh5228I1RktBMziHEzSHTcrygYa1LBC47Z6RLGV48TAl+gk3Q0D/ksZWD6SgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('af27f0ab0f2fd1f49dd43504eb1da2fc')


@app.route("/")
def test():
    return "OK"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


users = {}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "勉強開始":
        reply_message = "計測を開始しました"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()
    else:
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        reply_message = f"ただいまの勉強時間は{hour}時間{minute}分{second}秒です。お疲れ様でした!合計で{users[userId]['total']}秒勉強しています。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()
