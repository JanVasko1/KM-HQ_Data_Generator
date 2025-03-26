# Import Libraries
import random
from datetime import datetime
from pandas import DataFrame, Series
from fastapi import HTTPException

import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, StringVar

def Generate_Delivery_Lines(Settings: dict, Configuration: dict|None, window: CTk|None, Purchase_Order: str, PO_Deliveries: list, Delivery_Count: int, PO_Delivery_Number_list: list, PO_Delivery_Date_list: list, Confirmed_Lines_df: DataFrame, PO_Confirmation_Number: str, HQ_Item_Transport_Register_df: DataFrame, Items_df: DataFrame, Items_Tracking_df: DataFrame, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    Delivery_Lines_df_Columns = ["Delivery_No", "line_item_id", "supplier_aid", "quantity", "order_unit", "delivery_start_date", "delivery_end_date", "order_id", "order_ref_line_item_id", "order_date", "supplier_order_id", "supplier_order_item_id", "serial_numbers"]
    Delivery_Lines_df = DataFrame(columns=Delivery_Lines_df_Columns)
    Delivery_Lines_Template_List = []

    DEL_Assignment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["Method"]
    DEL_FOCH_with_Main = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["FreeOfCharge_with_Main"]

    SN_Machines = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Generate"]["Machines"]
    SN_Tracked_Items = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Generate"]["Tracked"]
    SN_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Prefix"]
    SN_Middle_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Method"]
    SN_Middle_Manual = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Fixed"]

    # --------------------------------------------- Items Splitting  --------------------------------------------- #
    if DEL_Assignment_Method == "Full random":
        # Define Total Qty for Delivery
        To_Split_Qty = int(Confirmed_Lines_df["quantity"].sum())
        if DEL_FOCH_with_Main == True:
            # TODO --> Minus FOCH Qty from whole Sum_Qty --> as should be on the same Delivery as machine
            pass 
        else:
            pass
    elif DEL_Assignment_Method == "Lines random":
        # Define Total Qty for Delivery
        To_Split_Qty = len(Confirmed_Lines_df)
        if DEL_FOCH_with_Main == True:
            # TODO --> Minus FOCH lines count from whole Sum_Lines --> as should be on the same Delivery as machine
            pass 
        else:
            pass
    elif DEL_Assignment_Method == "Prompt":
        if GUI == True:
            # Define Total Qty for Delivery
            To_Split_Qty = len(Confirmed_Lines_df)
            if DEL_FOCH_with_Main == True:
                # TODO --> Minus FOCH lines count from whole Sum_Lines --> as should be on the same Delivery as machine
                pass 
            else:
                pass
        else:
            raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Delivery_Lines:Item_Splitting:DEL_Assignment_Method")
    else:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Random Method selected: {DEL_Assignment_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail=f"Delivery Random Method selected: {DEL_Assignment_Method} which is not supporter. Cancel File creation.")
        Can_Continue = False

    # Define Qty per Delivery
    if Can_Continue == True:
        Delivery_Qty_Split_List = []
        Remaining_Deliveries = Delivery_Count

        for i in range(1, Delivery_Count + 1):
            # Check Last Delivery
            if Remaining_Deliveries == 1:
                Delivery_Qty = To_Split_Qty
            elif Remaining_Deliveries == Delivery_Count:
                Delivery_Qty = random.randint(a=1, b=To_Split_Qty // 2)
            else:
                Delivery_Qty = random.randint(a=1, b=To_Split_Qty)

            # Remaining After Selection
            Remaining_Deliveries = Delivery_Count - i
            To_Split_Qty = To_Split_Qty - Delivery_Qty
            if To_Split_Qty >= Remaining_Deliveries:
                pass
            else:
                Difference = Remaining_Deliveries - To_Split_Qty
                To_Split_Qty = To_Split_Qty + Difference
                Delivery_Qty = Delivery_Qty - Difference
                
            Delivery_Qty_Split_List.append(Delivery_Qty)

        # Split According to Method and Delivery Qty
        if DEL_Assignment_Method == "Full random":
            Confirmed_Lines_df_copy = Confirmed_Lines_df.copy() # I Should not delete lines in original Confirmed_Lines_df (as used in Invoice then)
            for Distribute_Qty_index, Distribute_Qty in enumerate(Delivery_Qty_Split_List):
                Delivery_Number = PO_Delivery_Number_list[Distribute_Qty_index]
                Confirmed_order_date = HQ_Item_Transport_Register_df.iloc[0]["Order_Date"]

                # Assign Qty from Confirmed_Lines_df for Delivery
                while Distribute_Qty > 0:
                    Delete_Lines_index_list  = []
                    Compare_Qty = 0

                    # Pick Confirmation line
                    Confirmed_Lines_df_index_list = Confirmed_Lines_df_copy.index.to_list()
                    Picked_index = random.choice(seq=Confirmed_Lines_df_index_list)
                    
                    # Read Confirmation line information
                    order_ref_line_item_id = Confirmed_Lines_df_copy.iloc[Picked_index]["line_item_id"]
                    order_ref_line_item_id = f"{order_ref_line_item_id :06d}"

                    supplier_aid = Confirmed_Lines_df_copy.iloc[Picked_index]["supplier_aid"]
                    Item_Qty = Confirmed_Lines_df_copy.iloc[Picked_index]["quantity"]
                    order_unit = Confirmed_Lines_df_copy.iloc[Picked_index]["order_unit"]
                    supplier_order_item_id = Confirmed_Lines_df_copy.iloc[Picked_index]["supplier_order_item_id"]

                    Picked_Qty = random.randint(a=1, b=Item_Qty)

                    # Check state between Distribute_Qty and Picked_Qty
                    if Picked_Qty > Distribute_Qty:
                        Compare_Qty = Distribute_Qty
                    elif Picked_Qty < Distribute_Qty:
                        Compare_Qty = Picked_Qty
                    elif Picked_Qty == Distribute_Qty:
                        Compare_Qty = Picked_Qty
                    else:
                        pass

                    # Analyze Confirmation lines against Compare Qty
                    if Item_Qty < Compare_Qty:
                        Delivery_Line_Values = [Delivery_Number, "", supplier_aid, Item_Qty, order_unit, "", "", Purchase_Order, order_ref_line_item_id, Confirmed_order_date, PO_Confirmation_Number, supplier_order_item_id, ""]
                        Confirmed_Lines_df_copy.at[Picked_index, "quantity"] = 0
                        Distribute_Qty = Distribute_Qty - Item_Qty
                        Delete_Lines_index_list.append(Picked_index)
                    elif Item_Qty > Compare_Qty:
                        Delivery_Line_Values = [Delivery_Number, "", supplier_aid, Compare_Qty, order_unit, "", "", Purchase_Order, order_ref_line_item_id, Confirmed_order_date, PO_Confirmation_Number, supplier_order_item_id, ""]
                        Confirmed_Lines_df_copy.at[Picked_index, "quantity"] = int(Item_Qty - Compare_Qty)
                        Distribute_Qty = Distribute_Qty - Compare_Qty
                    elif Item_Qty == Compare_Qty:
                        Delivery_Line_Values = [Delivery_Number, "", supplier_aid, Item_Qty, order_unit, "", "", Purchase_Order, order_ref_line_item_id, Confirmed_order_date, PO_Confirmation_Number, supplier_order_item_id, ""]
                        Confirmed_Lines_df_copy.at[Picked_index, "quantity"] = 0
                        Distribute_Qty = Distribute_Qty - Compare_Qty
                        Delete_Lines_index_list.append(Picked_index)
                    else:
                        pass

                    # Add Line to Package_Lines_df
                    Delivery_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_End(Insert_DataFrame=Delivery_Lines_df, New_Row=Delivery_Line_Values)

                    # Delete Delivery_Lines_df_Filtered --> fully assigned
                    if len(Delete_Lines_index_list) > 0:
                        Confirmed_Lines_df_copy.drop(index=Delete_Lines_index_list, inplace=True, axis=0)
                        Confirmed_Lines_df_copy.reset_index(drop=True, inplace=True)
                    else:
                        pass

                    # Check residual value for package
                    if Distribute_Qty > 0:
                        pass
                    else:
                        break

            # Put same lines with different Qty together
            Delivery_Lines_df = Delivery_Lines_df.groupby(Delivery_Lines_df.columns.difference(["quantity"]).tolist(), as_index=False)["quantity"].sum()

            # Sort Dataframe
            Delivery_Lines_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Delivery_Lines_df, Columns_list=["Delivery_No", "order_ref_line_item_id", "supplier_order_item_id"], Accenting_list=[True, True, True])
            
            # Update Delivery Dates --> cannot be updated in main loop
            for Delivery_index, Delivery_Number in enumerate(PO_Delivery_Number_list):
                Delivery_Date = PO_Delivery_Date_list[Delivery_index]
                Delivery_No_condition = [(Delivery_Lines_df["Delivery_No"] == Delivery_Number)]
                Delivery_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Delivery_Lines_df, conditions=Delivery_No_condition, Set_Column="delivery_start_date", Set_Value=Delivery_Date)
                Delivery_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Delivery_Lines_df, conditions=Delivery_No_condition, Set_Column="delivery_end_date", Set_Value=Delivery_Date)   

        elif DEL_Assignment_Method == "Lines random":
            Confirmed_Lines_df_index_list = Confirmed_Lines_df.index.to_list()
            Confirmed_order_date = HQ_Item_Transport_Register_df.iloc[0]["Order_Date"]
            for Delivery_Lines_index, Delivery_Lines_Count in enumerate(Delivery_Qty_Split_List):
                # Defaults
                Current_Delivery_No = PO_Delivery_Number_list[Delivery_Lines_index]
                Current_Delivery_Date = PO_Delivery_Date_list[Delivery_Lines_index]

                # Get Line from Confirmed_Lines_df
                Selected_Line_indexes = random.sample(population=Confirmed_Lines_df_index_list, k=Delivery_Lines_Count)
                Selected_Line_indexes.sort()

                for x in Selected_Line_indexes:
                    Confirmed_Lines_df_index_list.remove(x)

                # Get Lines from Confirmed_Lines_df and put to Delivery_Lines_df
                for Support_Index, Confirmed_Lines_df_index in enumerate(Selected_Line_indexes):
                    Delivery_Line_Values = []
                    order_ref_line_item_id = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["line_item_id"]
                    order_ref_line_item_id = f"{order_ref_line_item_id :06d}"

                    supplier_aid = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["supplier_aid"]
                    quantity = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["quantity"]
                    order_unit = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["order_unit"]
                    supplier_order_item_id = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["supplier_order_item_id"]

                    # Add to Lines_df
                    Delivery_Line_Values = [Current_Delivery_No, "", supplier_aid, quantity, order_unit, Current_Delivery_Date, Current_Delivery_Date, Purchase_Order, order_ref_line_item_id, Confirmed_order_date, PO_Confirmation_Number, supplier_order_item_id, ""]
                    Delivery_Lines_df.loc[len(Delivery_Lines_df)] = Delivery_Line_Values

        elif DEL_Assignment_Method == "Prompt":
            if GUI == True:
                Confirmed_order_date = HQ_Item_Transport_Register_df.iloc[0]["Order_Date"]
                def Assing_Item_Line_to_Delivery(Frame_Body: CTkFrame, Lines_No: int, Confirmed_Lines_df: DataFrame):
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                            df_i = 0
                        elif i == 1:
                            continue
                        else:
                            df_i = i - 1
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe4"].children["!ctkoptionmenu"]
                        try:
                            Value_Delivery = Value_CTkEntry.get()
                        except:
                            Value_Delivery = ""

                        order_ref_line_item_id = Confirmed_Lines_df.iloc[df_i]["line_item_id"]
                        order_ref_line_item_id = f"{order_ref_line_item_id :06d}"

                        supplier_aid = Confirmed_Lines_df.iloc[df_i]["supplier_aid"]
                        quantity = Confirmed_Lines_df.iloc[df_i]["quantity"]
                        order_unit = Confirmed_Lines_df.iloc[df_i]["order_unit"]
                        supplier_order_item_id = Confirmed_Lines_df.iloc[df_i]["supplier_order_item_id"]

                        # Add to Lines_df
                        Delivery_Line_Values = [Value_Delivery, "", supplier_aid, quantity, order_unit, "", "", Purchase_Order, order_ref_line_item_id, Confirmed_order_date, PO_Confirmation_Number, supplier_order_item_id, ""]
                        Delivery_Lines_df.loc[len(Delivery_Lines_df)] = Delivery_Line_Values

                    PO_Item_Assing_Variable.set(value="Selected")
                    PO_Item_Assing_Window.destroy()

                # TopUp Window
                PO_Item_Assing_Window_geometry = (1020, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Item_Assing_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Item_Assing_Window_geometry[1] //2
                PO_Item_Assing_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Delivery for Item line.", max_width=PO_Item_Assing_Window_geometry[0], max_height=PO_Item_Assing_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_Item_Assing_Window, Name="Select Delivery for Item line.", Additional_Text="", Widget_size="Item_Del_Assign", Widget_Label_Tooltip="To make Item assignment to delivery.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Delivery Assignment
                Lines_No = Confirmed_Lines_df.shape[0]
                for row in Confirmed_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Line_Item_No = row_Series["supplier_aid"]
                    Line_Item_Desc = row_Series["description_long"]
                    Line_Qty = row_Series["quantity"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Prompt_Delivery_Assignment(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Line_Item_No=Line_Item_No, Line_Item_Desc=Line_Item_Desc, Line_Qty=Line_Qty, PO_Delivery_Number_list=PO_Delivery_Number_list, GUI_Level_ID=3) 
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_Item_Assing_Window_geometry[1]:
                    content_height = PO_Item_Assing_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_Item_Assing_Variable = StringVar(master=PO_Item_Assing_Window, value="", name="PO_Item_Assing_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Assing_Item_Line_to_Delivery(Frame_Body=Frame_Body, Lines_No=Lines_No, Confirmed_Lines_df=Confirmed_Lines_df))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Unit of Measure selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_Item_Assing_Variable)

                # Update Delivery Dates --> cannot be updated in main loop
                for Delivery_index, Delivery_Number in enumerate(PO_Delivery_Number_list):
                    Delivery_Date = PO_Delivery_Date_list[Delivery_index]
                    Delivery_No_condition = [(Delivery_Lines_df["Delivery_No"] == Delivery_Number)]
                    Delivery_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Delivery_Lines_df, conditions=Delivery_No_condition, Set_Column="delivery_start_date", Set_Value=Delivery_Date)
                    Delivery_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Delivery_Lines_df, conditions=Delivery_No_condition, Set_Column="delivery_end_date", Set_Value=Delivery_Date)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Delivery_Lines:Item_Splitting")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Random Method selected: {DEL_Assignment_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Delivery Random Method selected: {DEL_Assignment_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Serial Numbers  --------------------------------------------- #
    # Data preparation
    Delivery_Lines_df["Material_Group_NUS"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Material_Group_help", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Material_Group_NUS"), axis=1)
    Delivery_Lines_df["Item_Tracking_Code"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Item_Tracking_Code", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Item_Tracking_Code"), axis=1)
    Delivery_Lines_df["SN_Purchase_Inbound_Tracking"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="SN_Purchase_Inbound_Tracking", Compare_Column_df1=["Item_Tracking_Code"], Compare_Column_df2=["Code"], Search_df=Items_Tracking_df, Search_Column="SN_Purchase_Inbound_Tracking"), axis=1)
    Delivery_Lines_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Delivery_Lines_df, Columns_list=["Delivery_No", "order_ref_line_item_id", "Material_Group_NUS"], Accenting_list=[True, True, True]) 

    def Assing_SN(Filtered_row: tuple) -> None:
        Can_Continue = True
        SN_Line_List = []
        Filtered_row_index = Filtered_row[0]
        row_Series = Series(Filtered_row[1])
        quantity = row_Series["quantity"]
        Item_No = row_Series["supplier_aid"]

        # Prepare data
        if SN_Middle_Method == "Fixed":
            SN_Middle_Part = SN_Middle_Manual
        elif SN_Middle_Method == "Item No":
            SN_Middle_Part = Item_No
        elif SN_Middle_Method == "DateTime stamp":
            Today_dt = datetime.now()
            SN_Middle_Part = Today_dt.strftime(Numbers_DateTime_format)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"SN Middle Method selected: {SN_Middle_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Create SNs
        for i in range(0, quantity):
            SN_Line_List.append(f"{SN_Prefix}{SN_Middle_Part}{Filtered_row_index}{i}")
        SN_joined = ";".join(SN_Line_List)

        # Add to Delivery_Lines_df
        Delivery_Lines_df.at[Filtered_row_index, "serial_numbers"] = SN_joined
        return Can_Continue

    # Loop
    if Can_Continue == True:
        # Machines
        if SN_Machines == True:
            # Add Material Group to every line
            mask_Machines = Delivery_Lines_df["Material_Group_NUS"] == "0100"
            Delivery_Machine_df = DataFrame(Delivery_Lines_df[mask_Machines]) 
            if Delivery_Machine_df.empty:
                pass
            else:
                for Delivery_Machine_row in Delivery_Machine_df.iterrows():
                    Can_Continue = Assing_SN(Filtered_row=Delivery_Machine_row)
        else:
            pass

        # Tracked Items
        if SN_Tracked_Items == True:
            # Purchase Tracking
            mask_Trackings = Delivery_Lines_df["SN_Purchase_Inbound_Tracking"] == True
            Delivery_Tracking_df = DataFrame(Delivery_Lines_df[mask_Trackings]) 

            if Delivery_Tracking_df.empty:
                pass
            else:
                for Delivery_Tracking_row in Delivery_Tracking_df.iterrows():
                    Can_Continue = Assing_SN(Filtered_row=Delivery_Tracking_row)
        else:
            pass
    else:
        pass

    # --------------------------------------------- Calculate Delivery Lines  --------------------------------------------- #
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        mask_Delivery = Delivery_Lines_df["Delivery_No"] == Delivery_Number
        Delivery_Lines_df_Filtered = DataFrame(Delivery_Lines_df[mask_Delivery])

        Line_Counter = 1
        for row in Delivery_Lines_df_Filtered.iterrows():
            row_index = row[0]

            # Update Delivery_line_item_id
            Delivery_line_item_id = str(f"9{(Line_Counter) :05d}")
            Line_Counter += 1

            Delivery_Lines_df.at[row_index, "line_item_id"] = Delivery_line_item_id

    Delivery_Lines_df.drop(labels=["Material_Group_NUS"], inplace=True, axis=1)

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # Loop of Each Delivery Separate
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        mask_Delivery = Delivery_Lines_df["Delivery_No"] == Delivery_Number
        Delivery_Lines_df_Filtered = DataFrame(Delivery_Lines_df[mask_Delivery])
        
        # Prepare Json for each line of DataFrame
        PO_Delivery_Lines = []
        for row in Delivery_Lines_df_Filtered.iterrows():
            row_Series = Series(row[1])

            # Serial Number Check
            Serial_Number = str(row_Series["serial_numbers"])
            if Serial_Number != "":
                Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Line_SN")
            else:
                Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Line")

            # Assign Values
            Current_line_json["line_item_id"] = row_Series["line_item_id"]
            Current_line_json["article_id"]["supplier_aid"] = row_Series["supplier_aid"]

            Current_line_json["quantity"] = row_Series["quantity"]
            Current_line_json["order_unit"] = row_Series["order_unit"]

            Current_line_json["delivery_date"]["delivery_start_date"] = row_Series["delivery_start_date"]
            Current_line_json["delivery_date"]["delivery_end_date"] = row_Series["delivery_end_date"]

            Current_line_json["order_reference"]["order_id"] = row_Series["order_id"]
            Current_line_json["order_reference"]["line_item_id"] = row_Series["order_ref_line_item_id"]
            Current_line_json["order_reference"]["order_date"] = row_Series["order_date"]
            
            Current_line_json["supplier_order_reference"]["supplier_order_id"] = row_Series["supplier_order_id"]
            Current_line_json["supplier_order_reference"]["supplier_order_item_id"] = row_Series["supplier_order_item_id"]

            if Serial_Number != "":
                Serial_Numbers_List = Serial_Number.split(sep=";")
                Current_line_json["serial_numbers"] = Serial_Numbers_List
            else:
                pass
            
            PO_Delivery_Lines.append(Current_line_json)
            del Current_line_json
        
        # Add Lines to proper Delivery Header
        PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_item_list"] = PO_Delivery_Lines

    return PO_Deliveries, Delivery_Lines_df