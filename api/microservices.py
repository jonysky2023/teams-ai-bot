MICROSERVICES = [
    {
        "id": "68cabe36cbe8922b3bf96dd9",
        "name": "Vaciar papelera de reciclaje",
        "description": "Vacía la papelera de reciclaje para todos los usuarios del dispositivo, liberando espacio en disco.",
        "keywords": ["papelera", "vaciar papelera", "recycle bin", "liberar espacio"]
    },
    {
        "id": "69ea36a7e100518d61d24002",
        "name": "Instalar Zoom",
        "description": "Descarga e instala Zoom 7.0.2.34412 en el dispositivo.",
        "keywords": ["zoom", "instalar zoom", "videoconferencia", "reuniones"]
    },
    {
        "id": "68a8557c04251ae4a7cd3ab6",
        "name": "Restablecer cola de impresión",
        "description": "Reinicia y restablece la cola de impresión del dispositivo. Útil cuando los documentos se quedan atascados en la cola.",
        "keywords": ["cola impresión", "reiniciar impresora", "atascado", "restablecer impresión"]
    },
    {
        "id": "6745da6fc062c421a01a4654",
        "name": "Limpieza de temporales",
        "description": "Elimina archivos temporales del sistema para liberar espacio en disco y mejorar el rendimiento.",
        "keywords": ["temporales", "limpiar disco", "liberar espacio", "temp", "limpieza"]
    },
    {
        "id": "69e1040e9ac2c51da41611db",
        "name": "Instalar 7-Zip",
        "description": "Descarga e instala 7-Zip en silencio en el dispositivo.",
        "keywords": ["7-zip", "7zip", "rar", "zip", "comprimir", "descomprimir", "instalar 7-zip"]
    }
]


def get_microservices_catalog() -> str:
    lines = ["Microservicios disponibles para ejecutar en el dispositivo:"]
    for ms in MICROSERVICES:
        lines.append(f"- [{ms['id']}] {ms['name']}: {ms['description']}")
    return "\n".join(lines)


def get_microservice_by_id(microservice_id: str) -> dict | None:
    for ms in MICROSERVICES:
        if ms["id"] == microservice_id:
            return ms
    return None
