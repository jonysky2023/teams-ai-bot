import os
import json
import base64
import requests


# =========================
# ENV VARS
# =========================
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

FLEXXIBLE_BASE_URL = os.environ.get("FLEXXIBLE_BASE_URL")
FLEXXIBLE_USER = os.environ.get("FLEXXIBLE_USER")
FLEXXIBLE_PASS = os.environ.get("FLEXXIBLE_PASS")


# =========================
# BASIC AUTH
# =========================
def get_basic_auth_header():
    credentials = f"{FLEXXIBLE_USER}:{FLEXXIBLE_PASS}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


# =========================
# SIMPLE MOCK IA (TEMP DEBUG)
# =========================
# 🔥 IMPORTANTE: primero hacemos que Vercel funcione
# luego volvemos a meter Anthropic
def fake_ai(text):
    return {
        "accion": "reiniciar_servicio",
        "dispositivo": "test",
        "descripcion": text
    }


# =========================
# FLEXXIBLE CALL
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

    try:
        r = requests.post(
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
            "response": r.text
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# =========================
# VERCEL ENTRYPOINT
# =========================
def handler(request):

    try:
        body = request.get_json(silent=True)

        if not body:
            body = {}

        text = body.get("text", "")

        # 1. IA (temporal fake para debug)
        parsed = fake_ai(text)

        # 2. ejecutar acción
        execution = ejecutar_accion(parsed)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
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
