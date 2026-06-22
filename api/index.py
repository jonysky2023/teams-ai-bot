from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import requests
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import tools
from workspaces import find_workspace, get_workspace, fetch_device_status, run_microservice
from microservices import get_microservices_catalog, get_microservice_by_id

app = Flask(__name__)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
DEFAULT_DEVICE = os.environ["DEFAULT_DEVICE"]  # ej: DESKTOP-DEFE7N5

conversation_history = {}
last_device_data = {}
last_flx_unique_id = {}     # ✅ FLXUniqueID necesario para ejecutar microservicios
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
    lines = []
    for key, value in status.items():
        if value not in (None, "N/A", "", False, 0) or key in ("cpu", "memory", "disk_pct", "sessions", "idle_time"):
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


@app.route("/api", methods=["POST"])
def slack_handler():
    # Ignorar reintentos automáticos de Slack (si tardamos >3s en responder)
    if request.headers.get("X-Slack-Retry-Num"):
        return jsonify({"ok": True}), 200

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

    # Comando especial: limpiar pantalla visualmente
    if text.lower().strip() in (
        "limpiar pantalla", "limpiar chat", "clear",
        "/limpiar pantalla", "/limpiar chat", "/clear", "/reset"
    ):
        conversation_history[channel] = []
        if channel:
            for _ in range(8):
                send_slack_message(channel, "⠀")  # carácter invisible, Slack no lo recorta
            send_slack_message(channel, "🆕 Conversación reiniciada. ¿En qué puedo ayudarte?")
        return jsonify({"ok": True}), 200


    if event_id:
        if event_id in processed_events:
            return jsonify({"ok": True}), 200
        processed_events.add(event_id)
        if len(processed_events) > 1000:
            processed_events.clear()

    # Obtener FLXUniqueID si no lo tenemos cacheado para este canal
    if channel not in last_flx_unique_id:
        device_info = find_workspace(DEFAULT_DEVICE)
        if device_info:
            last_flx_unique_id[channel] = device_info.get("FLXUniqueID") or device_info.get("FlexxibleMID", "")

    # Refrescar datos del dispositivo predefinido
    status = fetch_device_status(DEFAULT_DEVICE)
    if status:
        last_device_data[channel] = status

    device_info_str = format_device_data(last_device_data.get(channel, {}))
    microservices_catalog = get_microservices_catalog()

    system_prompt = (
        "Eres un asistente IT que responde preguntas y ejecuta acciones en dispositivos. "
        "Responde SIEMPRE en el idioma del usuario. "
        "Interpreta errores tipográficos: 'cepu' es CPU, 'hdd' o 'disco' es disco duro. "
        "Nunca inventes datos. Sé conciso y usa emojis para hacer la respuesta más legible en Slack. "
        "Nunca menciones el nombre técnico exacto del dispositivo (ej. códigos tipo DESKTOP-XXXXX); "
        "refiérete a él siempre como 'tu equipo' o 'tu dispositivo'.\n\n"
        f"Dispositivo activo: '{DEFAULT_DEVICE}'\n\n"
        f"Datos actuales del dispositivo:\n{device_info_str}\n\n"
        f"{microservices_catalog}\n\n"
        "Cuando el usuario pida ejecutar una acción en su equipo, usa la tool run_microservice "
        "eligiendo el microservice_id más apropiado del catálogo anterior. "
        "Pide confirmación al usuario antes de ejecutar cualquier acción."
    )

    if channel not in conversation_history:
        conversation_history[channel] = []
    conversation_history[channel].append({"role": "user", "content": text})
    history = conversation_history[channel][-10:]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=600,
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

        if tool_call and tool_call.name == "run_microservice":
            microservice_id = tool_call.input.get("microservice_id")
            microservice_name = tool_call.input.get("microservice_name")
            flx_unique_id = last_flx_unique_id.get(channel, "")

            if not flx_unique_id:
                slack_message = "❌ No tengo el identificador único del dispositivo para ejecutar la acción. Comprueba que el agente Flexxible está activo."
            else:
                result = run_microservice(
                    microservice_id=microservice_id,
                    flx_unique_id=flx_unique_id,
                    display_name=f"{microservice_name} - FlexxiBot"
                )
                if result:
                    slack_message = (
                        f"✅ *{microservice_name}* lanzado correctamente en tu equipo.\n"
                        f"⏳ El script se está ejecutando en el dispositivo. Puede tardar unos minutos."
                    )
                else:
                    slack_message = f"❌ No se pudo ejecutar *{microservice_name}*. Comprueba que el dispositivo está online y el agente activo."

        elif tool_call is None:
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
