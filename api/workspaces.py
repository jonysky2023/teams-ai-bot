import os
import json
import requests

API_BASE = "https://api.flexxible.net/v1"

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ['FLEXXIBLE_API_KEY']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def _org_id() -> str:
    return os.environ["FLEXXIBLE_ORG_ID"]


def get_workspace(name: str) -> dict:
    return {"name": name}


def find_workspace(device_name: str) -> dict | None:
    if not device_name:
        return None
    try:
        filters = json.dumps({
            "field": "name",
            "op": "contains",
            "value": device_name
        })

        response = requests.get(
            f"{API_BASE}/organizations/{_org_id()}/workspaces",
            headers=_headers(),
            params={
                "filters": filters,
                "per_page": 10
            },
            timeout=10
        )

        print(f"DEBUG find_workspace status: {response.status_code}")
        print(f"DEBUG find_workspace response: {response.text[:300]}")

        if not response.ok:
            print(f"Flexxible API error: {response.status_code} {response.text[:200]}")
            return None

        data = response.json()
        items = data.get("data", [])

        if not items:
            return None

        device_name_lower = device_name.lower()

        for item in items:
            if item.get("name", "").lower() == device_name_lower:
                return item

        for item in items:
            if device_name_lower in item.get("name", "").lower():
                return item

        return None

    except Exception as e:
        print(f"Error conectando con Flexxible: {e}")
        return None


def fetch_device_status(device_name: str, workspace_name: str = "default") -> dict | None:
    device = find_workspace(device_name)
    if not device:
        return None

    return {
        "full_name":            device.get("name", "N/A"),
        "user":                 device.get("user_name", "N/A"),
        "workspace_id":         device.get("workspace_id", "N/A"),

        "status":               device.get("status", "N/A"),
        "power_state":          device.get("power_state", "N/A"),
        "agent_status":         device.get("flexxagent_status", "N/A"),
        "agent_version":        device.get("flexxagent_version", "N/A"),
        "last_connection":      device.get("last_connection_time", "N/A"),
        "last_restart":         device.get("last_restart_time", "N/A"),
        "reboot_pending":       device.get("os_reboot_pending", "N/A"),
        "sessions":             device.get("sessions_count", "N/A"),

        "ip":                   device.get("ip_address", "N/A"),
        "public_ip":            device.get("public_ip", "N/A"),
        "mac":                  device.get("wake_on_lan_mac", "N/A"),
        "subnet":               device.get("current_subnet", "N/A"),
        "gateway":              device.get("default_gateway", "N/A"),
        "network_type":         device.get("network_interface_type", "N/A"),
        "wifi_signal":          device.get("network_signal", "N/A"),

        "cpu":                  device.get("percent_cpu", "N/A"),
        "memory":               device.get("percent_ram", "N/A"),
        "total_ram_mb":         device.get("total_ram", "N/A"),
        "cores":                device.get("cores_count", "N/A"),
        "disk_pct":             device.get("boot_hard_disk_used_percentage", "N/A"),
        "processor":            device.get("processor", "N/A"),
        "is_physical":          device.get("is_physical", "N/A"),
        "is_laptop":            device.get("is_laptop", "N/A"),
        "hypervisor":           device.get("hypervisor", "N/A"),
        "last_boot_duration":   device.get("last_boot_duration", "N/A"),

        "os":                   device.get("operating_system", "N/A"),
        "os_build":             device.get("os_build_number", "N/A"),
        "windows_type":         device.get("windows_type", "N/A"),
        "last_windows_update":  device.get("last_windows_update", "N/A"),
        "days_since_update":    device.get("os_update_num_days_since_last", "N/A"),
        "pending_updates":      device.get("os_update_num_pending", "N/A"),
        "fast_startup":         device.get("os_fast_startup", "N/A"),

        "antivirus":            device.get("antivirus", "N/A"),
        "antivirus_status":     device.get("antivirus_status", "N/A"),
        "antivirus_version":    device.get("antivirus_version_number", "N/A"),
        "edr":                  device.get("edr", "N/A"),
        "edr_status":           device.get("edr_status", "N/A"),
        "compliance":           device.get("compliance_result", "N/A"),
        "encrypted_disks":      device.get("encrypted_harddisks", "N/A"),
        "secure_boot":          device.get("secure_boot_state", "N/A"),

        "bios_version":         device.get("bios_version", "N/A"),
        "bios_manufacturer":    device.get("bios_manufacturer", "N/A"),
        "bios_serial":          device.get("bios_serialnumber", "N/A"),

        "department":           device.get("department", "N/A"),
        "office":               device.get("office", "N/A"),
        "area":                 device.get("area", "N/A"),
        "domain":               device.get("domain_name", "N/A"),
        "ou":                   device.get("ou", "N/A"),

        "iot_status":           device.get("iot_hub_config_sync_status", "N/A"),
        "broker":               device.get("broker", "N/A"),
        "broker_status":        device.get("broker_status", "N/A"),
        "num_alerts":           device.get("num_alerts", "N/A"),
    }


def run_microservice(microservice_id: str, flx_unique_id: str, display_name: str = "Task from FlexxiBot") -> dict | None:
    try:
        payload = {
            "name": display_name,
            "microservice_id": microservice_id,
            "target": {
                "type": "WORKSPACES",
                "ids": [flx_unique_id]
            }
        }

        response = requests.post(
            f"{API_BASE}/organizations/{_org_id()}/operations",
            headers=_headers(),
            json=payload,
            timeout=15
        )

        print(f"DEBUG runMicroservice status: {response.status_code}")
        print(f"DEBUG runMicroservice response: {response.text[:300]}")

        if response.ok:
            return response.json() if response.text else {"ok": True}
        else:
            print(f"Flexxible runMicroservice error: {response.status_code} {response.text}")
            return None

    except Exception as e:
        print(f"Error ejecutando microservicio: {e}")
        return None
