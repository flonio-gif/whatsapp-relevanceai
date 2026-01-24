from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print("Message reçu :", incoming_msg)

    # 🤖 Réponse IA MOCK (fausse IA)
    ai_response = (
        f"🤖 IA : Bonjour 👋\n\n"
        f"Tu m’as écrit : \"{incoming_msg}\"\n\n"
        f"Comment puis-je t’aider aujourd’hui ?"
    )

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

@app.route("/", methods=["GET"])
def home():
    return "Serveur WhatsApp Flask actif ✅", 200
