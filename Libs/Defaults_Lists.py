# Import Libraries
from pandas import DataFrame, to_datetime
from dotenv import load_dotenv, set_key
import json
import os
import pyautogui
from glob import glob
from shutil import rmtree, copy

from customtkinter import CTkButton, StringVar, IntVar, BooleanVar, get_appearance_mode
from CTkTable import CTkTable

import Libs.GUI.Elements as Elements

# --------------------------------------------- Load defaults --------------------------------------------- #
def Load_Application() -> dict:
    File = open(file=Absolute_path(relative_path=f"Libs\\App\\Application.json"), mode="r", encoding="UTF-8", errors="ignore")
    Application = json.load(fp=File)
    File.close()
    return Application

def Load_Settings() -> dict:
    File = open(file=Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
    Settings = json.load(fp=File)
    File.close()
    return Settings

def Load_Settings_Part(my_dict: dict, JSON_path: list) -> str|int|float|list|dict:
    for key in JSON_path[:]:
        my_dict = my_dict.setdefault(key, {})
    return my_dict

def Load_Configuration() -> dict:
    File = open(file=Absolute_path(relative_path=f"Libs\\GUI\\Configuration.json"), mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Save_set_key_env(Key: str, Value: str) -> None:
    set_key(dotenv_path=Absolute_path(relative_path=f"Libs\\Azure\\Authorization.env"), key_to_set=Key, value_to_set=Value)
    

def Load_Exchange_env() -> list[str, str, str]:
    load_dotenv(dotenv_path=Absolute_path(relative_path=f"Libs\\Azure\\Authorization.env"))
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
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Imported file is not .json you have to import only .json.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    # Check if file contain Supported Type
    if Can_Import == True:
        with open(file=File_Name, mode="r") as json_file:
            Import_file = json.load(json_file)
        json_file.close()
        
        if Import_file["Type"] == Import_Type:
            pass
        else:
            Can_Import = False
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"You try to import not supported file. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        pass

    # Take content and place it to file and change settings
    if Can_Import == True:
        if Method == "Overwrite":
            Upload_updated_data = Import_file["Data"]
        elif Method == "Add":
            Import_New_Data = Import_file["Data"]
            Current_Saved_Data = Load_Settings_Part(my_dict=Settings, JSON_path=JSON_path)
            
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


# --------------------------------------------- Folders / Files --------------------------------------------- #
def Create_Folder(Configuration: dict, file_path: str) -> None:
    # Create Folder
    try: 
        os.makedirs(f"{file_path}")
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Not possible to create folder int {file_path}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Copy_File(Configuration: dict, Source_Path: str, Destination_Path: str) -> None:
    try:
        copy(src=Source_Path, dst=Destination_Path)
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Not possible to copy file:\n From: {Source_Path}\n To: {Destination_Path}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Delete_Folder(file_path: str) -> None:
    # Create Folder
    try: 
        os.rmdir(path=f"{file_path}")
    except Exception as Error:
        print(Error)

def Delete_Folders(file_path: str) -> None:
    try:
        rmtree(file_path)
    except Exception as Error:
        print(Error)

def Delete_File(file_path: str) -> None:
    # Delete File
    try: 
        os.remove(path=f"{file_path}")
    except Exception as Error:
        print(Error)

def Delete_All_Files(file_path: str, include_hidden: bool) -> None:
    # Delete File
    try:
        files = glob(pathname=os.path.join(file_path, "*"), include_hidden=include_hidden)
        for file in files:
            os.remove(file)
    except Exception as Error:
        print(Error)

def Get_Downloads_File_Path(File_Name: str, File_postfix: str):
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    Destination_File = os.path.join(downloads_folder, os.path.basename(f"{File_Name}.{File_postfix}"))
    return Destination_File

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

# --------------------------------------------- CustomTkinter --------------------------------------------- #
def Dialog_Window_Request(Configuration: dict, title: str, text: str, Dialog_Type: str) -> str|None:
    # Password required
    dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type)
    Dialog_Input = dialog.get_input()
    return Dialog_Input

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

def Get_Current_Theme() -> str:
    Current_Theme = get_appearance_mode()
    return Current_Theme

def Count_coordinate_for_new_window(Clicked_on: CTkButton, New_Window_width: int) -> list:
    # Click_on coordinate
    Clicked_on_X = Clicked_on.winfo_pointerx() - Clicked_on.winfo_rootx()
    Clicked_on_Y = Clicked_on.winfo_pointery() - Clicked_on.winfo_rooty()

    Clicked_on_width = Clicked_on._current_width
    Clicked_on_X_middle = Clicked_on_width // 2
    Clicked_on_height = Clicked_on._current_height

    Clicked_On_X_difference = Clicked_on_X_middle - Clicked_on_X - (New_Window_width // 2)
    Clicked_on_Y_difference = Clicked_on_height - Clicked_on_Y

    # Window coordinate
    Window_X, Window_Y = pyautogui.position()

    # Top middle coordinate for new window
    return [Window_X + Clicked_On_X_difference, Window_Y + Clicked_on_Y_difference + 5]

def Disable_Enable_Fields(Enable_Elements_List: list, Disable_Elements_List: list) -> None:
    # Enable Fields
    for Enable_Element in Enable_Elements_List:
        Enable_Element.configure(state="normal")

    # Disable Fields
    for Disable_Element in Disable_Elements_List:
        Disable_Element.configure(state="disabled")

# --------------------------------------------- PyInstaller --------------------------------------------- #
def Absolute_path(relative_path: str) -> str:
    try:
        base_path = os.path.abspath(".")
        Absolute_path_str = os.path.join(base_path, relative_path)
    except:
        Absolute_path_str = relative_path
    return Absolute_path_str
