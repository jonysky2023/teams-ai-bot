from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests

app = Flask(__name__)

# 🔑 Anthropic API Key (Vercel env var)
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# 🔑 Slack token (opcional si quieres responder en Slack)
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


@app.route("/api", methods=["POST"])
def handle():
    try:
        data = request.get_json()

        # =========================
        # 1. DETECTAR ORIGEN
        # =========================

        text = ""

        # Slack Events API
        if data and "event" in data:
            event = data["event"]

            # evitar bots
            if event.get("bot_id"):
                return jsonify({"ok": True, "ignored": True})

            text = event.get("text", "")
            channel = event.get("channel")

        # Postman / manual test
        else:
            text = data.get("text", "")
            channel = None

        if not text:
            return jsonify({"ok": False, "error": "No text received"}), 400

        # =========================
        # 2. LLAMADA A CLAUDE
        # =========================

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Eres un sistema IT.

Convierte el mensaje en JSON estructurado:

{{
  "accion": "reiniciar_servicio | ejecutar_script | estado | desconocido",
  "dispositivo": "string",
  "descripcion": "string breve"
}}

Mensaje:
{text}

Responde SOLO JSON válido.
"""
                }
            ]
        )

        result = response.content[0].text

        # =========================
        # 3. RESPUESTA A SLACK (si viene de Slack)
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
                print("Slack send error:", e)

        # =========================
        # 4. RESPUESTA GENERAL
        # =========================

        return jsonify({
            "ok": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# 🔥 necesario para Vercel
app = app
