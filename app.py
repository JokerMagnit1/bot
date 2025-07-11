from flask import Flask, request
from telegram import Bot
import os

app = Flask(__name__)
bot = Bot(token=os.getenv("BOT_TOKEN"))  # Получаем токен из переменной окружения

# Простое хранилище сообщений
messages = []

# Главная страница
@app.route("/")
def index():
    return "✅ Бот запущен на Render!"

# Обработка Webhook от Telegram
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_name = msg.get("from", {}).get("first_name")
    text = msg.get("text")

    print("📩 Пришло сообщение:", data)  # Лог для отладки

    if chat_id and text:
        messages.append({
            "user": user_name,
            "text": text,
            "chat_id": chat_id
        })
        bot.send_message(chat_id=os.getenv("ADMIN_ID"), text=f"💬 {user_name}: {text}")

    return "ok"

# Эндпоинт для веб-интерфейса — получить все сообщения
@app.route("/messages", methods=["GET"])
def get_messages():
    return messages

# Эндпоинт для отправки ответа пользователю
@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text")

    if chat_id and text:
        bot.send_message(chat_id=chat_id, text=text)
        return {"status": "✅ Ответ отправлен"}
    return {"status": "⚠️ Ошибка: отсутствует chat_id или text"}, 400

# Правильный запуск Flask на Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Получаем порт от Render
    app.run(host="0.0.0.0", port=port)        # Слушаем внешний мир!
