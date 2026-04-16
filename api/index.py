from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import tools
from workspaces import find_workspace, fetch_device_status, find_device_by_slack_user

app = Flask(__name__)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


def format_device_info(ws: dict) -> str:
    return (
        f"💻 *Dispositivo:* {ws.get('FullName', 'N/A')}\n"
        f"🆔 *FlexxibleMID:* {ws.get('FlexxibleMID', 'N/A')}\n"
        f"👤 *Usuario:* {ws.get('UserName', 'N/A')}\n"
        f"🌐 *IP:* {ws.get('IP', 'N/A')}\n"
        f"🖥️ *OS:* {ws.get('OperatingSystem', 'N/A')}\n"
        f"⚡ *Estado:* {ws.get('PowerState', 'N/A')} / Agente: {ws.get('FlexxAgentStatus', 'N/A')}"
    )


def format_device_status(status: dict) -> str:
    return (
        f"📡 *Estado de {status.get('name', 'N/A')}*\n"
        f"⚡ *Power / Agente:* {status.get('online', 'N/A')}\n"
        f"🖥️ *CPU:* {status.get('cpu', 'N/A')}%\n"
        f"💾 *RAM:* {status.get('memory', 'N/A')}%\n"
        f"💿 *Disco:* {status.get('disk', 'N/A')}\n"
        f"🕐 *Última actividad:* {status.get('last_seen', 'N/A')}\n"
        f"🛡️ *Antivirus:* {status.get('antivirus', 'N/A')}\n"
        f"🔄 *Último reinicio:* hace {status.get('last_restart', 'N/A')} días\n"
        f"🌐 *IP:* {status.get('ip', 'N/A')}\n"
        f"🖥️ *OS:* {status.get('os', 'N/A')}"
    )


@app.route("/api", methods=["POST"])
def slack_handler():
    # Ignorar reintentos de Slack para evitar duplicados
    if request.headers.get("X-Slack-Retry-Num"):
        return jsonify({"ok": True}), 200

    data = request.get_json()

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    text = ""
    channel = None
    slack_user_id = None

    if "event" in data:
        event = data["event"]
        if event.get("bot_id"):
            return jsonify({"ok": True})
        text = event.get("text", "")
        channel = event.get("channel")
        slack_user_id = event.get("user")  # ✅ capturar user_id de Slack
    else:
        text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text received"}), 400

    # ✅ Intentar encontrar el dispositivo del usuario automáticamente
    user_device = None
    if slack_user_id and SLACK_BOT_TOKEN:
        user_device = find_device_by_slack_user(slack_user_id, SLACK_BOT_TOKEN)

    # Construir contexto para Claude
    device_context = ""
    if user_device:
        device_context = (
            f"\nEl usuario que escribe tiene asignado el dispositivo: "
            f"{user_device.get('FullName')} (Usuario: {user_device.get('UserName')}). "
            f"Usa este dispositivo directamente sin preguntar su nombre."
        )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        tools=tools,
        tool_choice={"type": "auto"},
        system=(
            "Eres un asistente IT. Cuando el usuario pida información sobre su dispositivo "
            "SIEMPRE usa las tools disponibles con el nombre de dispositivo que se te indica. "
            "Nunca respondas con JSON en crudo. Nunca inventes datos. "
            "Si no puedes usar una tool, di que no tienes esa información."
        ),
        messages=[
            {
                "role": "user",
                "content": text + device_context
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
            # Si Claude no especificó nombre pero tenemos el dispositivo del usuario
            ws = find_workspace(device_name) if device_name else user_device
            if not ws:
                slack_message = f"❌ No encontrado: *{device_name}*"
            else:
                slack_message = format_device_info(ws)

        elif tool_call.name == "get_device_status":
            device_name = tool_call.input.get("device_name")
            ws = find_workspace(device_name) if device_name else user_device
            if not ws:
                slack_message = f"❌ No se pudo obtener el estado de: *{device_name}*"
            else:
                status = fetch_device_status(ws)
                slack_message = format_device_status(status)

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
