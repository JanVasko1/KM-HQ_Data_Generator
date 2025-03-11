# Import Libraries
import random
from pandas import DataFrame

import Libs.GUI.Elements as Elements
import Libs.Pandas_Functions as Pandas_Functions

from customtkinter import CTk

def Generate_PO_CON_Lines(Settings: dict, 
                        Configuration: dict, 
                        window: CTk,
                        Purchase_Order: str,
                        Purchase_Lines_df: DataFrame, 
                        HQ_Item_Transport_Register_df: DataFrame,
                        Items_df: DataFrame, 
                        Items_BOMs_df: DataFrame, 
                        Items_Substitutions_df: DataFrame, 
                        Items_Connected_Items_df: DataFrame, 
                        Items_Price_List_Detail_df: DataFrame, 
                        Items_Tracking_df: DataFrame, 
                        Items_UoM_df: DataFrame, 
                        UoM_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Lines_df = DataFrame(columns=["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group"])

    Price_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Prices"]["Method"]

    Free_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Method"]

    Cable_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Number"]
    Cable_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Description"]
    Cable_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["QTY_per_Machine"]
    Cable_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Price"]
    Free_Cable_Number = ""
    Free_Cable_Description = ""
    Free_Cable_Quantity = ""
    Free_Cable_Price = ""

    Documentation_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Number"]
    Documentation_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Description"]
    Documentation_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["QTY_per_Machine"]
    Documentation_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Price"]
    Free_Documentation_Number = ""
    Free_Documentation_Description = ""
    Free_Documentation_Quantity = ""
    Free_Documentation_Price = ""

    Others_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["Number"]
    Others_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["Description"]
    Others_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["QTY_per_Machine"]
    Others_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["Price"]
    Free_Others_Number = ""
    Free_Others_Description = ""
    Free_Others_Quantity = ""
    Free_Others_Price = ""

    # Filter Dataframes by Purchase Order
    mask_HQ_Item_Tr_Reg = HQ_Item_Transport_Register_df["Document_No"] == Purchase_Order
    HQ_Item_Tr_Reg_Filtered = HQ_Item_Transport_Register_df[mask_HQ_Item_Tr_Reg]    

    mask_Machines = Items_df["Material_Group_NUS"] == "0100"
    Machines_df = Items_df[mask_Machines]  

    mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
    Purchase_Lines_df_Filtered = Purchase_Lines_df[mask_Purch_Line] 


    # --------------------------------------------- Items Definition --------------------------------------------- #
    Exported_Items_list = HQ_Item_Tr_Reg_Filtered["Item_No"].to_list()
    Exported_Lines_NOs_list = HQ_Item_Tr_Reg_Filtered["Exported_Line_No"].to_list()
    Lines_df["buyer_aid"] = Exported_Items_list
    Lines_df["Exported_Line_No"] = Exported_Lines_NOs_list
    

    print(Lines_df)
    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        if Price_Method == "Price List":
            Lines_df["price_amount"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Asset_No"], Search_df=Items_Price_List_Detail_df, Search_Column="DirectUnitCost"), axis=1)
        elif Price_Method == "Purchase Line":
            Price_PO_Line_List = Purchase_Lines_df_Filtered["Direct_Unit_Cost"].to_list()
            Lines_df["price_amount"] = Price_PO_Line_List
        elif Price_Method == "Prompt":
            pass
            # TODO
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Items price Method selected: {Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    print(Lines_df)
    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    Lines_df["price_line_amount"] = Lines_df["quantity"]*Lines_df["price_amount"]

    Total_Line_Amount = float(Lines_df["price_line_amount"].sum(axis=0))


    # -------------------- BEU Set -------------------- #
    # TODO --> not existing Case now 

    # -------------------- Free of Charge -------------------- #
    # Find Machine in Lines_df
    if Machines_df.empty:
        pass
    else:
        for machine_row in Machines_df.iterrows():
            
            if Can_Continue == True:
                if Free_Method == "Fixed":
                    # Cable
                    Free_Cable_Number = Cable_Number
                    Free_Cable_Description = Cable_Description
                    Free_Cable_Quantity = Cable_QTY_per_Machine
                    Free_Cable_Price = Cable_Price

                    # Documentation
                    Free_Documentation_Number = Documentation_Number
                    Free_Documentation_Description = Documentation_Description
                    Free_Documentation_Quantity = Documentation_QTY_per_Machine
                    Free_Documentation_Price = Documentation_Price

                    # Other
                    Free_Others_Number = Others_Number
                    Free_Others_Description = Others_Description
                    Free_Others_Quantity = Others_QTY_per_Machine
                    Free_Others_Price = Others_Price

                elif Free_Method == "Connected Items":
                    # Connected ITems - Free of Charge
                    pass
                elif Free_Method == "Prompt":
                    pass
                else:
                    Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Free of Charge Method selected: {Free_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    Can_Continue = False
            else:
                pass

    # -------------------- Label -------------------- #

    


    # Number of Lines in Document
    Lines_No = len(Lines_df)


    # --------------------------------------------- Line Flags --------------------------------------------- #
    # If USe
    # TODO --> LAbel Always


    # --------------------------------------------- Apply Header information --------------------------------------------- #


    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # TODO -- převést Exported_Line_No na supplier_order_item_id