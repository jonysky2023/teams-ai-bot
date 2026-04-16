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
    }
]
