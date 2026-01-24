import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

RELEVANCE_API_KEY = os.getenv("RELEVANCE_API_KEY")
WORKFLOW_ID = "7317117e-ed9b-4991-ae1b-2ae64c7916de"

def call_relevance_ai(user_message):
    url = f"https://api.relevance.ai/latest/workflows/{WORKFLOW_ID}/invoke"

    headers = {
        "Authorization": f"Bearer {RELEVANCE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {
            "input": user_message
        }
    }

    response = requests.post(url, json=payload, headers=headers, timeout=20)

    if response.status_code != 200:
        raise Exception(f"RelevanceAI error {response.status_code}: {response.text}")

    data = response.json()

    # 🔎 Extraction robuste de la réponse
    # RelevanceAI peut renvoyer différents formats
    if "output" in data:
        return str(data["output"])

    if "results" in data and len(data["results"]) > 0:
        return str(data["results"][0].get("output", "Réponse vide"))

    return "⚠️ L’agent n’a pas retourné de réponse."

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
        resp.message("⚠️ Désolé, l’agent IA est momentanément indisponible.")

    return str(resp)

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp RelevanceAI agent running 🚀", 200
