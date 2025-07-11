from flask import Flask, request
from telegram import Bot
import os

app = Flask(__name__)
bot = Bot(token=os.getenv("BOT_TOKEN"))

messages = []  # можно позже подключить базу или Google Sheets

@app.route("/")
def index():
    return "Бот работает 🚀"

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_name = msg.get("from", {}).get("first_name")
    text = msg.get("text")

    print("📩 Получено сообщение:", data)  # выводим лог в Render

    if chat_id and text:
        messages.append({
            "user": user_name,
            "text": text,
            "chat_id": chat_id
        })
        # отправляем админу (тебе)
        bot.send_message(chat_id=os.getenv("ADMIN_ID"), text=f"💬 {user_name}: {text}")

    return "ok"

# Добавим обработку ответов через POST /reply
@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text")

    if chat_id and text:
        bot.send_message(chat_id=chat_id, text=text)
        return {"status": "✅ Ответ отправлен"}
    return {"status": "⚠️ Ошибка"}, 400

# Настройки для Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
