# Import Libraries
import random
from pandas import DataFrame, Series

from customtkinter import CTk

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Pandas_Functions as Pandas_Functions

def Generate_PO_ATP_CON_Lines(Settings: dict, Configuration: dict, window: CTk, Confirmed_Lines_df: DataFrame, PO_Confirmation_Lines: dict) -> dict:
    # --------------------------------------------- Defaults --------------------------------------------- #
    Date_format = Settings["0"]["General"]["Formats"]["Date"]

    ATP_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Use"]
    ATP_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Method"]

    ATP_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Method"]

    ONH_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["ONH"]
    ONB_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["ONB"]
    BACK_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["BACK"]

    ATP_ONH_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Fixed_Dates"]["ONH"]
    ATP_ONB_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Fixed_Dates"]["ONH"]

    ATP_Interval_ONH_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["From"]
    ATP_Interval_ONH_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["To"]
    ATP_Interval_ONB_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["From"]
    ATP_Interval_ONB_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["To"]

    # --------------------------------------------- Lines iteration --------------------------------------------- #
    if ATP_Enabled == True:
        if ATP_Quantity_Method == "Ratio":
            ratio = [ONH_Ratio, ONB_Ratio, BACK_Ratio]
            ratio_sum = sum(ratio)
        else:
            pass

        Lines_ATP_columns = ["quantity", "date", "stock_origin"]
        for Item_line in Confirmed_Lines_df.iterrows():
            Item_Line_index = Item_line[0]
            row_Series = Series(Item_line[1])
            Item_line_qty = row_Series["quantity"]

            Lines_ATP_df = DataFrame(columns=Lines_ATP_columns)

            # Quantity
            if ATP_Quantity_Method == "All On-Hand":
                new_row = {"quantity": Item_line_qty, "date": "", "stock_origin": "ONH"}
                Lines_ATP_df.loc[len(Lines_ATP_df)] = new_row
            elif ATP_Quantity_Method == "All On-Board":
                new_row = {"quantity": Item_line_qty, "date": "", "stock_origin": "ONB"}
                Lines_ATP_df.loc[len(Lines_ATP_df)] = new_row
            elif ATP_Quantity_Method == "Line Random":
                ONH_qty = random.randint(a=0, b=Item_line_qty)
                ONB_qty = Item_line_qty - ONH_qty

                if ONH_qty > 0:
                    new_row = {"quantity": ONH_qty, "date": "", "stock_origin": "ONH"}
                    Lines_ATP_df.loc[len(Lines_ATP_df)] = new_row
                else: 
                    pass

                if ONB_qty > 0:
                    new_row = {"quantity": ONB_qty, "date": "", "stock_origin": "ONB"}
                    Lines_ATP_df.loc[len(Lines_ATP_df)] = new_row
                else: 
                    pass
            elif ATP_Quantity_Method == "Ratio":
                raw_split = [Item_line_qty * part // ratio_sum for part in ratio]
                
                # Adjust any remaining amount to ensure the total sum is correct
                total_allocated = sum(raw_split)
                remaining = Item_line_qty - total_allocated
                
                # Distribute the remaining amount to the parts proportionally
                for i in range(remaining):
                    raw_split[i % len(ratio)] += 1

                ONH_qty = raw_split[0]
                ONB_qty = raw_split[1]
                # ONH
                if ONH_qty > 0:
                    new_row = {"quantity": ONH_qty, "date": "", "stock_origin": "ONH"}
                    Lines_ATP_df.loc[len(Lines_ATP_df)] = new_row
                else:
                    pass

                # ONB
                if ONB_qty > 0:
                    new_row = {"quantity": ONB_qty, "date": "", "stock_origin": "ONB"}
                    Lines_ATP_df.loc[len(Lines_ATP_df)] = new_row
                else:
                    pass

            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"ATP Quantity Method selected: {ATP_Quantity_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                Can_Continue = False

            # Dates
            if ATP_Dates_Method == "Fixed":
                # ONH
                ONH_conditions = [(Lines_ATP_df["stock_origin"] == "ONH")]
                Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Lines_ATP_df, conditions=ONH_conditions, Set_Column="date", Set_Value=ATP_ONH_Date)

                # ONB 
                ONB_conditions = [(Lines_ATP_df["stock_origin"] == "ONB")]
                ATP_ONB_week = Defaults_Lists.Date_str_to_Week_str(Date_str=ATP_ONB_Date, Format=Date_format)
                Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Lines_ATP_df, conditions=ONB_conditions, Set_Column="date", Set_Value=ATP_ONB_week)
            elif ATP_Dates_Method == "Intervals":
                # ONH
                ATP_ONH_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=ATP_Interval_ONH_From, To_int=ATP_Interval_ONH_To, Format=Date_format)
                ONH_conditions = [(Lines_ATP_df["stock_origin"] == "ONH")]
                Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Lines_ATP_df, conditions=ONH_conditions, Set_Column="date", Set_Value=ATP_ONH_Date)

                # ONB
                ATP_ONB_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=ATP_Interval_ONB_From, To_int=ATP_Interval_ONB_To, Format=Date_format)
                ONB_conditions = [(Lines_ATP_df["stock_origin"] == "ONB")]
                ATP_ONB_week = Defaults_Lists.Date_str_to_Week_str(Date_str=ATP_ONB_Date, Format=Date_format)
                Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Lines_ATP_df, conditions=ONB_conditions, Set_Column="date", Set_Value=ATP_ONB_week)

            elif ATP_Quantity_Method != "All BackOrder":
                # Create ATP Dictionary
                PO_ATP_Lines = []
                Lines_ATP_df["quantity"] = Lines_ATP_df["quantity"].round(2)
                for row in Lines_ATP_df.iterrows():
                    row_Series = Series(row[1])
                    Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Confirmation_ATP")

                    Current_line_json["quantity"] = row_Series["quantity"]
                    Current_line_json["date"] = row_Series["date"]
                    Current_line_json["stock_origin"] = row_Series["stock_origin"]

                    PO_ATP_Lines.append(Current_line_json)
                    del Current_line_json

                # Assign Values into Lines_dict
                PO_Confirmation_Lines[Item_Line_index]["schedules"] = PO_ATP_Lines

                # Add information to line element
                if ATP_ONH_Date != "":
                    PO_Confirmation_Lines[Item_Line_index]["delivery_date"]["delivery_start_date"] = ATP_ONH_Date
                    PO_Confirmation_Lines[Item_Line_index]["delivery_date"]["delivery_end_date"] = ATP_ONH_Date
                else:
                    PO_Confirmation_Lines[Item_Line_index]["delivery_date"]["delivery_start_date"] = ATP_ONB_Date
                    PO_Confirmation_Lines[Item_Line_index]["delivery_date"]["delivery_end_date"] = ATP_ONB_Date
                
                del Lines_ATP_df
            else:
                # If all Backordered delete whole Schedules information
                try:
                    del PO_Confirmation_Lines[Item_Line_index]["schedules"] 
                except:
                    pass
    else:
        pass

    return PO_Confirmation_Lines