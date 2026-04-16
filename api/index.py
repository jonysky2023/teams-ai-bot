from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests
import sys

# 🔥 FIX VERCEL IMPORTS
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import tools
from workspaces import find_workspace, get_workspace

app = Flask(__name__)

# 🔑 API KEYS
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


# =========================
# HELPER: obtener estado del dispositivo
# =========================
def fetch_device_status(device_name: str, workspace_name: str = "default") -> dict | None:
    config = get_workspace(workspace_name)
    base_url = config.get("api_baseurl")
    user = config.get("api_user")
    password = config.get("api_pass")

    if not base_url:
        return None

    try:
        response = requests.get(
            f"{base_url}/devices/{device_name}/status",
            auth=(user, password),
            timeout=10
        )
        if response.ok:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching device status: {e}")
        return None


# =========================
# MAIN ENDPOINT
# =========================
@app.route("/api", methods=["POST"])
def slack_handler():
    data = request.get_json()

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    text = ""
    channel = None

    if "event" in data:
        event = data["event"]
        if event.get("bot_id"):
            return jsonify({"ok": True})
        text = event.get("text", "")
        channel = event.get("channel")
    else:
        text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text received"}), 400

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": f"""
El usuario puede pedir información o el estado de dispositivos.

- Si pide datos o información de un equipo → usa get_workspace_info
- Si pide el estado, salud, si está online/offline → usa get_device_status

Mensaje:
{text}
"""
            }
        ]
    )

    tool_call = None
    for block in response.content:
        if block.type == "tool_use":
            tool_call = block
            break

    slack_message = "No se pudo procesar la solicitud."

    if tool_call:

        if tool_call.name == "get_workspace_info":
            device_name = tool_call.input.get("device_name")
            ws = find_workspace(device_name)
            if not ws:
                slack_message = f"❌ No encontrado: *{device_name}*"
            else:
                slack_message = (
                    f"💻 *Dispositivo:* {ws.get('Name')}\n"
                    f"🆔 *FlexxibleMID:* {ws.get('FlexxibleMID')}\n"
                    f"📊 *Datos completos:* {ws}"
                )

        elif tool_call.name == "get_device_status":
            device_name = tool_call.input.get("device_name")
            workspace_name = tool_call.input.get("workspace", "default")
            status = fetch_device_status(device_name, workspace_name)
            if not status:
                slack_message = f"❌ No se pudo obtener el estado de: *{device_name}*"
            else:
                slack_message = (
                    f"📡 *Estado de {device_name}*\n"
                    f"🟢 Online: {status.get('online', 'desconocido')}\n"
                    f"🖥️ CPU: {status.get('cpu', 'N/A')}%\n"
                    f"💾 RAM: {status.get('memory', 'N/A')}%\n"
                    f"💿 Disco: {status.get('disk', 'N/A')}%\n"
                    f"🕐 Última actividad: {status.get('last_seen', 'N/A')}"
                )

    else:
        for block in response.content:
            if hasattr(block, "text"):
                slack_message = block.text
                break

    if channel and SLACK_BOT_TOKEN:
        try:
            requests.post(
                "https://slack.com/api/chat.postMessage",
                headers={
                    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={"channel": channel, "text": slack_message}
            )
        except Exception as e:
            print("Slack error:", e)

    return jsonify({"ok": True, "response": slack_message})


app = app
