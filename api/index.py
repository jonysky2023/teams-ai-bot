import os
import json
import base64
import requests
from anthropic import Anthropic


# =========================
# ENV VARIABLES
# =========================
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

FLEXXIBLE_BASE_URL = os.environ["FLEXXIBLE_BASE_URL"]
FLEXXIBLE_USER = os.environ["FLEXXIBLE_USER"]
FLEXXIBLE_PASS = os.environ["FLEXXIBLE_PASS"]

client = Anthropic(api_key=ANTHROPIC_API_KEY)


# =========================
# BASIC AUTH
# =========================
def get_basic_auth_header():
    credentials = f"{FLEXXIBLE_USER}:{FLEXXIBLE_PASS}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


# =========================
# FLEXXIBLE EXECUTION
# =========================
def ejecutar_accion(data):
    accion = data.get("accion")

    if accion == "reiniciar_servicio":
        url = f"{FLEXXIBLE_BASE_URL}/restart"

    elif accion == "ejecutar_script":
        url = f"{FLEXXIBLE_BASE_URL}/script"

    elif accion == "estado":
        url = f"{FLEXXIBLE_BASE_URL}/status"

    else:
        return {"status": "ignored"}

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


# =========================
# VERCEL HANDLER (IMPORTANT)
# =========================
def handler(request):
    try:
        body = request.get_json()
        text = body.get("text", "")

        # IA call
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Convierte esto en JSON:

{{
  "accion": "reiniciar_servicio | ejecutar_script | estado | desconocido",
  "dispositivo": "string",
  "descripcion": "string"
}}

Texto:
{text}

SOLO JSON.
"""
                }
            ]
        )

        result_text = response.content[0].text
        parsed = json.loads(result_text)

        execution = ejecutar_accion(parsed)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "ok": True,
                "interpreted": parsed,
                "execution": execution
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "ok": False,
                "error": str(e)
            })
        }
