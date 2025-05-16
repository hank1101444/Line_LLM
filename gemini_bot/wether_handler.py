import requests
import os
from dotenv import load_dotenv

def get_weather(city: str) -> str:
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "ERROR: OpenWeatherMap API key not found."

    url = f"https://api.openweathermap.org/data/2.5/forecast/?q={city}&appid={api_key}&units=metric&lang=zh_tw"

    try:
        response = requests.get(url)
        data = response.json()
        #print(data)
        print(data.get("cod"))
        if data.get("cod") != "200":
            return f"❌ 查不到「{city}」的天氣資訊"

        # 使用預報資料中的第一筆
        forecast = data["list"][0]
        weather = forecast["weather"][0]["description"]
        temp = forecast["main"]["temp"]
        humidity = forecast["main"]["humidity"]
        dt_txt = forecast["dt_txt"]

        return (
            f"📍 {city} 預測時間：{dt_txt}\n"
            f"🌤️ 天氣狀況：{weather}\n"
            f"🌡️ 氣溫：{temp}°C\n"
            f"💧 濕度：{humidity}%"
        )

    except Exception as e:
        return f"❌ 查詢失敗：{str(e)}"


