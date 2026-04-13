from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import json
import requests
import base64

# =========================
# INIT APP
# =========================
app = Flask(__name__)

# =========================
# ENV VARIABLES (Vercel)
# =========================
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

FLEXXIBLE_BASE_URL = os.environ["FLEXXIBLE_BASE_URL"]
FLEXXIBLE_USER = os.environ["FLEXXIBLE_USER"]
FLEXXIBLE_PASS = os.environ["FLEXXIBLE_PASS"]

# Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)


# =========================
# BASIC AUTH BUILDER
# =========================
def get_basic_auth_header():
    credentials = f"{FLEXXIBLE_USER}:{FLEXXIBLE_PASS}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


# =========================
# FLEXXIBLE API CALL
# =========================
def ejecutar_accion(data):
    try:
        accion = data.get("accion")

        # Routing de acciones
        if accion == "reiniciar_servicio":
            url = f"{FLEXXIBLE_BASE_URL}/restart"

        elif accion == "ejecutar_script":
            url = f"{FLEXXIBLE_BASE_URL}/script"

        elif accion == "estado":
            url = f"{FLEXXIBLE_BASE_URL}/status"

        else:
            return {
                "status": "ignored",
                "reason": "accion desconocida"
            }

        # HTTP request a API externa
        response = requests.post(
            url,
            json=data,
            headers={
                "Authorization": get_basic_auth_header(),
                "Content-Type": "application/json"
            },
            timeout=15
        )

        return {
            "status": "ok",
            "api_response": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# =========================
# MAIN ENDPOINT
# =========================
@app.route("/api", methods=["POST"])
def handle():
    try:
        # Leer request
        data = request.get_json()
        text = data.get("text", "")

        # =========================
        # IA: INTERPRETACIÓN
        # =========================
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Eres un sistema de gestión de incidencias IT.

Convierte el mensaje en JSON válido:

{{
  "accion": "reiniciar_servicio | ejecutar_script | estado | desconocido",
  "dispositivo": "string",
  "descripcion": "string breve"
}}

Mensaje:
{text}

Responde SOLO JSON sin texto adicional.
"""
                }
            ]
        )

        # Resultado IA
        result_text = response.content[0].text

        # Parse JSON
        parsed = json.loads(result_text)

        # Ejecutar acción en sistema externo
        execution = ejecutar_accion(parsed)

        # Respuesta final
        return jsonify({
            "ok": True,
            "interpreted": parsed,
            "execution": execution
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# =========================
# VERCEL ENTRYPOINT
# =========================
app = app
