# Import Libraries
import random
from pandas import DataFrame, Series

from customtkinter import CTk

import Libs.Defaults_Lists as Defaults_Lists

def Generate_PRO_ATP_CON_Lines(Settings: dict, Configuration: dict|None, window: CTk|None, PRO_Confirmed_Lines_df: DataFrame, PRO_Confirmation_Lines: dict, GUI: bool=True) -> dict:
    # --------------------------------------------- Defaults --------------------------------------------- #
    Lines_ATP_columns = ["quantity", "date", "stock_origin"]
    for Item_line in PRO_Confirmed_Lines_df.iterrows():
        Item_Line_index = Item_line[0]
        row_Series = Series(Item_line[1])

        PO_ATP_Lines = []
        Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Confirmation_ATP")
        Current_line_json["quantity"] = row_Series["quantity"]
        Current_line_json["date"] = row_Series["delivery_start_date"]
        Current_line_json["stock_origin"] = "ONH"

        PO_ATP_Lines.append(Current_line_json)
        del Current_line_json

        # Assign Values into Lines_dict
        PRO_Confirmation_Lines[Item_Line_index]["schedules"] = PO_ATP_Lines

    return PRO_Confirmation_Lines
