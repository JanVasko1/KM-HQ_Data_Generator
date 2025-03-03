# Import Libraries
import json
import os
from glob import glob

from customtkinter import StringVar, IntVar, BooleanVar

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

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

def Get_All_Templates_List(Settings: dict) -> list:
    file_path = Absolute_path(relative_path=f"Operational\\Template")
    Files = glob(pathname=os.path.join(file_path, "*"))
    Files_Templates = [x.replace(file_path, "") for x in Files]
    Files_Templates = [x.replace("\\", "") for x in Files_Templates]
    Files_Templates = [x.replace(".json", "") for x in Files_Templates]
    Files_Templates = list(set(Files_Templates))
    Files_Templates.sort()
    Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Template", "Templates_List"], Information=Files_Templates)

    return Files_Templates

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
            # Update current Settings
            Value_change(my_dict=Settings, JSON_path=JSON_path, Information=Information)

            # Save to file
            with open(Absolute_path(relative_path=f"Libs\\Settings.json"), mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=Settings, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        elif File_Name == "Configuration":
            # Update current Configuration
            Value_change(my_dict=Configuration, JSON_path=JSON_path, Information=Information)

            # Save to file
            with open(Absolute_path(relative_path=f"Libs\\GUI\\Configuration.json"), mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=Configuration, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        else:
            pass
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Not possible to update {Information} into Field: {JSON_path} of {File_Name}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Import_Data(Settings: dict, Configuration: dict, import_file_path: str, Import_Type: str,  JSON_path: list, Method: str) -> None:
    Can_Import = True
    # Check if file is json
    File_Name = import_file_path[0]
    File_Name_list = File_Name.split(".")

    if File_Name_list[1] == "json":
        pass
    else:
        Can_Import = False
        Elements.Get_MessageBox(Configuration=Configuration, title=f"Imported file is not .json you have to import only .json.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    # Check if file contain Supported Type
    if Can_Import == True:
        with open(file=File_Name, mode="r") as json_file:
            Import_file = json.load(json_file)
        json_file.close()
        
        if Import_file["Type"] == Import_Type:
            pass
        else:
            Can_Import = False
            Elements.Get_MessageBox(Configuration=Configuration, title=f"You try to import not supported file. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        pass

    # Take content and place it to file and change settings
    if Can_Import == True:
        if Method == "Overwrite":
            Upload_updated_data = Import_file["Data"]
        elif Method == "Add":
            Import_New_Data = Import_file["Data"]
            Current_Saved_Data = Defaults_Lists.Load_Settings_Part(my_dict=Settings, JSON_path=JSON_path)
            
            if type(Current_Saved_Data) is dict:
                # Change Keys for imported Dictionary --> because for or operand for same key would be deleted
                Current_Saved_Data_len = len(Current_Saved_Data)
                Import_New_Data = Dict_Main_Key_Change(Dictionary=Import_New_Data, counter=Current_Saved_Data_len)

                Concatenate_dict = Import_New_Data | Current_Saved_Data
                Upload_dict_len = len(Concatenate_dict)

                # Check each value of key for duplicate values
                Upload_updated_data = {}
                for key in range(0, Upload_dict_len):
                    Found = False
                    Base_Dict = Concatenate_dict[f"{key}"]
                    for sub_key in range(key + 1, Upload_dict_len):
                        if Base_Dict == Concatenate_dict[f"{sub_key}"]:
                            Found = True
                        else:
                            pass
                    if Found == False:
                        Dict_with_index = {
                            f"{key}": Base_Dict
                        }
                        Upload_updated_data.update(Dict_with_index)
                    else:
                        pass
                Upload_updated_data = Dict_Main_Key_Change(Dictionary=Upload_updated_data, counter=0)

            elif type(Current_Saved_Data) is list:
                # Put together
                Upload_updated_data = Import_New_Data + Current_Saved_Data
                Upload_updated_data = list(set(Upload_updated_data))
                Upload_updated_data.sort()
            else:
                pass

        Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=JSON_path, Information=Upload_updated_data)

    else:
        pass

# --------------------------------------------- PyInstaller --------------------------------------------- #
def Absolute_path(relative_path: str) -> str:
    try:
        base_path = os.path.abspath(".")
        Absolute_path_str = os.path.join(base_path, relative_path)
    except:
        Absolute_path_str = relative_path
    return Absolute_path_str
