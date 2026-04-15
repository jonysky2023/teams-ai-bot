export default async function handler(req, res) {
  const body = req.body;

  // 1. Verificación inicial de Slack
  if (body?.type === "url_verification") {
    return res.status(200).send(body.challenge);
  }

  // 2. Evitar loops / bots
  const event = body?.event;
  if (!event || event.bot_id) {
    return res.status(200).send("ok");
  }

  // 3. Filtrar solo mensajes reales
  const text = event.text;
  const channel = event.channel;

  if (!text) {
    return res.status(200).send("no text");
  }

  try {
    // 4. Llamada a tu IA (Claude / Sonnet / OpenAI)
    const aiResponse = await processAI(text);

    // 5. Responder a Slack
    await fetch("https://slack.com/api/chat.postMessage", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.SLACK_BOT_TOKEN}`,
      },
      body: JSON.stringify({
        channel: channel,
        text: aiResponse,
      }),
    });

    return res.status(200).send("ok");
  } catch (err) {
    console.error(err);
    return res.status(500).send("error");
  }
}

/**
 * 🔥 TU IA (ejemplo)
 * Sustituye esto por Claude / Sonnet / OpenAI
 */
async function processAI(text) {
  // Ejemplo simple (puedes reemplazarlo)
  if (text.includes("reinicia")) {
    return "🔧 He procesado la orden de reinicio del servicio.";
  }

  if (text.includes("portátil")) {
    return "💻 Estoy analizando el problema del portátil de Juan.";
  }

  return `🤖 Recibido: ${text}`;
}
