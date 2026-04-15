tools = [
    {
        "name": "get_workspace_info",
        "description": "Obtiene información de un dispositivo (workspace) incluyendo su FlexxibleMID",
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Nombre del equipo, por ejemplo jserra"
                }
            },
            "required": ["device_name"]
        }
    }
]
