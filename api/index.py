# Imports necesarios
# Flask para el API, Anthropic para IA, requests para llamadas HTTP externas
from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import json
import requests

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Variables de entorno (Vercel)
# Claves sensibles almacenadas fuera del código
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
FLEXXIBLE_BASIC_TOKEN = os.environ["FLEXXIBLE_BASIC_TOKEN"]

# Cliente de Anthropic inicializado con API key
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Función encargada de ejecutar acciones contra la API de Flexxible
# Recibe el JSON generado por la IA y lo traduce a una llamada HTTP
def ejecutar_accion(data):
    try:
        accion = data.get("accion")

        # Routing de acciones según tipo detectado por la IA
        if accion == "reiniciar_servicio":
            url = "https://tu-api/restart"

        elif accion == "ejecutar_script":
            url = "https://tu-api/script"

        elif accion == "estado":
            url = "https://tu-api/status"

        else:
            return {
                "status": "ignored",
                "reason": "accion desconocida"
            }

        # Llamada HTTP a la API externa con autenticación Basic
        response = requests.post(
            url,
            json=data,
            headers={
                "Authorization": f"Basic {FLEXXIBLE_BASIC_TOKEN}",
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

# Endpoint principal del chatbot
# Recibe texto del usuario, lo procesa con IA y ejecuta acciones
@app.route("/api", methods=["POST"])
def handle():
    try:
        # Lectura del cuerpo de la petición
        data = request.get_json()
        text = data.get("text", "")

        # Llamada al modelo de IA para interpretar el texto
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Eres un sistema de gestión de incidencias IT.

Convierte el mensaje en JSON válido con estructura:

{
  "accion": "reiniciar_servicio | ejecutar_script | estado | desconocido",
  "dispositivo": "string",
  "descripcion": "string breve"
}

Mensaje:
{text}

Responde SOLO JSON sin texto adicional.
"""
                }
            ]
        )

        # Respuesta cruda del modelo
        result_text = response.content[0].text

        # Conversión de string JSON a objeto Python
        parsed = json.loads(result_text)

        # Ejecución de la acción en el sistema externo
        execution = ejecutar_accion(parsed)

        # Respuesta final del endpoint
        return jsonify({
            "ok": True,
            "interpreted": parsed,
            "execution": execution
        })

    except Exception as e:
        # Manejo global de errores
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# Punto de entrada requerido por Vercel
app = app
