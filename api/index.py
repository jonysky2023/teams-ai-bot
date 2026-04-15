from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests

app = Flask(__name__)

# 🔑 API KEY
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


# =========================
# MAIN ENDPOINT
# =========================
@app.route("/api", methods=["POST"])
def slack_handler():
    data = request.get_json()

    # =========================
    # 1. SLACK URL VERIFICATION (OBLIGATORIO)
    # =========================
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})


    # =========================
    # 2. EXTRAER TEXTO (Slack o Postman)
    # =========================
    text = ""
    channel = None

    # Slack event
    if "event" in data:
        event = data["event"]

        # ignorar bots
        if event.get("bot_id"):
            return jsonify({"ok": True})

        text = event.get("text", "")
        channel = event.get("channel")

    # Postman / test manual
    else:
        text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text received"}), 400


    # =========================
    # 3. IA (Anthropic Claude)
    # =========================
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""
Eres un sistema IT.

Convierte el mensaje en JSON:

{{
  "accion": "reiniciar_servicio | ejecutar_script | estado | desconocido",
  "dispositivo": "string",
  "descripcion": "string breve"
}}

Mensaje:
{text}

Devuelve SOLO JSON válido.
"""
            }
        ]
    )

    result = response.content[0].text


    # =========================
    # 4. RESPONDER A SLACK
    # =========================
    if channel and SLACK_BOT_TOKEN:
        try:
            requests.post(
                "https://slack.com/api/chat.postMessage",
                headers={
                    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "channel": channel,
                    "text": result
                }
            )
        except Exception as e:
            print("Slack error:", e)


    # =========================
    # 5. RESPUESTA HTTP NORMAL
    # =========================
    return jsonify({
        "ok": True,
        "result": result
    })


# necesario para Vercel
app = app
