tools = [
    {
        "name": "run_microservice",
        "description": (
            "Ejecuta un microservicio (script de automatización) en el dispositivo del usuario. "
            "Úsala cuando el usuario quiera realizar una acción en su equipo como: "
            "limpiar temporales, vaciar papelera, borrar caché de Edge, instalar software, "
            "reiniciar cola de impresión, deshabilitar spooler, etc. "
            "Debes elegir el microservice_id correcto según lo que pida el usuario."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "microservice_id": {
                    "type": "string",
                    "description": "ID del microservicio a ejecutar"
                },
                "microservice_name": {
                    "type": "string",
                    "description": "Nombre descriptivo del microservicio para mostrar al usuario"
                }
            },
            "required": ["microservice_id", "microservice_name"]
        }
    }
]
