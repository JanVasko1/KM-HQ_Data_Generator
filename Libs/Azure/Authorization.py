# Import Libraries
import requests

from CTkMessagebox import CTkMessagebox

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Azure_OAuth(client_id: str, client_secret: str, tenant_id: str) -> str:
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
        "scope": "https://api.businesscentral.dynamics.com/.default"}
    
    response = requests.post(url=url, data=payload)
    tokens = response.json()
    access_token = tokens["access_token"]

    return access_token