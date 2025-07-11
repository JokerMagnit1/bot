from flask import Flask, request
from telegram import Bot
import os

app = Flask(__name__)
bot = Bot(token=os.getenv("BOT_TOKEN"))  # Получаем токен из переменных окружения

# Хранилище сообщений (можно заменить на базу или Google Sheets)
messages = []

@app.route("/")
def index():
    return "🚀 Бот работает!"

# Webhook от Telegram
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_name = msg.get("from", {}).get("first_name")
    text = msg.get("text")

    if chat_id and text:
        messages.append({
            "user": user_name,
            "text": text,
            "chat_id": chat_id
        })
        bot.send_message(chat_id=os.getenv("ADMIN_ID"), text=f"💬 {user_name}: {text}")

    return "ok"

# Получение списка сообщений (для веб-интерфейса)
@app.route("/messages", methods=["GET"])
def get_messages():
    return messages

# Ответ пользователю
@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text")

    if chat_id and text:
        bot.send_message(chat_id=chat_id, text=text)
        return {"status": "✅ Ответ отправлен"}
    return {"status": "⚠️ Ошибка: отсутствуют данные"}, 400

# Запуск Flask — важно для Render!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render подаёт порт через переменную окружения
    app.run(host="0.0.0.0", port=port)
