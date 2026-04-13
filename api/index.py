import os
import json
import base64
import requests
from anthropic import Anthropic


# =========================
# ENV VARIABLES (Vercel)
# =========================
FLEXXIBLE_BASE_URL = os.environ["FLEXXIBLE_BASE_URL"]
FLEXXIBLE_USER = os.environ["FLEXXIBLE_USER"]
FLEXXIBLE_PASS = os.environ["FLEXXIBLE_PASS"]

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=ANTHROPIC_API_KEY)


# =========================
# BASIC AUTH
# =========================
def get_basic_auth_header():
    credentials = f"{FLEXXIBLE_USER}:{FLEXXIBLE_PASS}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


# =========================
# IA (CLAUDE GENERA TODO EL BODY)
# =========================
def interpretar(text):

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": f"""
Eres un generador de requests para una API IT.

Devuelve SOLO JSON válido con esta estructura:

{{
  "baseurl_path": "/runMicroserviceAsTask?apiversion=1",
  "body": {{
    "displayname": "string",
    "MicroserviceId": "66e1466f51dcb8b8d0f7a948",
    "FLXUniqueIDList": "string",
    "SNOWEnvironmentList": "",
    "WorkspaceGroupIDList": ""
  }}
}}

REGLAS:
- No texto adicional
- Solo JSON válido
- Inferir valores desde el mensaje del usuario

Mensaje:
{text}
"""
            }
        ]
    )

    return json.loads(response.content[0].text)


# =========================
# EXECUTE API CALL
# =========================
def ejecutar(payload):

    url = FLEXXIBLE_BASE_URL + payload["baseurl_path"]

    try:
        r = requests.post(
            url,
            json=payload["body"],
            headers={
                "Authorization": get_basic_auth_header(),
                "Content-Type": "application/json"
            },
            timeout=20
        )

        return {
            "status": "ok",
            "http_status": r.status_code,
            "response": r.text
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# =========================
# VERCEL HANDLER
# =========================
def handler(request):

    try:
        body = request.get_json(silent=True) or {}
        text = body.get("text", "")

        # 1. Claude genera request completo
        payload = interpretar(text)

        # 2. Ejecutar request generado
        result = ejecutar(payload)

        # 3. respuesta final
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "ok": True,
                "payload": payload,
                "execution": result
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
