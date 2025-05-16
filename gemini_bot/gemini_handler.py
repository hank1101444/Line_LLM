import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # read api_key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# 建立 Gemini 模型設定
model = genai.GenerativeModel(
    model_name= "gemini-2.5-flash-preview-04-17",#"gemini-2.5-pro-exp-03-25",
    system_instruction=(
        "你是我的個人助理，請用繁體中文回答。回答要口語化、精簡實用，"
        "請像朋友一樣回應。"
    )
)

# 使用者 ID → chat session 的映射（記憶保留）
user_sessions = {}

def generate_reply(user_id: str, user_input: str) -> str:
    try:
        if user_id not in user_sessions:
            # 為新使用者建立新的對話 session（含記憶）
            user_sessions[user_id] = model.start_chat(history=[])

        chat = user_sessions[user_id]
        response = chat.send_message(user_input)
        return response.text.strip()
    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

def reset_all_sessions():
    user_sessions.clear()
    
def reset_user_session(user_id: str):
    if user_id in user_sessions:
        print("reset_user_session:", user_id)
        del user_sessions[user_id]

