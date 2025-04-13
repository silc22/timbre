from flask import Flask, request
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# 🔒 Token del bot
TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# 👥 Lista de destinatarios (chat_ids)
RECEIVERS = os.getenv("RECEIVERS", "")
RECEIVERS = [chat_id.strip() for chat_id in RECEIVERS.split(",") if chat_id.strip()]


# 📤 Función para enviar mensajes
def send_msg(chat_id, text):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(URL, json=data)

# 🔔 Función para notificar a todos
def notify_all(text):
    for chat_id in RECEIVERS:
        send_msg(chat_id, text)

# 📲 Webhook de Telegram
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "✅ Bot funcionando", 200

    data = request.get_json()
    print("📩 Datos recibidos:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_msg(chat_id, "¡Hola! Este es el timbre. Tocá el botón para avisar que estás abajo.")
            send_button(chat_id)

        elif text == "🚪 Tocar timbre":
            notify_all("🚨 Tocaron el timbre.")


    return "ok", 200

# 📦 Botón "Tocar timbre"
def send_button(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    button = {
        "chat_id": chat_id,
        "text": "Tocá el timbre 👇",
        "reply_markup": {
            "keyboard": [[{"text": "🚪 Tocar timbre"}]],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    }
    requests.post(url, json=button)

