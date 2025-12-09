from flask import Flask, request, jsonify
from flask_cors import CORS
import yagmail

app = Flask(__name__)
CORS(app)  # Permitir que otros sitios (tu web) hablen con el backend

# PONÉ ACÁ TU GMAIL Y TU CONTRASEÑA DE APLICACIÓN
GMAIL_USER = "romixdlujo@gmail.com"
GMAIL_PASS = "pusa vrnp ygut thse"

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json  # Leemos lo que nos manda el formulario
    nombre = data.get("nombre")
    email = data.get("email")
    mensaje = data.get("mensaje")

    try:
        # Conectarse a Gmail
        yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)

        # Enviar el mail
        yag.send(
            to=GMAIL_USER,  # Te lo mandás a vos mismo
            subject=f"Nuevo mensaje de {nombre}",
            contents=f"Email: {email}\n\nMensaje:\n{mensaje}"
        )

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Error al enviar mail:", e)
        return jsonify({"status": "error", "detalle": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
