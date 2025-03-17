# Import Libraries
import random
from pandas import DataFrame

import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTk, CTkFrame, StringVar, IntVar

def Generate_Delivery_Lines(Settings: dict, Configuration: dict, window: CTk, Purchase_Order: str, Delivery_Count: int, PO_Delivery_Number_list: list, PO_Delivery_Date_list: list, Confirmed_Lines_df: DataFrame, UoM_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Delivery_Lines_df_Columns = ["Purchase_Order", "Delivery_No", "line_item_id", "supplier_aid", "quantity", "order_unit", "delivery_start_date", "delivery_end_date", "order_id", "line_item_id", "order_date", "supplier_order_id", "supplier_order_item_id"]
    Delivery_Lines_df = DataFrame(columns=Delivery_Lines_df_Columns)
    Delivery_Lines_Template_List = []

    DEL_Random_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["Method"]
    DEL_FOCH_with_Main = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["FreeOfCharge_with_Main"]

    SN_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Prefix"]
    SN_Middle_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Method"]
    SN_Middle_Manual = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Manual"]
    SN_Suffix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Suffix"]

    # --------------------------------------------- Items Splitting  --------------------------------------------- #
    # Define Total Qty for Delivery
    if DEL_Random_Method == "Lines and Qty":
        To_Split_Qty = Confirmed_Lines_df["quantity"].sum()
    elif DEL_Random_Method == "Lines only":
        To_Split_Qty = len(Confirmed_Lines_df)
    
    Delivery_Qty_List = []
    Remaining_Deliveries = Delivery_Count
    Pick_Weight_step = 100 // Delivery_Count

    for i in range(1, Delivery_Count + 1):
        Step_PickAble_Qty = To_Split_Qty // 100 * (Pick_Weight_step * i)

        # Check Last Delivery
        if Remaining_Deliveries == 1:
            Delivery_Qty = To_Split_Qty
        else:
            try:
                Delivery_Qty = random.randint(a=1, b=Step_PickAble_Qty)
            except:
                Delivery_Qty = 1

        # Remaining After Selection
        Remaining_Deliveries = Delivery_Count - i
        To_Split_Qty = To_Split_Qty - Delivery_Qty
        if To_Split_Qty >= Remaining_Deliveries:
            pass
        else:
            Difference = Remaining_Deliveries - To_Split_Qty
            To_Split_Qty = To_Split_Qty + Difference
            Delivery_Qty = Delivery_Qty - Difference
            
        Delivery_Qty_List.append(Delivery_Qty)




        
    # Split According to MEthod and Delivery Qty





    # --------------------------------------------- Unit of Measure --------------------------------------------- #
    # TODO --> Like on Confirmation

    # --------------------------------------------- Serial Numbers  --------------------------------------------- #


    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # TODO --> Like on Confirmation




    return Delivery_Lines_df