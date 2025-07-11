from flask import Flask, request, jsonify
from telegram import Bot
import os

app = Flask(__name__)
bot = Bot(token=os.getenv("8098721049:AAGRrKEbOnqsAKDubJqVGX-x9R4vhcPxv_Y"))

messages = []  # Хранилище сообщений

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_name = msg.get("from", {}).get("first_name")
    text = msg.get("text")

    if chat_id and text:
        # сохраняем сообщение
        messages.append({
            "user": user_name,
            "text": text,
            "chat_id": chat_id
        })
        # пересылаем админу (тебе)
        bot.send_message(chat_id=os.getenv("5827840288"), text=f"💬 {user_name}: {text}")

    return jsonify({"ok": True})

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(messages)

@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text")

    if chat_id and text:
        bot.send_message(chat_id=chat_id, text=text)
        return jsonify({"ok": True})
    return jsonify({"error": "Missing data"}), 400