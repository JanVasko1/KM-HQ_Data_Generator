# Import Libraries
import random
from pandas import DataFrame, Series
from datetime import datetime

import Libs.GUI.Elements as Elements
import Libs.Pandas_Functions as Pandas_Functions
import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTk

def Generate_Delivery_Packages_Headers(Settings: dict, Configuration: dict, window: CTk, PO_Deliveries: dict, PO_Delivery_Number_list: list, Delivery_Lines_df: DataFrame, UoM_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    Package_Header_df_Columns = ["Delivery_No", "package_id", "exidv2", "package_weight_unit", "package_volume_unit"]
    Package_Header_df = DataFrame(columns=Package_Header_df_Columns)

    Pack_Number_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Method"]
    Pack_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Automatic_Options"]["Prefix"]
    Pack_Max_Records = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Automatic_Options"]["Max_Packages_Records"]
    Pack_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Fixed_Options"]["Fixed_Package_No"]

    Pack_Weight_UoM_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Weight"]["Method"]
    Pack_Weight_UoM_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Weight"]["Fixed_Options"]["Fixed_Weight_UoM"]
    Weight_UoM = ""

    Pack_Volume_UoM_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Volume"]["Method"]
    Pack_Volume_UoM_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Volume"]["Fixed_Options"]["Fixed_Volume_UoM"]
    Volume_UoM = ""

    EXIDV2_Assign_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Method"]
    EXIDV2_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Method"]
    EXIDV2_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Automatic_Options"]["Prefix"]
    EXIDV2_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Fixed_Options"]["Fixed_EXIDV2"]

    # --------------------------------------------- Package Count --------------------------------------------- #
    Packages_Count_List = []
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        mask_Delivery = Delivery_Lines_df["Delivery_No"] == Delivery_Number
        Delivery_Lines_df_Filtered = DataFrame(Delivery_Lines_df[mask_Delivery])
        Qty_sum = int(Delivery_Lines_df_Filtered["quantity"].sum())

        # Package Count 
        Packages_Count = random.randint(a=1, b=Qty_sum)
        if Packages_Count > Pack_Max_Records:
            Packages_Count = Pack_Max_Records
        else:
            pass

        # Assign Package Count to list
        Packages_Count_List.append(Packages_Count)

    # --------------------------------------------- Package Numbers --------------------------------------------- #
    Packages_Number_List = []
    if Can_Continue == True:
        if Pack_Number_Method == "Fixed":
            Total_Package_Count = len(Packages_Count_List)  # One Package per delivery -> len
            Packages_Count_List = []
            Package_Number = Pack_Fixed_Number
            for i in range(0, Total_Package_Count):
                Packages_Number_List.append(Package_Number)
                Packages_Count_List.append(1)
        elif Pack_Number_Method == "Automatic":
            Total_Package_Count = sum(Packages_Count_List)  # Packages according Count -> sum
            Today_dt = datetime.now()
            Today_str = Today_dt.strftime(Numbers_DateTime_format)
            for i in range(0, Total_Package_Count):
                Package_Number = f"{Pack_Prefix}{Today_str}{str(i)}"
                Packages_Number_List.append(Package_Number)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Package Number Method selected: {Pack_Number_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    # Package Lists based on Packages_Count_List
    Package_Distribution_list = []
    start = 0
    for size in Packages_Count_List:
        end = start + size
        Package_Distribution_list.append(Packages_Number_List[start:end])
        start = end

    # Add to Dataframe
    for Package_Chunk_index, Package_Chunk in enumerate(Package_Distribution_list):
        Delivery_No = PO_Delivery_Number_list[Package_Chunk_index]
        for Package_Number in Package_Chunk:
            Package_Header_Value = [Delivery_No, Package_Number, "", "", ""]
            Package_Header_df = Pandas_Functions.Dataframe_Insert_Row_at_End(Insert_DataFrame=Package_Header_df, New_Row=Package_Header_Value)

    # --------------------------------------------- EXIDV2 --------------------------------------------- #
    EXIDV2_Number_list = []
    if Can_Continue == True:
        if EXIDV2_Assign_Method == "Per Package":
            if EXIDV2_Numbers_Method == "Fixed":
                Package_Header_df["exidv2"] = EXIDV2_Fixed_Number
            elif EXIDV2_Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                for i in range(0, sum(Packages_Count_List)):
                    EXIDV2_Number = f"{EXIDV2_Automatic_Prefix}{Today_str}{str(i)}"
                    EXIDV2_Number_list.append(EXIDV2_Number)
                Package_Header_df["exidv2"] = EXIDV2_Number_list
            elif EXIDV2_Numbers_Method == "Empty":
                Package_Header_df["exidv2"] = ""
            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"EXIDV2 Number Method selected: {EXIDV2_Numbers_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                Can_Continue = False
                
        elif EXIDV2_Assign_Method == "Per Delivery":
            if EXIDV2_Numbers_Method == "Fixed":
                Package_Header_df["exidv2"] = EXIDV2_Fixed_Number
            elif EXIDV2_Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                Delivery_Package_rows_List = Package_Header_df["Delivery_No"].to_list()
                for index, Delivery_Number in enumerate(Delivery_Package_rows_List):
                    if index == 0:
                        EXIDV2_Number = f"{EXIDV2_Automatic_Prefix}{Today_str}{str(index)}"
                        EXIDV2_Number_list.append(EXIDV2_Number)
                    else:
                        if Delivery_Package_rows_List[index] == Delivery_Package_rows_List[index - 1]:
                            EXIDV2_Number_list.append(EXIDV2_Number)
                        else:
                            EXIDV2_Number = f"{EXIDV2_Automatic_Prefix}{Today_str}{str(index)}"
                            EXIDV2_Number_list.append(EXIDV2_Number)
                Package_Header_df["exidv2"] = EXIDV2_Number_list
            elif EXIDV2_Numbers_Method == "Empty":
                Package_Header_df["exidv2"] = ""
            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"EXIDV2 Number Method selected: {EXIDV2_Numbers_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                Can_Continue = False
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"EXIDV2 Assign Method selected: {EXIDV2_Assign_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Measurements --------------------------------------------- #
    # Weight UoM
    if Can_Continue == True:
        if Pack_Weight_UoM_Method == "Fixed":
            Weight_UoM = Pack_Weight_UoM_Fixed
        elif Pack_Weight_UoM_Method == "Random":
            Weight_UoM_List = UoM_df["International_Standard_Code"].to_list()
            Weight_UoM = random.choice(seq=Weight_UoM_List)
        elif Pack_Weight_UoM_Method == "Empty":
            Weight_UoM = ""
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Weight Method selected: {Pack_Weight_UoM_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass 
    Package_Header_df["package_weight_unit"] = Weight_UoM
     
    # Volume UoM  
    if Can_Continue == True:
        if Pack_Volume_UoM_Method == "Fixed":
            Volume_UoM = Pack_Volume_UoM_Fixed
        elif Pack_Volume_UoM_Method == "Random":
            Volume_UoM_List = UoM_df["International_Standard_Code"].to_list()
            Volume_UoM = random.choice(seq=Volume_UoM_List)
        elif Pack_Volume_UoM_Method == "Empty":
            Volume_UoM = ""
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Weight Method selected: {Pack_Weight_UoM_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass   
    Package_Header_df["package_volume_unit"] = Volume_UoM

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # Loop of Each Delivery Separate
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        mask_Delivery = Package_Header_df["Delivery_No"] == Delivery_Number
        Package_Header_df_Filtered = DataFrame(Package_Header_df[mask_Delivery])
        
        # Prepare Json for each line of DataFrame
        PO_Package_Lines = []
        for row in Package_Header_df_Filtered.iterrows():
            row_Series = Series(row[1])

            Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Package_Header")

            # Assign Values
            Current_line_json["package_id"] = row_Series["package_id"]
            Current_line_json["exidv2"] = row_Series["exidv2"]
            Current_line_json["package_weight_unit"] = row_Series["package_weight_unit"]
            Current_line_json["package_volume_unit"] = row_Series["package_volume_unit"]

            PO_Package_Lines.append(Current_line_json)
            del Current_line_json
        
        # Add Lines to proper Delivery Header
        PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["packages_info"] = PO_Package_Lines

    return PO_Deliveries, Package_Header_df, Weight_UoM, Volume_UoM

