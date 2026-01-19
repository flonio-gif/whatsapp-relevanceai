import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Récupération de la clé RelevanceAI depuis les variables d'environnement
RELEVANCE_API_KEY = os.getenv("RELEVANCE_API_KEY")
RELEVANCE_ENDPOINT = "https://api.relevance.ai/v1/generate"

# Route principale pour le sandbox WhatsApp
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    # Récupérer le message entrant
    incoming_msg = request.values.get("Body", "")
    print("Message reçu :", incoming_msg)

    # Préparer la réponse par défaut si IA échoue
    response_text = "Erreur lors de l'appel IA."

    # Préparer le payload pour RelevanceAI
    payload = {
        "prompt": incoming_msg,
        "model": "gpt-4o-mini"  # tu peux changer le modèle si besoin
    }

    headers = {
        "Authorization": f"Bearer {RELEVANCE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Appel API RelevanceAI
        r = requests.post(RELEVANCE_ENDPOINT, headers=headers, json=payload, timeout=20)
        r.raise_for_status()  # lève une exception si erreur HTTP
        data = r.json()
        # On récupère le texte généré
        response_text = data.get("output", "Réponse IA vide")
    except Exception as e:
        print("Erreur API RelevanceAI:", e)

    # Réponse à Twilio
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

# S'assurer que Flask écoute sur le bon port pour Railway
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
