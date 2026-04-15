from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests

from tools import tools
from workspaces import find_workspace

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
    # 1. SLACK URL VERIFICATION
    # =========================
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})


    # =========================
    # 2. EXTRAER TEXTO
    # =========================
    text = ""
    channel = None

    if "event" in data:
        event = data["event"]

        # ignorar bots
        if event.get("bot_id"):
            return jsonify({"ok": True})

        text = event.get("text", "")
        channel = event.get("channel")

    else:
        text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text received"}), 400


    # =========================
    # 3. CLAUDE CON TOOLS
    # =========================
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": f"""
El usuario puede pedir información de dispositivos.

Si pide datos de un equipo, DEBES usar la tool get_workspace_info.

Mensaje:
{text}
"""
            }
        ]
    )


    # =========================
    # 4. DETECTAR TOOL CALL
    # =========================
    tool_call = None

    for block in response.content:
        if block.type == "tool_use":
            tool_call = block


    # =========================
    # 5. EJECUTAR TOOL
    # =========================
    slack_message = "No se pudo procesar la solicitud"

    if tool_call:

        if tool_call.name == "get_workspace_info":

            device_name = tool_call.input.get("device_name")

            ws = find_workspace(device_name)

            if not ws:
                slack_message = f"❌ No encontrado: {device_name}"
            else:
                slack_message = f"""
💻 Dispositivo: {ws.get('Name')}
🆔 FlexxibleMID: {ws.get('FlexxibleMID')}
📊 Datos completos: {ws}
"""


    else:
        # fallback si Claude no usa tool
        slack_message = response.content[0].text


    # =========================
    # 6. RESPONDER A SLACK
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
                    "text": slack_message
                }
            )
        except Exception as e:
            print("Slack error:", e)


    # =========================
    # 7. RESPUESTA HTTP
    # =========================
    return jsonify({
        "ok": True,
        "response": slack_message
    })


# necesario para Vercel
app = app
