from flask import Flask, request, Response, jsonify, abort
import os
import json
from dotenv import load_dotenv
from gemini_handler import generate_reply, reset_user_session
from wether_handler import get_weather

# LINE SDK v3 imports
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import StickerMessageContent
from linebot.v3.messaging.models import ImageMessage, VideoMessage, LocationMessage

from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    ReplyMessageRequest,
    StickerMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# 載入 .env
load_dotenv()

app = Flask(__name__)
chat_history = []
#print("LINE_SECRET:", os.getenv("LINE_CHANNEL_SECRET"))
# 初始化 LINE 設定（注意：不在這裡建立 MessagingApi 實例）

# LINE SDK v3 正確初始化方式
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# ✅ Gemini test API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    ai_reply = generate_reply(user_message)
    chat_history.append({"user": user_message, "ai": ai_reply})

    return Response(json.dumps({"reply": ai_reply}, ensure_ascii=False),
                    content_type="application/json")

# ✅ 取得歷史紀錄
# curl http://localhost:5000/history 
@app.route("/history", methods=["GET"])
def get_history():
    print("歷史紀錄:", chat_history)
    return Response(json.dumps(chat_history, ensure_ascii=False),
                    content_type="application/json")

# ✅ 清除歷史紀錄
# curl -X DELETE http://localhost:5000/history
@app.route("/history", methods=["DELETE"])
def delete_history():
    chat_history.clear()
    return jsonify({"message": "歷史已清除"}), 200

# ✅ LINE webhook
@app.route("/callback", methods=["GET", "POST"])
def callback():
    if request.method == "GET":
        return "✅ Webhook is ready (GET test)"
    
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text
    user_id = event.source.user_id  # 使用者 LINE ID 當作 key
    print("用戶訊息:", user_text)

    if user_text == "!安安":
        chat_history.clear()
        ai_reply = "你好啊"
        
    if user_text == "!reset":
        chat_history.clear()
        reset_user_session(user_id)  # ✅ 正確呼叫清除這個使用者的記憶
        ai_reply = "你好啊，我會從這裡開始記憶新的對話唷😊～任何事情我都能幫上忙喔！需要我幫你生演講稿或是介紹任何你想知道的主題嗎？"

    

    elif user_text == "!image":
        # 回傳圖片訊息
        image = ImageMessage(
            original_content_url="https://velog.velcdn.com/images%2Fhhhong%2Fpost%2F8f43502a-f9fe-4c29-8dd7-0874a89a2669%2FScreen%20Shot%202022-01-07%20at%203.53.35%20PM.png",
            preview_image_url="https://velog.velcdn.com/images%2Fhhhong%2Fpost%2F8f43502a-f9fe-4c29-8dd7-0874a89a2669%2FScreen%20Shot%202022-01-07%20at%203.53.35%20PM.png"
        )
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image]
                )
            )
        return  
    
    elif user_text == "!address":
        location = LocationMessage(
            title="中正紀念堂",
            address="台北市中正區中山南路21號",
            latitude=25.036798,
            longitude=121.519041,
        )
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[location]
                )
            )
        return


    elif user_text == "!video":
        # 回傳影片訊息
        video = VideoMessage(
            original_content_url="https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            preview_image_url="https://i.imgur.com/0Z5XhRQ.jpg"
        )
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[video]
                )
            )
        return
    
    elif user_text.startswith("天氣 "):
        city = user_text.replace("天氣 ", "").strip()
        ai_reply = get_weather(city)
    

    else:
        # 一般 Gemini 回覆
        ai_reply = generate_reply(user_id, user_text)

    chat_history.append({"user": user_text, "ai": ai_reply})

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=ai_reply)]
            )
        )

@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker(event):
    print("get sticker!")

    # 建立回傳的貼圖內容
    reply_sticker = StickerMessage(
        package_id="6359",
        sticker_id="11069851"
    )

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_sticker]
            )
        )


from gemini_handler import generate_reply, reset_all_sessions  # ✅ 確保有匯入 reset 函數

# API: reset all users memory
# curl -X DELETE http://localhost:5050/reset_memory
@app.route("/reset_memory", methods=["DELETE"])
def reset_memory():
    reset_all_sessions()
    print("✅ 所有使用者 Gemini 對話記憶已清除")
    return jsonify({"message": "所有使用者記憶已清除"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)  

