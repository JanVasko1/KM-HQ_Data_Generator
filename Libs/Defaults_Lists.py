# Import Libraries
import pickle
import json
import random
from datetime import datetime, timedelta
from holidays import country_holidays

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

def Load_Documents() -> dict:
    File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Documents.json"), mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Load_Template(NUS_Version: str, Template: str) -> dict:
    File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Process\\_File_Templates\\{NUS_Version}\\{Template}.json"), mode="r", encoding="UTF-8", errors="ignore")
    Template = json.load(fp=File)
    File.close()
    return Template

# --------------------------------------------- OAuth2 --------------------------------------------- #
def Load_Azure_Auth() -> list[str, str, str]:
    with open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Authorization.pkl"), mode="rb") as Authorization:
        Aut_Data = pickle.load(Authorization)
    Display_name = Aut_Data["Display_name"]
    client_id = Aut_Data["client_id"]
    client_secret = Aut_Data["client_secret"]
    tenant_id = Aut_Data["tenant_id"]
    return Display_name, client_id, client_secret, tenant_id

def Save_set_key_Auth(Key: str, Value: str) -> None:
    with open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Authorization.pkl"), mode="rb") as Authorization:
        Auth_Data = pickle.load(Authorization)

    Auth_Data[Key] = Value

    with open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Authorization.pkl"), mode="wb") as Authorization:
        pickle.dump(obj=Auth_Data, file=Authorization)

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

# --------------------------------------------- Other Defaults --------------------------------------------- #
def Date_str_to_Week_str(Date_str: str, Format: str) -> str:
    Date_dt = datetime.strptime(Date_str, Format)
    Week = Date_dt.isocalendar()[1]
    Year = Date_dt.isocalendar()[0]
    Year_Week_str = f"{Year}-{Week}"
    return Year_Week_str

def Date_Random_from_CurrentDay_plus_Interval(From_int: int, To_int: int, Format: str) -> str:
    German_Holidays = country_holidays("GE")
    Today = datetime.now()
    Start_Date_dt = Today + timedelta(days=From_int)
    End_Date_dt = Today + timedelta(days=To_int)

    date_list = []
    current_date_dt = Start_Date_dt
    while current_date_dt <= End_Date_dt:
        current_date = current_date_dt.strftime(Format)
        
        # Check if working Day / non-working Day
        Weekday_num = current_date_dt.isoweekday()

        # Check Holidays
        Holiday_day = German_Holidays.get(key=current_date)
        if (Holiday_day == True) or (Weekday_num==6) or (Weekday_num==7):
            # Enlarge interval because of non-working Day / holiday found
            End_Date_dt += timedelta(days=1)
            current_date_dt += timedelta(days=1)
        else:
            date_list.append(current_date)
            current_date_dt += timedelta(days=1)
            

    Date_Selected = random.choice(date_list)
    return Date_Selected

def DateString_minus_Number_Day(Date_str: str, No_Days: int, Format: str) -> str:
    Date_dt = datetime.strptime(Date_str, Format)
    New_Date_dt = Date_dt + timedelta(days=No_Days)
    New_Date = New_Date_dt.strftime(Format)
    return New_Date

