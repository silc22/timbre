from flask import Flask, request
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


TOKEN = os.getenv("TOKEN")
RECEIVERS = os.getenv("RECEIVERS")

@app.route('/', methods=['GET', 'POST'])

def notify_all(text):
    for chat_id in RECEIVERS:
        send_msg(chat_id, text)

def webhook():
    if request.method == 'GET':
        return "Bot funcionando", 200

    data = request.get_json()
    print("📩 Datos recibidos de Telegram:", data) 

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        print(f"💬 Nuevo mensaje de chat_id: {chat_id} | Texto: {text}")  

        if text == "/start":
            send_msg(chat_id, "¡Hola! Este es el timbre. Tocá el botón para avisar que estás abajo.")
            send_button(chat_id)

        elif text == "🚪 Tocar timbre":
            notify_all("🚨 Tocaron el timbre abajo.")

    return "ok", 200


def send_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

def send_button(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": "Tocá el botón para avisarme:",
        "reply_markup": {
            "keyboard": [[{"text": "🚪 Tocar timbre"}]],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
    }
    requests.post(url, json=data)
    