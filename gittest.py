from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

import requests
def searchWord(word):
    url = "https://www.moedict.tw/raw/" + word
    r = requests.get(url).json()
    msg = '-'*10
    msg += '\n國字:' + r["title"]
    msg += '\n部首:' + r["radical"]
    msg += '\n筆畫:' + str(r["stroke_count"])
    return msg

#connNgrok()
app = Flask(__name__)

line_bot_api = LineBotApi('3JJ4SzVdvKWNWk9AjvJrIBBVfgIjmAjDRWVw4aENXoC8GZaJRJlo1J3Gw/+DTds8ByiNQ2SZF4xWNw63tpbv7EJXbOmBDhKdz+QLIbWroeOvehCUUjtLapyegqyJgKTU0WcI25oWfkcE/thaE9bLvAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5c285bb3195b517cf72d0d7b7eeefe08')

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=searchWord(event.message.text)))


if __name__ == "__main__":
    app.run()