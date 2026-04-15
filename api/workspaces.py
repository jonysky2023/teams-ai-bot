import requests
import os

def get_workspaces():

    url = f"{os.environ['FLEXX_BASE_URL']}/workspaces?apiversion=1"

    auth = (os.environ["FLEXX_USER"], os.environ["FLEXX_PASS"])

    response = requests.get(url, auth=auth)

    return response.json()


def find_workspace(device_name):

    workspaces = get_workspaces()

    device_name = device_name.lower()

    for ws in workspaces:

        name = ws.get("Name", "").lower()

        if name == device_name:
            return ws

    return None
