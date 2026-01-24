from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body", "")
    print("Message reçu :", incoming_msg)

    resp = MessagingResponse()
    resp.message(f"Tu as dit : {incoming_msg}")

    return str(resp)

@app.route("/")
def home():
    return "Flask WhatsApp is running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
