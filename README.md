
# 🤖 LINE AI 聊天機器人 (Gemini + Flask)

這是一個整合 [LINE Messaging API](https://developers.line.biz/en/) 與 Google Gemini AI 的聊天機器人專案，使用 Python Flask 建立 Webhook 伺服器，支援多種互動功能（對話、圖片、影片、貼圖、位置、天氣查詢等），並可透過 REST API 操作歷史紀錄與記憶重置。

LINE ID: @420cttze
- get / delete history
```md
https://6c1f-140-138-83-134.ngrok-free.app/history
```

## 🚀 Feature

### 🧠 AI 對話

* 整合 Google Gemini 模型，支援自然語言問答。
* 支援使用者輸入訊息後即時回應。
* 使用者記憶系統可重置對話上下文（`!reset`）。

### 📜 對話歷史管理

* `GET /history`：取得所有對話紀錄。
* `DELETE /history`：清除對話紀錄。
* `DELETE /reset_memory`：清除所有使用者對話記憶（多使用者支援）。

### ☁️ 天氣查詢

* 輸入 `天氣 [城市名稱]` 即可查詢當地天氣。

### 📦 LINE 指令支援

* `!安安`：打招呼。
* `!reset`：清除目前使用者的 Gemini 記憶。
* `!image`：回傳圖片訊息。
* `!video`：回傳影片訊息。
* `!address`：回傳位置訊息。
* 傳送貼圖時，回覆指定貼圖。

### 🔁 LINE Webhook 整合

* 支援 LINE webhook `/callback`。
* 使用 LINE SDK v3 初始化 Messaging API。
* 包含文字、貼圖、圖片、影片、位置等事件處理。

## 📦 API 一覽

| 方法       | 路由              | 功能說明            |
| -------- | --------------- | --------------- |
| `POST`   | `/chat`         | 傳送文字與 AI 對話     |
| `GET`    | `/history`      | 查看對話紀錄          |
| `DELETE` | `/history`      | 清空對話紀錄          |
| `DELETE` | `/reset_memory` | 重設所有使用者記憶       |
| `POST`   | `/callback`     | LINE webhook 入口 |

## ⚙️ 環境變數設定

請在根目錄建立 `.env` 檔案，並加入以下內容：

```env
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_ACCESS_TOKEN
LINE_CHANNEL_SECRET=你的LINE_SECRET
```

## 🛠️ 執行方式

```bash
pip install -r requirements.txt
python app.py
```

