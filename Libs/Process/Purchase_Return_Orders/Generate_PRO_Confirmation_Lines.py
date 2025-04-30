# Import Libraries
import random
from pandas import DataFrame, Series
from fastapi import HTTPException

import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTk, CTkFrame, StringVar

def Generate_PRO_CON_Lines(Settings: dict, 
                            Configuration: dict|None, 
                            window: CTk|None,
                            Purchase_Return_Order: str,
                            Purchase_Return_Lines_df: DataFrame, 
                            HQ_Item_Transport_Register_df: DataFrame,
                            Items_df: DataFrame, 
                            Items_Price_List_Detail_df: DataFrame, 
                            UoM_df: DataFrame,
                            GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    PRO_Confirmed_Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "cancelled", "Exported_Line_No"]
    PRO_Confirmed_Lines_df = DataFrame(columns=PRO_Confirmed_Lines_df_Columns)

    PRO_Price_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Prices"]["Method"]

    PRO_UoM_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Unit_of_Measure"]["Method"]
    PRO_Fixed_UoM = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Unit_of_Measure"]["Fixed_Options"]["Fix_UoM"]

    PRO_Reject_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Rejection"]["Method"]
    PRO_Reject_Ration_Confirm = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Rejection"]["Ratio"]["Confirm"]
    PRO_Reject_Ration_Reject = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Rejection"]["Ratio"]["Reject"]

    # Filter Dataframes by Purchase Order
    mask_HQ_Item_Tr_Reg = HQ_Item_Transport_Register_df["Document_No"] == Purchase_Return_Order
    HQ_Item_Tr_Reg_Filtered = DataFrame(HQ_Item_Transport_Register_df[mask_HQ_Item_Tr_Reg])

    mask_Purch_Ret_Line = Purchase_Return_Lines_df["Document_No"] == Purchase_Return_Order
    Purchase_Ret_Lines_df_Filtered = DataFrame(Purchase_Return_Lines_df[mask_Purch_Ret_Line])

    # --------------------------------------------- Items Definition --------------------------------------------- #
    PRO_Confirmed_Lines_df["buyer_aid"] = HQ_Item_Tr_Reg_Filtered["Item_No"].to_list()
    PRO_Confirmed_Lines_df["supplier_aid"] = HQ_Item_Tr_Reg_Filtered["Item_No"].to_list()
    PRO_Confirmed_Lines_df["description_long"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_long", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)
    PRO_Confirmed_Lines_df["Exported_Line_No"] = HQ_Item_Tr_Reg_Filtered["Exported_Line_No"].to_list()
    PRO_Confirmed_Lines_df["quantity"] = HQ_Item_Tr_Reg_Filtered["Quantity"].to_list()
    PRO_Confirmed_Lines_df["ordered_quantity"] = HQ_Item_Tr_Reg_Filtered["Quantity"].to_list()
    PRO_Confirmed_Lines_df["delivery_start_date"] = HQ_Item_Tr_Reg_Filtered["Order_Date"].to_list()
    PRO_Confirmed_Lines_df["delivery_end_date"] = HQ_Item_Tr_Reg_Filtered["Order_Date"].to_list()
    PRO_Confirmed_Lines_df["item_category"] = "YN01"
    PRO_Confirmed_Lines_df["cancelled"] = False

    # Number of Lines in Document
    Lines_No = len(PRO_Confirmed_Lines_df)

    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        if PRO_Price_Method == "Price List":
            PRO_Confirmed_Lines_df["price_amount"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Asset_No"], Search_df=Items_Price_List_Detail_df, Search_Column="DirectUnitCost"), axis=1)
        elif PRO_Price_Method == "Purchase Return Line":
            PRO_Confirmed_Lines_df["price_amount"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Ret_Lines_df_Filtered, Search_Column="Direct_Unit_Cost"), axis=1)
        elif PRO_Price_Method == "Prompt":
            if GUI == True:
                def Select_PRO_Prices(Frame_Body: CTkFrame, Lines_No: int):
                    Price_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkentry"]
                        try:
                            Value_Price = float(Value_CTkEntry.get())
                        except:
                            Value_Price = 0
                        Value_Price = round(number=Value_Price, ndigits=2)
                        Price_list.append(Value_Price)

                    PRO_Confirmed_Lines_df["price_amount"] = Price_list
                    PRO_Price_Variable.set(value="Selected")
                    PRO_Price_Window.destroy()

                # TopUp Window
                PRO_Price_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_Price_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_Price_Window_geometry[1] //2
                PRO_Price_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Price for Items.", max_width=PRO_Price_Window_geometry[0], max_height=PRO_Price_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_Price_Window, Name="Select Price for Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Price for each Item of Confirmation.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Prices
                for row in PRO_Confirmed_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["buyer_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal", Validation="Float") 
                    PRO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PRO_Fields_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PRO_Price_Window_geometry[1]:
                    content_height = PRO_Price_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PRO_Price_Window.maxsize(width=PRO_Price_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PRO_Price_Variable = StringVar(master=PRO_Price_Window, value="", name="PRO_Price_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_Prices(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Price selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_Price_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PRO_CON_Lines:Price")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items price Method selected: {PRO_Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items price Method selected: {PRO_Price_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Unit of Measure --------------------------------------------- #
    if Can_Continue == True:
        if PRO_UoM_Method == "Fixed":
            PRO_Confirmed_Lines_df["order_unit"] = PRO_Fixed_UoM
        elif PRO_UoM_Method == "Purchase Return Line":
            PRO_Confirmed_Lines_df["PRO_UoM"] = ""
            PRO_Confirmed_Lines_df["PRO_UoM"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="PRO_UoM", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Ret_Lines_df_Filtered, Search_Column="Unit_of_Measure_Code"), axis=1)
            PRO_Confirmed_Lines_df["order_unit"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit", Compare_Column_df1=["PRO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
            PRO_Confirmed_Lines_df.drop(labels=["PRO_UoM"], inplace=True, axis=1)
        elif PRO_UoM_Method == "HQ Item Transport Export":
            PRO_Confirmed_Lines_df["PRO_UoM"] = ""
            PRO_Confirmed_Lines_df["PRO_UoM"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="PRO_UoM", Compare_Column_df1=["buyer_aid", "Exported_Line_No"], Compare_Column_df2=["Item_No", "Exported_Line_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Unit_of_Measure"), axis=1)
            PRO_Confirmed_Lines_df["order_unit"] = PRO_Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit", Compare_Column_df1=["PRO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
            PRO_Confirmed_Lines_df.drop(labels=["PRO_UoM"], inplace=True, axis=1)
        elif PRO_UoM_Method == "Prompt":
            if GUI == True:
                def Select_PRO_UoM(Frame_Body: CTkFrame, Lines_No: int):
                    UoM_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkentry"]
                        try:
                            Value_UoM = Value_CTkEntry.get()
                        except:
                            Value_UoM = ""
                        UoM_list.append(Value_UoM)

                    PRO_Confirmed_Lines_df["order_unit"] = UoM_list
                    PRO_UoM_Variable.set(value="Selected")
                    PRO_UoM_Window.destroy()

                # TopUp Window
                PRO_UoM_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_UoM_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_UoM_Window_geometry[1] //2
                PRO_UoM_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Unit of Measure for Items Items.", max_width=PRO_UoM_Window_geometry[0], max_height=PRO_UoM_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_UoM_Window, Name="Select Unit of Measure for Items Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Unit of Measure for each Item of Confirmation.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Unit of Measure
                for row in PRO_Confirmed_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["buyer_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal") 
                    PRO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PRO_Fields_Frame_Var.configure(placeholder_text="Manual Unit of Measure", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PRO_UoM_Window_geometry[1]:
                    content_height = PRO_UoM_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PRO_UoM_Window.maxsize(width=PRO_UoM_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PRO_UoM_Variable = StringVar(master=PRO_UoM_Window, value="", name="PRO_UoM_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_UoM(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Unit of Measure selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_UoM_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PRO_CON_Lines:Unit_of_Measure")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items Unit of Measure Method selected: {PRO_UoM_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items Unit of Measure Method selected: {PRO_UoM_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Item Rejection --------------------------------------------- #
    if Can_Continue == True:
        if PRO_Reject_Method == "Confirm All":
            PRO_Confirmed_Lines_df["cancelled"] = False
        elif PRO_Reject_Method == "Reject All":
            PRO_Confirmed_Lines_df["cancelled"] = True
        elif PRO_Reject_Method == "Random Reject":
            Index_to_Reject_list = []
            index_list = PRO_Confirmed_Lines_df.index.to_list()
            Max_number = PRO_Confirmed_Lines_df.shape[0]
            No_Lines_to_Reject = random.randint(a=0, b=Max_number - 1)  # Considerate as index later

            # Find Indexes
            for i in range(0, No_Lines_to_Reject):
                Selected_index = random.choice(index_list)
                index_list.remove(Selected_index)
                Index_to_Reject_list.append(Selected_index)

            # Reject lines
            for index in Index_to_Reject_list:
                PRO_Confirmed_Lines_df.at[index, "cancelled"] = True
        elif PRO_Reject_Method == "Ratio":
            ratio = [PRO_Reject_Ration_Confirm, PRO_Reject_Ration_Reject]
            ratio_sum = sum(ratio)
            
            Lines_sum = PRO_Confirmed_Lines_df["quantity"].sum()
            raw_split = [Lines_sum * part // ratio_sum for part in ratio]

            # Sort according to qty
            PRO_Confirmed_Lines_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=PRO_Confirmed_Lines_df, Columns_list=["quantity"], Accenting_list=[False]) 
    
            Conf_rem_Qty = 0
            for row in PRO_Confirmed_Lines_df.iterrows():
                # Dataframe
                row_index = row[0]
                row_Series = Series(row[1])
                Quantity = row_Series["quantity"]

                if Conf_rem_Qty < raw_split[0]:
                    pass
                else:
                    PRO_Confirmed_Lines_df.at[row_index, "cancelled"] = True
                Conf_rem_Qty += Quantity

            # Sort according back again
            PRO_Confirmed_Lines_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=PRO_Confirmed_Lines_df, Columns_list=["Exported_Line_No"], Accenting_list=[True]) 
    
        elif PRO_Reject_Method == "Prompt":
            if GUI == True:
                # Select Delivery PopUp
                def Select_PRO_Reject(Frame_Body: CTkFrame, Lines_No: int):
                    PRO_Reject_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkCheck = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkcheckbox"]
                        Value_CTkCheck_Value = Value_CTkCheck.get()
                        if Value_CTkCheck_Value == True:
                            PRO_Reject_list.append("True")
                        else:
                            PRO_Reject_list.append("False")
                    PO_DEL_Number_list_joined = ";".join(PRO_Reject_list)
                    PRO_Reject_Variable.set(value=PO_DEL_Number_list_joined)
                    PRO_Reject_Window.destroy()

                # TopUp Window
                PRO_Reject_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_Reject_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_Reject_Window_geometry[1] //2
                PRO_Reject_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Items to be rejected.", max_width=PRO_Reject_Window_geometry[0], max_height=PRO_Reject_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_Reject_Window, Name=f"Select Items to be rejected.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip=f"To select which will be rejected by BEU on Confirmation.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Lines Flags
                for row in PRO_Confirmed_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]
                    Item_Line = row_Series["Exported_Line_No"]

                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column", Label=f"{Item_Line} - {Item_No}", Field_Type="Input_CheckBox") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                    Fields_Frame_Var.configure(text="")

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PRO_Reject_Window_geometry[1]:
                    content_height = PRO_Reject_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PRO_Reject_Window.maxsize(width=PRO_Reject_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PRO_Reject_Variable = StringVar(master=PRO_Reject_Window, value="", name="PRO_Reject_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_Reject(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Number selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_Reject_Variable)
                PRO_Cancelled_list = PRO_Reject_Variable.get().split(";")
                PRO_Cancelled_list = list(map(lambda x: True if x.lower() == "true" else False, PRO_Cancelled_list))
                PRO_Confirmed_Lines_df["cancelled"] = PRO_Cancelled_list
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PRO_CON_Lines:Unit_of_Measure")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items Rejection Method selected: {PRO_Reject_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items Rejection Method selected: {PRO_Reject_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    PRO_Confirmed_Lines_df["price_line_amount"] = PRO_Confirmed_Lines_df["quantity"]*PRO_Confirmed_Lines_df["price_amount"]

    Total_Line_Amount = float(PRO_Confirmed_Lines_df["price_line_amount"].sum(axis=0))


    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # line_item_id
    PRO_Confirmed_Lines_df["Exported_Line_No"] = PRO_Confirmed_Lines_df["Exported_Line_No"].astype(int)
    PRO_Confirmed_Lines_df["line_item_id"] = PRO_Confirmed_Lines_df["Exported_Line_No"] // 100

    # supplier_order_item_id
    line_item_id_list= []
    for i in range(1, Lines_No + 1):
        line_item_id = i * 10
        line_item_id_list.append((f"{line_item_id :06d}"))
    PRO_Confirmed_Lines_df["supplier_order_item_id"] = line_item_id_list

    # Round Values
    PRO_Confirmed_Lines_df["quantity"] = PRO_Confirmed_Lines_df["quantity"].round(2)
    PRO_Confirmed_Lines_df["ordered_quantity"] = PRO_Confirmed_Lines_df["ordered_quantity"].round(2)
    PRO_Confirmed_Lines_df["price_amount"] = PRO_Confirmed_Lines_df["price_amount"].round(2)
    PRO_Confirmed_Lines_df["price_line_amount"] = PRO_Confirmed_Lines_df["price_line_amount"].round(2)

    # Prepare Json for each line of DataFrame
    PRO_Confirmation_Lines = []
    for row in PRO_Confirmed_Lines_df.iterrows():
        row_Series = Series(row[1])
        Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PRO_Confirmation_Line")

        # Assign Values
        Current_line_json["line_item_id"] = row_Series["line_item_id"]
        Current_line_json["article_id"]["supplier_aid"] = row_Series["supplier_aid"]
        Current_line_json["article_id"]["buyer_aid"] = row_Series["buyer_aid"]
        Current_line_json["article_id"]["description_long"] = row_Series["description_long"]

        Current_line_json["quantity"] = row_Series["quantity"]
        Current_line_json["order_unit"] = row_Series["order_unit"]

        Current_line_json["article_price"]["price_amount"] = row_Series["price_amount"]
        Current_line_json["article_price"]["price_line_amount"] = row_Series["price_line_amount"]

        Current_line_json["delivery_date"]["delivery_start_date"] = row_Series["delivery_start_date"]
        Current_line_json["delivery_date"]["delivery_end_date"] = row_Series["delivery_end_date"]

        Current_line_json["remarks"]["ordered_quantity"] = row_Series["ordered_quantity"]
        Current_line_json["remarks"]["supplier_order_item_id"] = row_Series["supplier_order_item_id"]
        Current_line_json["remarks"]["item_category"] = row_Series["item_category"]
        if row_Series["cancelled"] == "False":
            Current_line_json["remarks"]["cancelled"] = False
        else:
            Current_line_json["remarks"]["cancelled"] = row_Series["cancelled"]

        PRO_Confirmation_Lines.append(Current_line_json)
        del Current_line_json

    Lines_No = len(PRO_Confirmed_Lines_df)
    return PRO_Confirmed_Lines_df, PRO_Confirmation_Lines, Total_Line_Amount, Lines_No