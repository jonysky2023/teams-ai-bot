import json
from http.server import BaseHTTPRequestHandler
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def interpretar(texto: str):
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": f"""
Eres un sistema de incidentes IT.

Convierte el texto en JSON:

{{
  "accion": "reiniciar_servicio | ejecutar_script | estado | desconocido",
  "dispositivo": "string",
  "descripcion": "string"
}}

Mensaje:
{texto}

Responde SOLO JSON válido.
"""
            }
        ]
    )

    return response.content[0].text


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)

        data = json.loads(body)
        text = data.get("text", "")

        result = interpretar(text)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({
            "ok": True,
            "result": result
        }).encode())
