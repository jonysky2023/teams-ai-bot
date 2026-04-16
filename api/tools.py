tools = [
    {
        "name": "get_workspace_info",
        "description": (
            "Busca información de un dispositivo o workspace por su nombre. "
            "Úsala cuando el usuario pregunte por datos de un equipo, máquina o dispositivo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Nombre exacto o aproximado del dispositivo a buscar"
                }
            },
            "required": ["device_name"]
        }
    },
    {
        "name": "get_device_status",
        "description": (
            "Obtiene el estado actual de un dispositivo: si está online/offline, "
            "uso de CPU, memoria, disco y última vez que se vio activo. "
            "Úsala cuando el usuario pregunte por el estado o salud de un equipo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Nombre del dispositivo del que se quiere conocer el estado"
                },
                "workspace": {
                    "type": "string",
                    "description": "Nombre del workspace al que pertenece el dispositivo (opcional, por defecto 'default')",
                }
            },
            "required": ["device_name"]
        }
    }
]
