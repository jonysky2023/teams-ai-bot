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

conversation_history = {}
last_device = {}
last_device_data = {}       # ✅ cache de todos los datos del dispositivo
waiting_for_device = {}
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


def format_device_data(status: dict) -> str:
    """Formatea todos los datos del dispositivo para pasarlos a Claude como contexto."""
    lines = []
    for key, value in status.items():
        if value not in (None, "N/A", "", False, 0) or key in ("cpu", "memory", "disk_pct", "sessions", "idle_time"):
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


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

    if event_id:
        if event_id in processed_events:
            return jsonify({"ok": True}), 200
        processed_events.add(event_id)
        if len(processed_events) > 1000:
            processed_events.clear()

    # Si esperamos el nombre del dispositivo, guardarlo
    if waiting_for_device.get(channel):
        device_name = text.strip()
        status = fetch_device_status(device_name)
        if not status:
            send_slack_message(channel, f"❌ No encontré ningún dispositivo con el nombre *{device_name}*. ¿Puedes comprobarlo e intentarlo de nuevo?")
            return jsonify({"ok": True}), 200
        last_device[channel] = device_name
        last_device_data[channel] = status
        waiting_for_device[channel] = False
        send_slack_message(channel, f"✅ Dispositivo *{device_name}* encontrado y guardado. ¿Qué quieres saber sobre él?")
        return jsonify({"ok": True}), 200

    # Si no hay dispositivo guardado, preguntar
    if channel not in last_device:
        waiting_for_device[channel] = True
        send_slack_message(channel, "👋 Para ayudarte necesito saber el nombre de tu equipo. ¿Cómo se llama tu dispositivo? (por ejemplo: *DESKTOP-DEFE7N5*)")
        return jsonify({"ok": True}), 200

    # Refrescar datos del dispositivo en cada consulta
    status = fetch_device_status(last_device[channel])
    if status:
        last_device_data[channel] = status

    device_info = format_device_data(last_device_data.get(channel, {}))

    system_prompt = (
        "Eres un asistente IT que responde preguntas sobre dispositivos. "
        "Responde SIEMPRE en el idioma del usuario. "
        "Interpreta errores tipográficos: 'cepu' es CPU, 'hdd' o 'disco' es disco duro. "
        "Nunca inventes datos. Si no tienes el dato, dilo claramente. "
        "Sé conciso y usa emojis para hacer la respuesta más legible en Slack.\n\n"
        f"Datos actuales del dispositivo '{last_device[channel]}':\n{device_info}"
    )

    if channel not in conversation_history:
        conversation_history[channel] = []
    conversation_history[channel].append({"role": "user", "content": text})
    history = conversation_history[channel][-10:]

    try:
        # ✅ Sin tools: Claude responde directamente con los datos del contexto
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            system=system_prompt,
            messages=history
        )

        slack_message = "No se pudo procesar la solicitud."
        for block in response.content:
            if hasattr(block, "text"):
                slack_message = block.text
                break

        conversation_history[channel].append({
            "role": "assistant",
            "content": slack_message
        })

        if channel:
            send_slack_message(channel, slack_message)

    except Exception as e:
        print(f"Error: {e}")
        if channel:
            send_slack_message(channel, "❌ Error interno procesando la solicitud.")

    return jsonify({"ok": True}), 200


app = app
