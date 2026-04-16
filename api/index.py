from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import tools
from workspaces import find_workspace, get_workspace, fetch_device_status

app = Flask(__name__)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

conversation_history = {}   # { channel_id: [ {role, content}, ... ] }
last_device = {}            # { channel_id: "DESKTOP-DEFE7N5" }
waiting_for_device = {}     # { channel_id: True/False } — esperando que el usuario diga el nombre
processed_events = set()


def send_slack_message(channel: str, text: str):
    try:
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"channel": channel, "text": text}
        )
    except Exception as e:
        print("Slack error:", e)


@app.route("/api", methods=["POST"])
def slack_handler():
    data = request.get_json()

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    text = ""
    channel = None
    event_id = None

    if "event" in data:
        event = data["event"]
        if event.get("bot_id"):
            return jsonify({"ok": True})
        text = event.get("text", "").strip()
        channel = event.get("channel")
        event_id = data.get("event_id")
    else:
        text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text received"}), 400

    # Deduplicar por event_id
    if event_id:
        if event_id in processed_events:
            return jsonify({"ok": True}), 200
        processed_events.add(event_id)
        if len(processed_events) > 1000:
            processed_events.clear()

    # ✅ Si estábamos esperando el nombre del dispositivo, guardarlo directamente
    if waiting_for_device.get(channel):
        device_name = text.strip()
        last_device[channel] = device_name
        waiting_for_device[channel] = False
        send_slack_message(channel, f"✅ Dispositivo *{device_name}* guardado. ¿Qué quieres saber sobre él?")
        return jsonify({"ok": True}), 200

    # ✅ Si no hay dispositivo guardado, preguntar antes de hacer nada
    if channel not in last_device:
        waiting_for_device[channel] = True
        send_slack_message(channel, "👋 Para ayudarte necesito saber el nombre de tu equipo. ¿Cómo se llama tu dispositivo? (por ejemplo: *DESKTOP-DEFE7N5*)")
        return jsonify({"ok": True}), 200

    # A partir de aquí siempre hay dispositivo guardado
    device_context = (
        f"El usuario está trabajando con el dispositivo '{last_device[channel]}'. "
        f"Usa SIEMPRE ese dispositivo para cualquier consulta sin volver a preguntarlo. "
        f"Interpreta errores tipográficos: 'cepu' es CPU, 'ram' es memoria, 'hdd' o 'disco' es disco duro."
    )

    system_prompt = (
        "Eres un asistente IT que consulta el estado de dispositivos. "
        "Usa siempre las tools disponibles. Nunca respondas con JSON en crudo. Nunca inventes datos. "
        + device_context
    )

    # Historial de conversación
    if channel not in conversation_history:
        conversation_history[channel] = []
    conversation_history[channel].append({"role": "user", "content": text})
    history = conversation_history[channel][-10:]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            tools=tools,
            tool_choice={"type": "auto"},
            system=system_prompt,
            messages=history
        )

        tool_call = None
        for block in response.content:
            if block.type == "tool_use":
                tool_call = block
                break

        slack_message = "No se pudo procesar la solicitud."
        assistant_response = ""

        if tool_call:

            if tool_call.name == "get_workspace_info":
                device_name = tool_call.input.get("device_name", last_device[channel])
                last_device[channel] = device_name
                ws = find_workspace(device_name)
                if not ws:
                    slack_message = f"❌ No encontrado: *{device_name}*"
                else:
                    slack_message = (
                        f"💻 *Dispositivo:* {ws.get('FullName', 'N/A')}\n"
                        f"🆔 *FlexxibleMID:* {ws.get('FlexxibleMID', 'N/A')}\n"
                        f"👤 *Usuario:* {ws.get('UserName', 'N/A')}\n"
                        f"🌐 *IP:* {ws.get('IP', 'N/A')}\n"
                        f"🖥️ *OS:* {ws.get('OperatingSystem', 'N/A')}\n"
                        f"⚡ *Estado:* {ws.get('PowerState', 'N/A')} / Agente: {ws.get('FlexxAgentStatus', 'N/A')}"
                    )

            elif tool_call.name == "get_device_status":
                device_name = tool_call.input.get("device_name", last_device[channel])
                last_device[channel] = device_name
                workspace_name = tool_call.input.get("workspace", "default")
                status = fetch_device_status(device_name, workspace_name)
                if not status:
                    slack_message = f"❌ No se pudo obtener el estado de: *{device_name}*"
                else:
                    slack_message = (
                        f"📡 *Estado de {device_name}*\n"
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

            assistant_response = slack_message

        else:
            for block in response.content:
                if hasattr(block, "text"):
                    slack_message = block.text
                    assistant_response = block.text
                    break

        if assistant_response:
            conversation_history[channel].append({
                "role": "assistant",
                "content": assistant_response
            })

        if channel:
            send_slack_message(channel, slack_message)

    except Exception as e:
        print(f"Error: {e}")
        if channel:
            send_slack_message(channel, "❌ Error interno procesando la solicitud.")

    return jsonify({"ok": True}), 200


app = app
