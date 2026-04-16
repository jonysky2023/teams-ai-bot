import os  # ✅ esto faltaba

WORKSPACES = {
    "default": {
        "api_baseurl": os.getenv("API_BASEURL"),
        "api_user": os.getenv("API_USER"),
        "api_pass": os.getenv("API_PASS"),
        "enabled_tools": [
            "get_device_status",
            "get_service_info",
            "restart_service"
        ]
    },

    "client_a": {
        "api_baseurl": "https://client-a.api.com",
        "api_user": "user_a",
        "api_pass": "pass_a",
        "enabled_tools": [
            "get_device_status",
            "get_user_info"
        ]
    }
}


def get_workspace(name: str):
    """Devuelve la config del workspace por nombre."""
    return WORKSPACES.get(name, WORKSPACES["default"])


def find_workspace(device_name: str):
    """
    Busca un dispositivo por nombre.
    Sustituye el cuerpo por una llamada real a tu API, por ejemplo:

        config = get_workspace("default")
        response = requests.get(
            f"{config['api_baseurl']}/devices?name={device_name}",
            auth=(config["api_user"], config["api_pass"])
        )
        return response.json() if response.ok else None
    """
    if not device_name:
        return None

    workspace = WORKSPACES.get(device_name)
    if workspace:
        return {"Name": device_name, "FlexxibleMID": "N/A", **workspace}

    return None
