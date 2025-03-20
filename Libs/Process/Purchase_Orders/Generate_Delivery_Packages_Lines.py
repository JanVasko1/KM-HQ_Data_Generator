# Import Libraries
import random
from pandas import DataFrame, Series

import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

from customtkinter import CTk, CTkFrame, StringVar

def Generate_Delivery_Packages_Lines(Settings: dict, Configuration: dict, window: CTk, PO_Deliveries: dict, PO_Delivery_Number_list: list, Delivery_Lines_df: DataFrame, Package_Header_df: DataFrame, Items_UoM_df: DataFrame, UoM_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Package_Lines_df_Columns = ["Delivery_No", "package_id", "package_itemnumber", "package_unit", "package_quantity", "package_plant"]
    Package_Lines_df = DataFrame(columns=Package_Lines_df_Columns)

    Pack_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Method"]
    Pack_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Pack_Fixed_Plant_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Plant_List"])
    Pack_Plant_list = []

    # --------------------------------------------- Item Assignment to Packages --------------------------------------------- #
    if Can_Continue == True:
        for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
            # Defaults
            Items_Qty_Distribution_list = []

            # Filter Dataframes for single Delivery
            mask_Delivery = Delivery_Lines_df["Delivery_No"] == Delivery_Number
            Delivery_Lines_df_Filtered = Delivery_Lines_df[mask_Delivery]
            Total_Items_Qty = int(Delivery_Lines_df_Filtered["quantity"].sum())

            mask_Delivery = Package_Header_df["Delivery_No"] == Delivery_Number
            Package_Header_df_Filtered = Package_Header_df[mask_Delivery]
            Package_list = Package_Header_df_Filtered["package_id"].to_list()
            Delivery_Package_Count = len(Package_list)

            # Define Qty of Item per Package
            Average = Total_Items_Qty // Delivery_Package_Count

            for Package_index, Package_Number in enumerate(Package_list):
                # First 
                if Package_index + 1 < Delivery_Package_Count:
                    Items_Qty_Distribution_list.append(Average)
                    Total_Items_Qty = Total_Items_Qty - Average
                elif Package_index + 1 == Delivery_Package_Count:
                    Items_Qty_Distribution_list.append(Total_Items_Qty)
                else:
                    pass

            # Add lines to Package_Lines_df from Delivery_Lines_df_Filtered
            for Distribution_index, Distribution_count in enumerate(Items_Qty_Distribution_list):
                Package_Number = Package_list[Distribution_index]
                Delete_Lines_index_list  = []
                for row in Delivery_Lines_df_Filtered.iterrows():
                    row_index = row[0]
                    row_Series = Series(row[1])
                    Item = row_Series["supplier_aid"]
                    Item_UoM = row_Series["order_unit"]
                    Item_Qty = row_Series["quantity"]

                    if Item_Qty < Distribution_count:
                        Package_Lines_Value = [Delivery_Number, Package_Number, Item, Item_UoM, Item_Qty, ""]
                        Delivery_Lines_df_Filtered.at[row_index, "quantity"] = 0
                        Distribution_count = Distribution_count - Item_Qty
                        Delete_Lines_index_list.append(row_index)
                    elif Item_Qty > Distribution_count:
                        Package_Lines_Value = [Delivery_Number, Package_Number, Item, Item_UoM, Distribution_count, ""]
                        Delivery_Lines_df_Filtered.at[row_index, "quantity"] = int(Item_Qty - Distribution_count)
                        Distribution_count = 0
                    elif Item_Qty == Distribution_count:
                        Package_Lines_Value = [Delivery_Number, Package_Number, Item, Item_UoM, Item_Qty, ""]
                        Delivery_Lines_df_Filtered.at[row_index, "quantity"] = 0
                        Distribution_count = 0
                        Delete_Lines_index_list.append(row_index)
                    else:
                        pass

                    # Add Line to Package_Lines_df
                    Package_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_End(Insert_DataFrame=Package_Lines_df, New_Row=Package_Lines_Value)

                    # Check residual value for package
                    if Distribution_count > 0:
                        pass
                    else:
                        # Delete Delivery_Lines_dff_Filtered --> fully assigned
                        if len(Delete_Lines_index_list) > 0:
                            Delivery_Lines_df_Filtered.drop(index=Delete_Lines_index_list, inplace=True, axis=0)
                        else:
                            pass
                        break
    else:
        pass

    # --------------------------------------------- Plant --------------------------------------------- #
    if Can_Continue == True:
        if Pack_Plant_Method == "Fixed":
            for Delivery in enumerate(PO_Delivery_Number_list):
                Pack_Plant_list.append(Pack_Fixed_Plant)
        elif Pack_Plant_Method == "Random":
            for Delivery in enumerate(PO_Delivery_Number_list):
                Pack_Plant = random.choice(seq=Pack_Fixed_Plant_List)
                Pack_Plant_list.append(Pack_Plant)
        elif Pack_Plant_Method == "Empty":
            for Delivery in enumerate(PO_Delivery_Number_list):
                Pack_Plant_list.append("")
        elif Pack_Plant_Method == "Prompt":
            def Select_PO_Pack_Plant(Frame_Body: CTkFrame, Lines_No: int):
                Plant_list = []
                for i in range(0, Lines_No + 1):
                    if i == 0:
                        i = ""
                    elif i == 1:
                        continue
                    else:
                        pass
                    
                    Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkoptionmenu"]
                    try:
                        Value_Plant = Value_CTkEntry.get()
                    except:
                        Value_Plant = "1000"
                    Plant_list.append(Value_Plant)

                Plant_list_joined = ";".join(Plant_list)
                PO_Pack_Plant_Variable.set(value=Plant_list_joined)
                PO_Pack_Plant_Window.destroy()
            
            # TopUp Window
            PO_Pack_Plant_Window_geometry = (520, 500)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Pack_Plant_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Pack_Plant_Window_geometry[1] //2
            PO_Pack_Plant_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Delivery Plant for selected Deliveries.", max_width=PO_Pack_Plant_Window_geometry[0], max_height=PO_Pack_Plant_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=False)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_Pack_Plant_Window, Name="Select Delivery Plant for selected Deliveries.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Plant for each Delivery..", GUI_Level_ID=3)
            Frame_Body = Frame_Main.children["!ctkframe2"]

            # Vendor_Service_ID
            Lines_No = len(PO_Delivery_Number_list)
            for Delivery_index, Delivery in enumerate(PO_Delivery_Number_list):
                # Fields
                Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Delivery}", Field_Type="Input_OptionMenu") 
                Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Pack_Fixed_Plant_List, command=None, GUI_Level_ID=3)

            # Dynamic Content height
            content_row_count = len(Frame_Body.winfo_children())
            content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
            if content_height > PO_Pack_Plant_Window_geometry[1]:
                content_height = PO_Pack_Plant_Window_geometry[1]
            Frame_Main.configure(bg_color = "#000001", height=content_height)

            # Buttons
            PO_Pack_Plant_Variable = StringVar(master=PO_Pack_Plant_Window, value="", name="PO_Pack_Plant_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_Pack_Plant(Frame_Body=Frame_Body, Lines_No=Lines_No))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Plant selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_Pack_Plant_Variable)
            Pack_Plant_list = PO_Pack_Plant_Variable.get().split(";")
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Plants Method selected: {Pack_Plant_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

    # Apply to Package_Lines_df
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        Current_plant = Pack_Plant_list[Delivery_Index]
        Plant_conditions = [(Package_Lines_df["Delivery_No"] == Delivery_Number)]
        Package_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Package_Lines_df, conditions=Plant_conditions, Set_Column="package_plant", Set_Value=Current_plant)

    else:
        pass

    # --------------------------------------------- Totals for Package Header --------------------------------------------- #
    # Prepare data
    Package_Lines_df["order_unit_Help"] = Package_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit_Help", Compare_Column_df1=["package_unit"], Compare_Column_df2=["International_Standard_Code"], Search_df=UoM_df, Search_Column="Code"), axis=1)
    Package_Lines_df["Item_Weight_Help"] = Package_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Item_Weight_Help", Compare_Column_df1=["package_itemnumber", "order_unit_Help"], Compare_Column_df2=["Item_No", "Code"], Search_df=Items_UoM_df, Search_Column="Weight"), axis=1)
    Package_Lines_df["Item_Volume_Help"] = Package_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Item_Volume_Help", Compare_Column_df1=["package_itemnumber", "order_unit_Help"], Compare_Column_df2=["Item_No", "Code"], Search_df=Items_UoM_df, Search_Column="Cubage"), axis=1)

    Package_Lines_df["Package_Line_Total_Weight"] =  Package_Lines_df["package_quantity"] * Package_Lines_df["Item_Weight_Help"]
    Package_Lines_df["Package_Line_Total_Volume"] =  Package_Lines_df["package_quantity"] * Package_Lines_df["Item_Volume_Help"]

    Package_Lines_df.drop(labels=["order_unit_Help", "Item_Weight_Help", "Item_Volume_Help"], inplace=True, axis=1)
    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # Loop of Each Delivery Separate
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        mask_Delivery = Package_Lines_df["Delivery_No"] == Delivery_Number
        Delivery_Filtered_df = Package_Lines_df[mask_Delivery]

        Package_list = Delivery_Filtered_df["package_id"].to_list()
        Package_list = list(set(Package_list))
        Package_list.sort()
        for Package_Index, Package_Number in enumerate(Package_list):
            mask_Package = Delivery_Filtered_df["package_id"] == Package_Number
            Delivery_Package_Filtered_df = Delivery_Filtered_df[mask_Package]

            # Update Measurements for whole Package
            package_total_weight = Delivery_Package_Filtered_df["Package_Line_Total_Weight"].sum()
            package_total_volume = Delivery_Package_Filtered_df["Package_Line_Total_Volume"].sum()

            PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["packages_info"][Package_Index]["package_total_weight"] = package_total_weight
            PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["packages_info"][Package_Index]["package_total_volume"] = package_total_volume

            # Prepare Json for each line of DataFrame
            PO_Package_Items = []
            for row_Del_Pack in Delivery_Package_Filtered_df.iterrows():
                row_Del_Pack_Series = Series(row_Del_Pack[1])
                Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Package_Item")

                # Assign Values
                Current_line_json["package_itemnumber"] = row_Del_Pack_Series["package_itemnumber"]
                Current_line_json["package_unit"] = row_Del_Pack_Series["package_unit"]
                Current_line_json["package_quantity"] = row_Del_Pack_Series["package_quantity"]
                Current_line_json["package_plant"] = row_Del_Pack_Series["package_plant"]

                PO_Package_Items.append(Current_line_json)
                del Current_line_json

            # Add Lines to proper Delivery Header
            PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["packages_info"][Package_Index]["package_items"] = PO_Package_Items

    return PO_Deliveries, Delivery_Lines_df, Package_Lines_df