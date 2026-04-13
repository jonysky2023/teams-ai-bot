import os
import json
import base64
import requests
from anthropic import Anthropic


# =========================
# ENV VARIABLES
# =========================
FLEXXIBLE_BASE_URL = os.environ["FLEXXIBLE_BASE_URL"]
FLEXXIBLE_USER = os.environ["FLEXXIBLE_USER"]
FLEXXIBLE_PASS = os.environ["FLEXXIBLE_PASS"]

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=ANTHROPIC_API_KEY)


# =========================
# AUTH BASIC
# =========================
def get_basic_auth_header():
    credentials = f"{FLEXXIBLE_USER}:{FLEXXIBLE_PASS}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


# =========================
# PARSE BODY (IMPORTANT VERCEL FIX)
# =========================
def parse_body(request):
    try:
        body = request.get("body")

        if not body:
            return {}

        if isinstance(body, str):
            return json.loads(body)

        return body

    except:
        return {}


# =========================
# CLAUDE
# =========================
def interpretar(text):

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": f"""
Devuelve SOLO JSON válido:

{{
  "baseurl_path": "/runMicroserviceAsTask?apiversion=1",
  "body": {{
    "displayname": "string",
    "MicroserviceId": "66e1466f51dcb8b8d0f7a948",
    "FLXUniqueIDList": "bf3c245bf5a2ce7ae67e1b12bc29a731ba4433f7da57211fa21c27c7f9a1808a",
    "SNOWEnvironmentList": "",
    "WorkspaceGroupIDList": ""
  }}
}}

Mensaje:
{text}
"""
            }
        ]
    )

    return json.loads(response.content[0].text)


# =========================
# EXEC API
# =========================
def ejecutar(payload):

    url = FLEXXIBLE_BASE_URL + payload["baseurl_path"]

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
        "http": r.status_code,
        "response": r.text
    }


# =========================
# VERCEL ENTRYPOINT (CORRECTO)
# =========================
def handler(request):

    try:
        body = parse_body(request)
        text = body.get("text", "")

        payload = interpretar(text)
        result = ejecutar(payload)

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


# 🔥 REQUIRED EXPORT FOR VERCEL
app = handler
