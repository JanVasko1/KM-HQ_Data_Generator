# Import Libraries
from dotenv import load_dotenv
import json
import os

import Libs.Data_Functions as Data_Functions

# --------------------------------------------- Load defaults --------------------------------------------- #
def Load_Application() -> dict:
    File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\App\\Application.json"), mode="r", encoding="UTF-8", errors="ignore")
    Application = json.load(fp=File)
    File.close()
    return Application

def Load_Settings() -> dict:
    File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
    Settings = json.load(fp=File)
    File.close()
    return Settings

def Load_Settings_Part(my_dict: dict, JSON_path: list) -> str|int|float|list|dict:
    for key in JSON_path[:]:
        my_dict = my_dict.setdefault(key, {})
    return my_dict

def Load_Configuration() -> dict:
    File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Configuration.json"), mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Load_Figures(Theme:str) -> dict:
    File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Figure_settings_{Theme}.json"), mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Busy_Status_List() -> list[str]:
    Busy_Statuses = ["Free", "Tentative", "Busy", "Out of Office", "Working elsewhere"]
    return Busy_Statuses

def Exchange_Busy_Status_List() -> list[str]:
    Busy_Statuses = ["free", "tentative", "busy", "oof", "workingElsewhere", "unknown"]
    return Busy_Statuses

def Busy_Status_Priorities_List() -> list[str]:
    # Smaller Index = Higher priority
    Busy_Statuses_Priorities = ["Busy", "Working elsewhere", "Tentative", "Free", "Out of Office"]
    return Busy_Statuses_Priorities

def Load_Azure_env() -> list[str, str, str]:
    load_dotenv(dotenv_path=Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Authorization.env"))
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    tenant_id = os.getenv("tenant_id")
    return client_id, client_secret, tenant_id

# --------------------------------------------- List / Dict Operations --------------------------------------------- #
def List_from_Dict(Dictionary: dict, Key_Argument: str) -> list:
    Return_List = []
    for key, value in Dictionary.items():
        Return_List.append(value[f"{Key_Argument}"])
    Return_List.sort()
    return Return_List

def List_missing_values(Source_list, Compare_list):
    set_source = set(Source_list)
    set_compare = set(Compare_list)
    missing_values = set_compare - set_source
    return list(missing_values)

def Dict_Main_Key_Change(Dictionary: dict, counter: int) -> dict:
    new_dict = {}
    for key, value in Dictionary.items():
        new_key = f"{counter}"
        new_dict[new_key] = value
        counter += 1
    return new_dict
