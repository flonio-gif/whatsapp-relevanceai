import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

RELEVANCE_API_KEY = os.getenv("RELEVANCE_API_KEY")

def call_relevance_ai(user_message):
    url = "https://api.relevance.ai/v1/generate"

    headers = {
        "Authorization": f"Bearer {RELEVANCE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": user_message,
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)

    if response.status_code != 200:
        raise Exception(f"RelevanceAI error {response.status_code}")

    data = response.json()

    # 🔴 important : on sécurise l'accès
    return data.get("output", "Désolé, je n’ai pas compris 😕")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print("Message reçu :", incoming_msg)

    resp = MessagingResponse()

    try:
        ai_response = call_relevance_ai(incoming_msg)
        resp.message(ai_response)
    except Exception as e:
        print("Erreur RelevanceAI :", e)
        resp.message("⚠️ Désolé, l’IA est temporairement indisponible.")

    return str(resp)

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp AI agent running 🚀", 200
