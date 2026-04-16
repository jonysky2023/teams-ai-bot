export const tools = [
  /**
   * =========================
   * DEVICE TOOLS
   * =========================
   */

  {
    name: "get_device_status",
    description: "Obtiene el estado actual de un dispositivo corporativo (online, offline, health, etc.)",
    input_schema: {
      type: "object",
      properties: {
        device: {
          type: "string",
          description: "Nombre del dispositivo (ej: portátil de Juan)"
        }
      },
      required: ["device"]
    }
  },

  {
    name: "get_device_info",
    description: "Obtiene información general del dispositivo (modelo, usuario asignado, IP, etc.)",
    input_schema: {
      type: "object",
      properties: {
        device: {
          type: "string"
        }
      },
      required: ["device"]
    }
  },

  /**
   * =========================
   * SERVICE TOOLS
   * =========================
   */

  {
    name: "get_service_status",
    description: "Consulta el estado de un servicio concreto en un dispositivo",
    input_schema: {
      type: "object",
      properties: {
        device: {
          type: "string"
        },
        service: {
          type: "string",
          description: "Nombre del servicio (ej: X, VPN, Agent, etc.)"
        }
      },
      required: ["device", "service"]
    }
  },

  {
    name: "restart_service",
    description: "Reinicia un servicio en un dispositivo (acción controlada)",
    input_schema: {
      type: "object",
      properties: {
        device: {
          type: "string"
        },
        service: {
          type: "string"
        }
      },
      required: ["device", "service"]
    }
  },

  /**
   * =========================
   * USER / IDENTITY TOOLS
   * =========================
   */

  {
    name: "get_user_devices",
    description: "Obtiene todos los dispositivos asignados a un usuario",
    input_schema: {
      type: "object",
      properties: {
        user: {
          type: "string",
          description: "Nombre del usuario (ej: Juan)"
        }
      },
      required: ["user"]
    }
  },

  {
    name: "get_user_info",
    description: "Obtiene información de un usuario (departamento, rol, dispositivos, etc.)",
    input_schema: {
      type: "object",
      properties: {
        user: {
          type: "string"
        }
      },
      required: ["user"]
    }
  }
]
