TOOLS = [
    {
        "name": "get_device_status",
        "description": "Obtiene el estado de un dispositivo",
        "input_schema": {
            "type": "object",
            "properties": {
                "device": {"type": "string"}
            },
            "required": ["device"]
        }
    },
    {
        "name": "get_service_status",
        "description": "Consulta estado de un servicio en un dispositivo",
        "input_schema": {
            "type": "object",
            "properties": {
                "device": {"type": "string"},
                "service": {"type": "string"}
            },
            "required": ["device", "service"]
        }
    },
    {
        "name": "restart_service",
        "description": "Reinicia un servicio en un dispositivo",
        "input_schema": {
            "type": "object",
            "properties": {
                "device": {"type": "string"},
                "service": {"type": "string"}
            },
            "required": ["device", "service"]
        }
    },
    {
        "name": "get_user_devices",
        "description": "Obtiene dispositivos de un usuario",
        "input_schema": {
            "type": "object",
            "properties": {
                "user": {"type": "string"}
            },
            "required": ["user"]
        }
    }
]
