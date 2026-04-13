from flask import Flask, request, jsonify
from anthropic import Anthropic
import os

# Crear app Flask
app = Flask(__name__)

# Cliente de Anthropic (usa variable de entorno en Vercel)
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@app.route("/api", methods=["POST"])
def handle():
    try:
        # Leer JSON de entrada
        data = request.get_json()
        text = data.get("text", "")

        # Llamada a Claude Sonnet
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
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

        # Respuesta del modelo
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


# 🔥 IMPORTANTE: exportar app para Vercel
app = app
