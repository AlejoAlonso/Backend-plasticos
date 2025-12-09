import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "API de Plásticos Alonso funcionando"})

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json

    if not data:
        return jsonify({"status": "error", "message": "No se recibió JSON"}), 400

    nombre = data.get("nombre")
    email = data.get("email")
    mensaje = data.get("mensaje")

    if not all([nombre, email, mensaje]):
        return jsonify({"status": "error", "message": "Faltan datos"}), 400

    email_data = {
        "sender": {
            "name": "Plásticos Alonso",
            "email": "romixdlujo@gmail.com"   # <-- TU EMAIL VERIFICADO
        },
        "to": [
            {"email": "romixdlujo@gmail.com"}  # <-- DONDE VAS A RECIBIR LOS MENSAJES
        ],
        "subject": f"Nuevo mensaje de {nombre}",
        "textContent": f"Email de contacto: {email}\n\nMensaje:\n{mensaje}"
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers=headers,
            json=email_data
        )

        print("Brevo status:", response.status_code)
        print("Brevo response:", response.text)

        if response.status_code in (200, 201):
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "brevo": response.text}), 400

    except Exception as e:
        return jsonify({"status": "error", "detalle": str(e)}), 500
