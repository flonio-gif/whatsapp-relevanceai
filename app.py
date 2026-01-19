from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# 🔹 Remplace par ta vraie clé RelevanceAI
RELEVANCE_API_KEY = "sk-MTNjNTM5MzEtMzMxNy00ZTYwLThmMzMtZDMwOTkzMDY4MGYz"

# 🔹 URL RelevanceAI via IP directe pour contourner le problème DNS
RELEVANCE_HOST = "https://172.67.71.250/v1/generate"  # IP du nslookup

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "")
    print("Message reçu :", incoming_msg)

    try:
        # 🔹 Données envoyées à RelevanceAI
        data = {
            "prompt": incoming_msg,
            "model": "gpt-relevance-1",  # Modèle IA
            "max_tokens": 150
        }

        # 🔹 Headers avec Host correct
        headers = {
            "Authorization": f"Bearer {RELEVANCE_API_KEY}",
            "Content-Type": "application/json",
            "Host": "api.relevanceai.com"
        }

        # 🔹 Appel HTTP
        resp = requests.post(RELEVANCE_HOST, json=data, headers=headers)

        # 🔹 Debug : statut et réponse brute
        print("Status code RelevanceAI:", resp.status_code)
        print("Response raw RelevanceAI:", resp.text)

        result = resp.json()
        reply_text = result.get("text", "Pas de réponse IA.")

    except Exception as e:
        print("Erreur API RelevanceAI:", e)
        reply_text = "Erreur lors de l'appel IA."

    # 🔹 Réponse à WhatsApp via Twilio
    resp_twilio = MessagingResponse()
    resp_twilio.message(reply_text)
    return str(resp_twilio)

@app.route("/")
def home():
    return "Flask est en ligne ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

