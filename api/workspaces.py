import os
import requests

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


def get_workspace(name: str) -> dict:
    return WORKSPACES.get(name, WORKSPACES["default"])


def find_workspace(device_name: str) -> dict | None:
    if not device_name:
        return None

    config = get_workspace("default")
    base_url = config.get("api_baseurl")
    user = config.get("api_user")
    password = config.get("api_pass")

    print(f"DEBUG base_url: {base_url}")
    print(f"DEBUG user: {user}")
    print(f"DEBUG buscando: {device_name}")

    if not base_url:
        print("ERROR: API_BASEURL no configurada")
        return None

    try:
        url = f"{base_url}/workspaces"
        params = {"apiversion": "1"}
        print(f"DEBUG request: GET {url} params={params} auth=({user}, ***)")

        response = requests.get(
            url,
            params=params,
            auth=(user, password),
            timeout=10
        )

        print(f"DEBUG status: {response.status_code}")
        print(f"DEBUG response (primeros 500 chars): {response.text[:500]}")

        if not response.ok:
            print(f"Flexxible API error: {response.status_code} {response.text}")
            return None

        data = response.json()
        items = data if isinstance(data, list) else data.get("Items", data.get("value", []))
        print(f"DEBUG total items: {len(items)}")
        if items:
            print(f"DEBUG primer item keys: {list(items[0].keys())}")
            print(f"DEBUG primer FullName: {items[0].get('FullName')}")

        device_name_lower = device_name.lower()

        # Match exacto por FullName
        for item in items:
            full_name = item.get("FullName", "")
            if full_name.lower() == device_name_lower:
                return item

        # Match parcial por FullName
        for item in items:
            full_name = item.get("FullName", "")
            if device_name_lower in full_name.lower():
                return item

        print(f"DEBUG: ningún dispositivo coincide con '{device_name}'")
        return None

    except Exception as e:
        print(f"Error conectando con Flexxible: {e}")
        return None


def fetch_device_status(device_name: str, workspace_name: str = "default") -> dict | None:
    device = find_workspace(device_name)
    if not device:
        return None

    power = device.get("PowerState", "Unknown")
    agent = device.get("FlexxAgentStatus", "Unknown")
    online = f"{power} / Agente: {agent}"

    disk = device.get("HardDiskCSize", "N/A")
    disk_pct = device.get("BootHardDiskUsedPercentage", "N/A")

    return {
        "online": online,
        "cpu": device.get("CPU", "N/A"),
        "memory": device.get("PercentRAM", "N/A"),
        "disk": f"{disk_pct}% ({disk})",
        "last_seen": device.get("LastTime", "N/A"),
        "os": device.get("OperatingSystem", "N/A"),
        "ip": device.get("IP", "N/A"),
        "antivirus": device.get("AntivirusStatus", "N/A"),
        "last_restart": device.get("LastRestartInDays", "N/A"),
    }
