import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "start", "overview", "search",
            "Festival", "intro", "custom", "video"],
    transitions=[
        {
            "trigger": "advance",
            "source": ["start", "Festival"],
            "dest": "overview",
            "conditions": "is_going_to_overview",
        },
        {
            "trigger": "advance",
            "source": ["start", "Festival"],
            "dest": "search",
            "conditions": "is_going_to_search",
        },
        {
            "trigger": "advance",
            "source": ["overview", "search", "intro", "custom", "video"],
            "dest": "Festival",
            "conditions": "is_going_to_Festival",
        },
        # {
        #     "trigger": "advance",
        #     "source": "search",
        #     "dest": "Festival",
        #     "conditions": "is_going_to_Festival",
        # },
        {
            "trigger": "advance",
            "source": "Festival",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "Festival",
            "dest": "custom",
            "conditions": "is_going_to_custom",
        },
        {
            "trigger": "advance",
            "source": "Festival",
            "dest": "video",
            "conditions": "is_going_to_video",
        },
        {
            "trigger": "advance", 
            "source": ["user","overview", "search"], 
            "dest": "start",
            "conditions": "is_going_to_start",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            #send_text_message(event.reply_token, "Not Entering any State")
            if machine.state == "user":
                send_text_message(event.reply_token, "請輸入「start」開始", None)
            elif machine.state == "start":
                send_text_message(event.reply_token, "請輸入「總覽」或「查詢」", None)
            elif machine.state == "overview":
                send_text_message(event.reply_token, "無此節日或指令", None)
            elif machine.state == "search":
                send_text_message(event.reply_token, "無法查詢到相應節日，請重新輸入並確認名稱、日期或格式是否有誤", None)
            else :
                send_text_message(event.reply_token, "無效的指令，請重新輸入", None)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
