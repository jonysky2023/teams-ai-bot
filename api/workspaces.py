import os
import requests

# ─── Configuración Gen 2 ───────────────────────────────────────────────────────
# Variables de entorno necesarias en Vercel:
#   FLEXXIBLE_API_KEY   → API key de Flexxible Gen 2
#   FLEXXIBLE_ORG_ID    → organization_id de tu organización
#   DEFAULT_DEVICE      → nombre del dispositivo (ya existía)

API_BASE = "https://api.flexxible.net/v1"  # Gen 2, versión v1

def _headers() -> dict:
    return {
        "x-api-key": os.environ["FLEXXIBLE_API_KEY"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def _org_id() -> str:
    return os.environ["FLEXXIBLE_ORG_ID"]


# ─── Workspaces ───────────────────────────────────────────────────────────────

def get_workspace(name: str) -> dict:
    """Compatibilidad con el código anterior — devuelve config básica."""
    return {"name": name}


def find_workspace(device_name: str) -> dict | None:
    """Busca un workspace por nombre/FullName usando la API Gen 2."""
    if not device_name:
        return None

    try:
        # Filtro JSON según estructura AST de FilterNode de Flexxible Gen 2
        import json
        filter_str = json.dumps({
            "field": "name",
            "operator": "contains",
            "value": device_name
        })

        response = requests.get(
            f"{API_BASE}/workspaces",
            headers=_headers(),
            params={
                "organizationId": _org_id(),
                "filter": filter_str,
                "pageSize": 10
            },
            timeout=10
        )

        if not response.ok:
            print(f"Flexxible API error: {response.status_code} {response.text[:200]}")
            return None

        data = response.json()
        items = data.get("items", data.get("data", []))

        if not items:
            return None

        device_name_lower = device_name.lower()

        # Coincidencia exacta primero
        for item in items:
            name_field = item.get("name", item.get("fullName", item.get("FullName", "")))
            if name_field.lower() == device_name_lower:
                return item

        # Coincidencia parcial
        for item in items:
            name_field = item.get("name", item.get("fullName", item.get("FullName", "")))
            if device_name_lower in name_field.lower():
                return item

        return None

    except Exception as e:
        print(f"Error conectando con Flexxible: {e}")
        return None


def fetch_device_status(device_name: str, workspace_name: str = "default") -> dict | None:
    """Obtiene el estado del workspace/dispositivo desde Gen 2."""
    device = find_workspace(device_name)
    if not device:
        return None

    # Gen 2 usa snake_case en los campos — mapeamos los conocidos
    # y hacemos fallback a los campos legacy por compatibilidad
    def g(key_new, key_old=None, default="N/A"):
        return device.get(key_new, device.get(key_old, default) if key_old else default)

    return {
        "full_name":            g("name", "FullName"),
        "user":                 g("userName", "UserName"),
        "flexxible_mid":        g("id", "FlexxibleMID"),

        "power_state":          g("powerState", "PowerState"),
        "agent_status":         g("agentStatus", "FlexxAgentStatus"),
        "agent_version":        g("agentVersion", "FlexxAgentVersion"),
        "last_report":          g("lastReport", "FlexxAgentLastReport"),
        "last_seen":            g("lastSeen", "LastTime"),
        "last_restart_days":    g("lastRestartInDays", "LastRestartInDays"),
        "reboot_pending":       g("rebootPending", "RebootPending"),
        "sessions":             g("sessionsCount", "SessionsCount"),
        "idle_time":            g("idleTime", "IdleTime"),

        "ip":                   g("ip", "IP"),
        "public_ip":            g("publicIp", "PublicIP"),
        "mac":                  g("macAddress", "MACAddress"),
        "network_type":         g("networkInterfaceType", "NetworkInterfaceType"),
        "wifi_signal":          g("connectionSignal", "ConnectionSignal"),

        "cpu":                  g("cpu", "CPU"),
        "memory":               g("percentRam", "PercentRAM"),
        "max_ram_gb":           g("maxRam", "MaxRAM"),
        "disk_pct":             g("bootHardDiskUsedPercentage", "BootHardDiskUsedPercentage"),
        "disk_detail":          g("hardDiskCSize", "HardDiskCSize"),

        "os":                   g("operatingSystem", "OperatingSystem"),
        "os_build":             g("osBuildNumber", "OSBuildNumber"),
        "last_windows_update":  g("lastWindowsUpdate", "LastWindowsUpdate"),
        "days_since_update":    g("lastWindowsUpdateInDays", "LastWindowsUpdateInDays"),

        "antivirus":            g("antivirus", "Antivirus"),
        "antivirus_status":     g("antivirusStatus", "AntivirusStatus"),
        "crowdstrike":          g("crowdStrikeStatus", "CrowdStrikeStatus"),
        "compliance":           g("complianceResult", "ComplianceResult"),

        "city":                 g("city", "City"),
        "country":              g("country", "Country"),
        "department":           g("department", "Department"),
        "reporting_group":      g("reportingGroup", "ReportingGroup"),
        "tenant":               g("tenant", "RGTenant"),
    }


# ─── Microservicios ───────────────────────────────────────────────────────────

def run_microservice(microservice_id: str, flx_unique_id: str, display_name: str = "Task from FlexxiBot") -> dict | None:
    """
    Ejecuta un microservicio en un dispositivo via Flexxible API Gen 2.
    Gen 2 usa el endpoint de Operaciones para ejecutar microservicios.
    """
    try:
        payload = {
            "organizationId": _org_id(),
            "name": display_name,
            "type": "MICROSERVICE",
            "microserviceId": microservice_id,
            "scope": {
                "type": "WORKSPACE",
                "workspaceIds": [flx_unique_id]
            }
        }

        response = requests.post(
            f"{API_BASE}/operations",
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
