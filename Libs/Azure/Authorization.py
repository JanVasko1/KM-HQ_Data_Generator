# Import Libraries
import requests
from Libs.Azure.API_Error_Handler import APIError

try:
    # Front-End Library
    from customtkinter import CTk
    import Libs.GUI.Elements as Elements
except:
    pass

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Azure_OAuth(Configuration: dict|None, window: CTk|None, client_id: str, client_secret: str, tenant_id: str, GUI: bool=True) -> str:
    if not client_id:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="No client_id found. Check your Settings.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise APIError(message="No client_id found. Check your Navision.", status_code=500, charset="utf-8")
    if not client_secret:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="No client_secret found. Check your Settings.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise APIError(message="No client_secret found. Check your Navision.", status_code=500, charset="utf-8")
    if not tenant_id:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="No tenant_id found. Check your Settings.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise APIError(message="No tenant_id found. Check your Navision.", status_code=500, charset="utf-8")

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

def Azure_OAuth_Test(client_id: str, client_secret: str, tenant_id: str) -> str:
    try:
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