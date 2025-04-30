# Import Libraries
import os
import json
from glob import glob
from shutil import rmtree, copy
from pandas import DataFrame
from fpdf import FPDF
from fastapi import HTTPException

import Libs.GUI.Elements as Elements

from customtkinter import CTk

# --------------------------------------------- Folders / Files --------------------------------------------- #
def Get_All_Files_Names(file_path: str) -> list:
    file_names = []
    for (dirpath, dirnames, filenames) in os.walk(file_path):
        for file in filenames:
            filename = str(file).split(".")[0]
            file_names.append(filename)
        break
    return file_names

def Create_Folder(Configuration: dict|None, window: CTk|None, file_path: str) -> None:
    # Create Folder
    try: 
        os.makedirs(f"{file_path}")
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Not possible to create folder int {file_path}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Copy_File(Configuration: dict|None, window: CTk|None, Source_Path: str, Destination_Path: str) -> None:
    try:
        copy(src=Source_Path, dst=Destination_Path)
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Not possible to copy file:\n From: {Source_Path}\n To: {Destination_Path} ", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Copy_All_File(Configuration: dict|None, window: CTk|None, Source_Path: str, Destination_Path: str, include_hidden: bool) -> None:
    files = glob(pathname=os.path.join(Source_Path, "*"), include_hidden=include_hidden)
    for source_file in files:
        dest_file = source_file.replace(Source_Path, Destination_Path)
        try:
            copy(src=source_file, dst=dest_file)
        except Exception as Error:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Not possible to copy file:\n From: {Source_Path}\n To: {Destination_Path} ", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

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
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    Destination_File = os.path.join(downloads_folder, os.path.basename(f"{File_Name}.{File_postfix}"))
    return Destination_File

# --------------------------------------------- Exporting to --------------------------------------------- #
def Export_NAV_Folders(Configuration: dict, window: CTk, NVR_FS_Connect_df: DataFrame, HQ_Communication_Setup_df: DataFrame, Buy_from_Vendor_No: str, File_Content: dict|FPDF, HQ_File_Type_Path: str, File_Name: str, File_suffix: str, GUI: bool=True) -> None:
    # NVR Connector
    Root_Path_NUS = str(NVR_FS_Connect_df.iloc[0]["Root_Path_NUS"])
    Root_Path_NUS = Root_Path_NUS.replace("\\\\", "")
    Root_Path_Suffix_NUS = str(NVR_FS_Connect_df.iloc[0]["Root_Path_Suffix_NUS"])

    # HQ Communication Filter
    HQ_mask = HQ_Communication_Setup_df["HQ_Vendor_No"] == Buy_from_Vendor_No
    HQ_Communication_Setup_df = DataFrame(HQ_Communication_Setup_df[HQ_mask])
    HQ_Path = str(HQ_Communication_Setup_df.iloc[0][HQ_File_Type_Path])

    if HQ_Path.endswith("\\"):
        pass
    else:
        HQ_Path = f"{HQ_Path}\\"

    # Export
    try:
        if File_suffix == "json":
            with open(rf"\\{Root_Path_NUS}{Root_Path_Suffix_NUS}\{HQ_Path}{File_Name}.{File_suffix}", "w") as outfile: 
                json.dump(File_Content, outfile)
        elif File_suffix == "pdf":
            File_Content.output(rf"\\{Root_Path_NUS}{Root_Path_Suffix_NUS}\{HQ_Path}{File_Name}.{File_suffix}")
    except:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Impossible to store data in FileServer.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail="Impossible to store data in FileServer.")

def Export_Download_Folders(Configuration: dict, window: CTk, File_Content: dict|FPDF, File_Name: str, File_suffix: str, GUI: bool=True) -> None:
    Export_Folder_Path = os.path.join(os.path.expanduser("~"), "Downloads")
    try:
        if File_suffix == "json":
            with open(f"{Export_Folder_Path}\\{File_Name}.{File_suffix}", "w") as outfile: 
                json.dump(File_Content, outfile)
        elif File_suffix == "pdf":
            File_Content.output(f"{Export_Folder_Path}\\{File_Name}.{File_suffix}")
    except:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Impossible to store data in Downloads folder.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail="Impossible to store data in Downloads folder.")