from flask import Flask, request
from telegram import Bot
import os

app = Flask(__name__)
Bot(token=os.getenv('BOT_TOKEN'))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    bot.send_message(chat_id=chat_id, text=f"Вы написали: {text}")
    return "ok"

if __name__ == "__main__":
    app.run()
