# Import Libraries
import requests

import Libs.GUI.Elements as Elements

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Azure_OAuth(Configuration: dict, client_id: str, client_secret: str, tenant_id: str) -> str:
    if not client_id:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="No client_id found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    if not client_secret:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="No client_secret found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    if not tenant_id:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="No tenant_id found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

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

def Azure_OAuth_Test(Configuration: dict, client_id: str, client_secret: str, tenant_id: str) -> str:
    try:
        if not client_id:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="No client_id found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        if not client_secret:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="No client_secret found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        if not tenant_id:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="No tenant_id found. Check your .env file.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # OAuth2 authentication at KM Azure
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://api.businesscentral.dynamics.com/.default"}
        
        response = requests.post(url=url, data=payload)
        if (response.status_code >= 200) and (response.status_code < 300):
            return True
        else:
            return False
    except:
        return False