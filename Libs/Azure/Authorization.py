# Import Libraries
import requests

import Libs.Defaults_Lists as Defaults_Lists

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()

def Exchange_OAuth(Settings: dict, User_Password: str) -> str:
    User_Email = Settings["General"]["User"]["Email"]

    if not client_id:
        CTkMessagebox(title="Error", message=f"No client_id found. Check your .env file.", icon="cancel", fade_in_duration=1)
    if not client_secret:
        CTkMessagebox(title="Error", message=f"No client_secret found. Check your .env file.", icon="cancel", fade_in_duration=1)
    if not tenant_id:
        CTkMessagebox(title="Error", message=f"No tenant_id found. Check your .env file.", icon="cancel", fade_in_duration=1)

    # OAuth2 authentication at KM Azure
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "username": User_Email,
        "password": User_Password}
    response = requests.post(url=url, data=payload)
    tokens = response.json()
    access_token = tokens["access_token"]

    return access_token