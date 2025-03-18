# Import Libraries
import random
from datetime import datetime
from pandas import DataFrame, Series

import Libs.Pandas_Functions as Pandas_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements as Elements

from customtkinter import CTk

def Generate_Delivery_Lines(Settings: dict, Configuration: dict, window: CTk, Purchase_Order: str, PO_Deliveries: list, Delivery_Count: int, PO_Delivery_Number_list: list, PO_Delivery_Date_list: list, Confirmed_Lines_df: DataFrame, PO_Confirmation_Number: str, HQ_Item_Transport_Register_df: DataFrame, Items_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    Delivery_Lines_df_Columns = ["Delivery_No", "line_item_id", "supplier_aid", "quantity", "order_unit", "delivery_start_date", "delivery_end_date", "order_id", "order_ref_line_item_id", "order_date", "supplier_order_id", "supplier_order_item_id", "serial_numbers"]
    Delivery_Lines_df = DataFrame(columns=Delivery_Lines_df_Columns)
    Delivery_Lines_Template_List = []

    DEL_Random_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["Method"]
    DEL_FOCH_with_Main = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["FreeOfCharge_with_Main"]

    SN_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Prefix"]
    SN_Middle_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Method"]
    SN_Middle_Manual = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Fixed"]

    print(HQ_Item_Transport_Register_df)
    print("------------------------------------------------------------------")
    print(Confirmed_Lines_df)
    print("------------------------------------------------------------------")
    print(Delivery_Lines_df)
    # --------------------------------------------- Items Splitting  --------------------------------------------- #
    if DEL_Random_Method == "Lines and Qty":
        # Define Total Qty for Delivery
        To_Split_Qty = Confirmed_Lines_df["quantity"].sum()
        if DEL_FOCH_with_Main == True:
            # TODO --> Minus FOCH Qty from whole Sum_Qty --> as should be on the same Delivery as machine
            pass 
        else:
            pass
    elif DEL_Random_Method == "Lines only":
        # Define Total Qty for Delivery
        To_Split_Qty = len(Confirmed_Lines_df)
        if DEL_FOCH_with_Main == True:
            # TODO --> Minus FOCH lines count from whole Sum_Lines --> as should be on the same Delivery as machine
            pass 
        else:
            pass
    else:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Delivery Random Method selected: {DEL_Random_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
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

        print(f"Split by ration: {Delivery_Qty_Split_List}")

        # Split According to Method and Delivery Qty
        if DEL_Random_Method == "Lines and Qty":
            # TODO --> to Finish whole split method Lines and Qty
            pass
        elif DEL_Random_Method == "Lines only":
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

                print(f"Lines for Delivery: {Selected_Line_indexes}")

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
                    Delivery_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_End(Insert_DataFrame=Delivery_Lines_df, New_Row=Delivery_Line_Values)

        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Delivery Random Method selected: {DEL_Random_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    Delivery_Lines_df["Material_Group_NUS"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Material_Group_help", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Material_Group_NUS"), axis=1)
    Delivery_Lines_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Delivery_Lines_df, Columns_list=["Delivery_No", "order_ref_line_item_id", "Material_Group_NUS"], Accenting_list=[True, True, True]) 

    # --------------------------------------------- Serial Numbers  --------------------------------------------- #
    if Can_Continue == True:
        # Add Material Group to every line
        mask_Machines = Delivery_Lines_df["Material_Group_NUS"] == "0100"
        Delivery_Machine_df = Delivery_Lines_df[mask_Machines]  
        if Delivery_Machine_df.empty:
            pass
        else:
            for Delivery_Machine_row in Delivery_Machine_df.iterrows():
                SN_Line_List = []
                Delivery_Machine_index = Delivery_Machine_row[0]
                row_Series = Series(Delivery_Machine_row[1])
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
                    Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"SN Middle Method selected: {SN_Middle_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    Can_Continue = False

                # Create SNs
                for i in range(0, quantity):
                    SN_Line_List.append(f"{SN_Prefix}{SN_Middle_Part}{i}")
                SN_joined = ";".join(SN_Line_List)

                # Add to Delivery_Lines_df
                Delivery_Lines_df.at[Delivery_Machine_index, "serial_numbers"] = SN_joined
    else:
        pass

    Delivery_Lines_df.drop(labels=["Material_Group_NUS"], inplace=True, axis=1)
    print("------------------------------------------------------------------")
    print(Delivery_Lines_df)
    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # Loop of Each Delivery Separate
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        mask_Delivery = Delivery_Lines_df["Delivery_No"] == Delivery_Number
        Delivery_Lines_df_Filtered = Delivery_Lines_df[mask_Delivery]
        
        # Prepare Json for each line of DataFrame
        PO_Delivery_Lines = []
        Line_Counter = 1
        for row in Delivery_Lines_df_Filtered.iterrows():
            row_Series = Series(row[1])

            # Update Delivery_line_item_id
            Delivery_line_item_id = str(f"9{(Line_Counter) :05d}")
            Line_Counter += 1

            # Serial Number Check
            Serial_Number = str(row_Series["serial_numbers"])
            if Serial_Number != "":
                Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Line_SN")
            else:
                Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Line")

            # Assign Values
            Current_line_json["line_item_id"] = Delivery_line_item_id
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