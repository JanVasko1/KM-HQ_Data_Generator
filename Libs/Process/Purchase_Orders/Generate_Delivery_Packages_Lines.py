# Import Libraries
from pandas import DataFrame, Series

import Libs.Pandas_Functions as Pandas_Functions

def Generate_Delivery_Packages_Lines(Settings: dict, Configuration: dict, PO_Deliveries: dict, PO_Delivery_Number_list: list, Delivery_Lines_df: DataFrame, Package_Header_df: DataFrame, Items_UoM_df: DataFrame, UoM_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Package_Lines_df_Columns = ["Delivery_No", "package_id", "package_itemnumber", "package_unit", "package_quantity", "package_plant"]
    Package_Lines_df = DataFrame(columns=Package_Lines_df_Columns)

    Pack_Item_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Items"]["Method"]
    
    Pack_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Method"]
    Pack_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Fixed_Plant"]

    # --------------------------------------------- Data Preparation --------------------------------------------- #
    # UoM
    print(Delivery_Lines_df)
    print("----------------------------------------------------")
    Delivery_Lines_df["order_unit_Help"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit_Help", Compare_Column_df1=["order_unit"], Compare_Column_df2=["International_Standard_Code"], Search_df=UoM_df, Search_Column="Code"), axis=1)
    Delivery_Lines_df["Item_Weight_Help"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Item_Weight_Help", Compare_Column_df1=["supplier_aid", "order_unit_Help"], Compare_Column_df2=["Item_No", "Code"], Search_df=Items_UoM_df, Search_Column="Weight"), axis=1)
    Delivery_Lines_df["Item_Volume_Help"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Item_Volume_Help", Compare_Column_df1=["supplier_aid", "order_unit_Help"], Compare_Column_df2=["Item_No", "Code"], Search_df=Items_UoM_df, Search_Column="Cubage"), axis=1)
    Delivery_Lines_df.drop(labels=["order_unit_Help"], inplace=True, axis=1)
    print(Delivery_Lines_df)
    print("----------------------------------------------------")


    print(Package_Header_df)
    # --------------------------------------------- Item Assignment to Packages --------------------------------------------- #

    # --------------------------------------------- Plant --------------------------------------------- #

    # --------------------------------------------- Totals for Package Header --------------------------------------------- #

    # --------------------------------------------- Totals for Delivery Footer --------------------------------------------- #

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    return PO_Deliveries