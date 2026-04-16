import os

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
    return WORKSPACES.get(name, WORKSPACES["default"])
