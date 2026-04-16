import requests
from requests.auth import HTTPBasicAuth


def run_tool(name, input_data, config):

    auth = HTTPBasicAuth(
        config["api_user"],
        config["api_pass"]
    )

    base_url = config["api_baseurl"]

    if name == "get_device_status":
        url = f"{base_url}/device/status"
        params = {"device": input_data["device"]}
        return requests.get(url, params=params, auth=auth).json()

    if name == "get_service_status":
        url = f"{base_url}/service/status"
        params = {
            "device": input_data["device"],
            "service": input_data["service"]
        }
        return requests.get(url, params=params, auth=auth).json()

    if name == "restart_service":
        url = f"{base_url}/service/restart"
        params = {
            "device": input_data["device"],
            "service": input_data["service"]
        }
        return requests.get(url, params=params, auth=auth).json()

    if name == "get_user_devices":
        url = f"{base_url}/user/devices"
        params = {"user": input_data["user"]}
        return requests.get(url, params=params, auth=auth).json()

    raise Exception(f"Tool no soportada: {name}")
