# Import Libraries
import os
import json
from pandas import DataFrame, to_datetime
from dotenv import load_dotenv

from customtkinter import StringVar, IntVar, BooleanVar, get_appearance_mode
from CTkMessagebox import CTkMessagebox

# --------------------------------------------- Load defaults --------------------------------------------- #
def Load_Settings() -> dict:
    File = open(file=Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
    Settings = json.load(fp=File)
    File.close()
    return Settings

def Load_Configuration() -> dict:
    File = open(file=Absolute_path(relative_path=f"Libs\\GUI\\Configuration.json"), mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Load_Environments() -> list:
    Environment_list = ["QA", "FIX", "Sandbox"]
    return Environment_list

def Load_NOC() -> list:
    NOC_list = ["Core", "BBG", "BBL", "BCZ", "BGR", "BGE", "BKZ", "BHN", "BHR", "BiH", "BPL", "BR", "BRO", "BRS", "BSK", "BSL", "BUR", "BDK", "BSW", "BNO", "BFI", "BTR"]
    return NOC_list

# --------------------------------------------- Load defaults --------------------------------------------- #
def Load_Exchange_env() -> list[str, str, str]:
    load_dotenv(dotenv_path=Absolute_path(relative_path=f"Libs\\Azure\\Authorization.env"))
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    tenant_id = os.getenv("tenant_id")
    return client_id, client_secret, tenant_id

# --------------------------------------------- Sorting Operations --------------------------------------------- #
def Dataframe_sort(Sort_Dataframe: DataFrame, Columns_list: list, Accenting_list: list) -> None:
    # Sort Dataframe and reindex 
    Sort_Dataframe.sort_values(by=Columns_list, ascending=Accenting_list, axis=0, inplace = True)
    Sort_Dataframe.reset_index(inplace=True)
    Sort_Dataframe.drop(labels=["index"], inplace=True, axis=1)
    return Sort_Dataframe

# --------------------------------------------- List Operations --------------------------------------------- #
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

# --------------------------------------------- Global Settings update --------------------------------------------- #
def Save_Value(Settings: dict|None, Configuration: dict|None, Variable: StringVar|IntVar|BooleanVar|None, File_Name: str, JSON_path: list, Information: bool|int|str|list|dict) -> None:
    def Value_change(my_dict: dict, JSON_path: list, Information: bool|int|str|list|dict) -> None:
        for key in JSON_path[:-1]:
            my_dict = my_dict.setdefault(key, {})
        my_dict[JSON_path[-1]] = Information

    # Must be here as local function because 2 operation needs to be executed 
    if Variable is None:
        pass
    elif type(Variable) is None:
        pass
    elif type(Variable) is BooleanVar:
        Information = Information.get()
    else:
        Variable.set(value=Information)

    # Globals update with every change of setup
    try:
        if File_Name == "Settings":
            Value_change(my_dict=Settings, JSON_path=JSON_path, Information=Information)

            # Save to file
            with open(Absolute_path(relative_path=f"Libs\\Settings.json"), mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=Settings, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        elif File_Name == "Configuration":
            Value_change(my_dict=Configuration, JSON_path=JSON_path, Information=Information)

            # Save to file
            with open(Absolute_path(relative_path=f"Libs\\GUI\\Configuration.json"), mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=Configuration, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        else:
            pass
    except Exception as Error:
        CTkMessagebox(title="Error", message=f"Not possible to update {Information} into Field: {JSON_path} of {File_Name}", icon="cancel", fade_in_duration=1)

# --------------------------------------------- Pandas --------------------------------------------- #
def PD_Column_to_DateTime(PD_DataFrame: DataFrame, Column: str, Covert_Format: str) -> DataFrame:
    PD_DataFrame[Column] = to_datetime(arg=PD_DataFrame[Column], format=Covert_Format)
    return PD_DataFrame

def Dataframe_sort(Sort_Dataframe: DataFrame, Columns_list: list, Accenting_list: list) -> None:
    # Sort Dataframe and reindex 
    Sort_Dataframe.sort_values(by=Columns_list, ascending=Accenting_list, axis=0, inplace = True)
    Sort_Dataframe.reset_index(inplace=True)
    Sort_Dataframe.drop(labels=["index"], inplace=True, axis=1)
    return Sort_Dataframe

# --------------------------------------------- PyInstaller --------------------------------------------- #
def Absolute_path(relative_path: str) -> str:
    try:
        base_path = os.path.abspath(".")
        Absolute_path_str = os.path.join(base_path, relative_path)
    except:
        Absolute_path_str = relative_path
    return Absolute_path_str
