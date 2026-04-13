from flask import Flask, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

# Cliente Anthropic (usa variable de entorno en Vercel)
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@app.route("/api", methods=["POST"])
def handle():
    try:
        # Leer request
        data = request.get_json()
        text = data.get("text", "")

        # Llamada a Claude (modelo accesible)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Eres un sistema de gestión de incidencias IT.

Convierte el mensaje en JSON:

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

        result_text = response.content[0].text

        return jsonify({
            "ok": True,
            "result": result_text
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# 🔥 necesario para Vercel
app = app
