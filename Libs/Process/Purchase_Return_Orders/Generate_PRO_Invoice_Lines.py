# Import Libraries
import random
from pandas import DataFrame, Series
from fastapi import HTTPException

import Libs.Pandas_Functions as Pandas_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

from customtkinter import CTk, CTkFrame, StringVar

def Generate_Credit_Memo_Lines(Settings: dict, Configuration: dict|None, window: CTk|None, Purchase_Return_Order: str, Purchase_Return_Lines_df: DataFrame, PRO_Credit_Memo: dict, PRO_Return_Shipment_Number: str, PRO_Shipment_Lines_df: DataFrame, PRO_Confirmed_Lines_df: DataFrame, Items_df: DataFrame, Items_Price_List_Detail_df: DataFrame, Country_ISO_Code_list: list, Tariff_Number_list: list, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Credit_Memo_Lines_df_columns = ["Invoice_No", "line_item_id", "supplier_aid", "description_short", "quantity", "order_unit", "price_amount", "price_line_amount", "order_id", "order_line_item_id", "order_date", "supplier_order_id", "supplier_order_item_id", "delivery_note_id", "delivery_line_item_id", "tariff_number", "origin", "plant"]
    Credit_Memo_Lines_df = DataFrame(columns=Credit_Memo_Lines_df_columns)

    Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Prices"]["Method"]

    Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Method"]
    Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Fixed_Options"]["Plants_List"])
    Plant = ""

    Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Country_Of_Origin"]["Method"]
    Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Tariff"]["Method"]
    Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    # Filter Dataframes by Purchase Order
    mask_Purch_Ret_Line = Purchase_Return_Lines_df["Document_No"] == Purchase_Return_Order
    Purchase_Return_Lines_df_Filtered = DataFrame(Purchase_Return_Lines_df[mask_Purch_Ret_Line])

    mask_Shipment_lines = PRO_Shipment_Lines_df["Document_No"] == PRO_Return_Shipment_Number
    PRO_Shipment_Lines_df_Filtered = DataFrame(PRO_Shipment_Lines_df[mask_Shipment_lines])

    # --------------------------------------------- Data from PRO_Shipment_Lines_df --------------------------------------------- #
    # Apply Lists to DataFrame
    Credit_Memo_Lines_df["supplier_aid"] = PRO_Confirmed_Lines_df["supplier_aid"].to_list()
    Credit_Memo_Lines_df["quantity"] = PRO_Confirmed_Lines_df["quantity"].to_list()
    Credit_Memo_Lines_df["order_unit"] = PRO_Confirmed_Lines_df["order_unit"].to_list()

    Credit_Memo_Lines_df["order_id"] = Purchase_Return_Order
    Credit_Memo_Lines_df["order_line_item_id"] = [f"{x :06d}" for x in PRO_Confirmed_Lines_df["line_item_id"].to_list()]       
    Credit_Memo_Lines_df["order_date"] = Purchase_Return_Lines_df.iloc[0]["Order_Date_NUS"]

    Credit_Memo_Lines_df["supplier_order_id"] = PRO_Confirmed_Lines_df["Vendor_Document_No"].to_list()
    Credit_Memo_Lines_df["supplier_order_item_id"] = PRO_Confirmed_Lines_df["supplier_order_item_id"].to_list()

    Credit_Memo_Lines_df["delivery_note_id"] = PRO_Return_Shipment_Number
    Credit_Memo_Lines_df["delivery_line_item_id"] = [f"{x :06d}" for x in PRO_Shipment_Lines_df_Filtered["Line_No"].to_list()]

    Credit_Memo_Lines_df["description_short"] = Credit_Memo_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_short", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)

    # --------------------------------------------- Calculate Credit Memo Lines  --------------------------------------------- #
    Line_Counter = 10
    for row in Credit_Memo_Lines_df.iterrows():
        row_index = row[0]

        # Update line_item_id
        Invoice_line_item_id = str(f"{Line_Counter :06d}")
        Line_Counter += 10

        Credit_Memo_Lines_df.at[row_index, "line_item_id"] = Invoice_line_item_id

    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        Credit_Memo_Lines_df["price_amount"] = 0
        if Price_Method == "Price List":
            Credit_Memo_Lines_df["price_amount"] = Credit_Memo_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["Asset_No"], Search_df=Items_Price_List_Detail_df, Search_Column="DirectUnitCost"), axis=1)
        elif Price_Method == "Purchase Return Line":
            Credit_Memo_Lines_df["price_amount"] = Credit_Memo_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Return_Lines_df_Filtered, Search_Column="Direct_Unit_Cost"), axis=1)
        elif Price_Method == "From Confirmation":
            Credit_Memo_Lines_df["price_amount"] = Credit_Memo_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["supplier_aid", "supplier_order_item_id"], Compare_Column_df2=["supplier_aid", "supplier_order_item_id"], Search_df=PRO_Confirmed_Lines_df, Search_Column="price_amount"), axis=1)
        elif Price_Method == "Prompt":
            if GUI == True:
                def Select_PRO_CR_Price(Frame_Body: CTkFrame, Lines_No: int):
                    PRO_CR_Price_list = []
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
                        PRO_CR_Price_list.append(str(Value_Price))

                    PRO_CR_Price_list_joined = ";".join(PRO_CR_Price_list)
                    PRO_CR_Price_Variable.set(value=PRO_CR_Price_list_joined)
                    PRO_CR_Price_Window.destroy()

                # TopUp Window
                PRO_CR_Price_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_CR_Price_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_CR_Price_Window_geometry[1] //2
                PRO_CR_Price_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Price for Credit Memo lines.", max_width=PRO_CR_Price_Window_geometry[0], max_height=PRO_CR_Price_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_CR_Price_Window, Name=f"Select Price for Credit Memo lines.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Price for each Credit Memo lines.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Lines_No = Credit_Memo_Lines_df.shape[0]
                for row in Credit_Memo_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal", Validation="Float") 
                    PRO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PRO_Fields_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = (content_row_count + 1) * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PRO_CR_Price_Window_geometry[1]:
                    content_height = PRO_CR_Price_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PRO_CR_Price_Window.maxsize(width=PRO_CR_Price_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PRO_CR_Price_Variable = StringVar(master=PRO_CR_Price_Window, value="", name="PRO_CR_Price_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_CR_Price(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Price selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_CR_Price_Variable)
                Prices_List = PRO_CR_Price_Variable.get().split(";")
                Prices_List = [float(element) for element in Prices_List]

                # Apply Prices
                Credit_Memo_Lines_df["price_amount"] = Prices_List
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Credit_Memo_Lines:Price.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items price Method selected: {Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items price Method selected: {Price_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    Credit_Memo_Lines_df["price_line_amount"] = Credit_Memo_Lines_df["quantity"]*Credit_Memo_Lines_df["price_amount"]

    # --------------------------------------------- Plants --------------------------------------------- #
    if Can_Continue == True:
        if Inv_Plant_Method == "Fixed":
            Plant = Inv_Fixed_Plant
        elif Inv_Plant_Method == "Random":
            Plant = random.choice(Inv_Fixed_Plants_List)
        elif Inv_Plant_Method == "Empty":
            Plant = ""
        elif Inv_Plant_Method == "Prompt":
            if GUI == True:
                def Select_PRO_CR_Plant(Frame_Body: CTkFrame):
                    Value_CTkEntry = Frame_Body.children[f"!ctkframe"].children["!ctkframe3"].children["!ctkoptionmenu"]
                    try:
                        Value_Plant = Value_CTkEntry.get()
                    except:
                        Value_Plant = "1000"

                    PRO_CR_Plant_Variable.set(value=Value_Plant)
                    PRO_CR_Plant_Window.destroy()

                # TopUp Window
                PRO_CR_Plant_Window_geometry = (520, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_CR_Plant_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_CR_Plant_Window_geometry[1] //2
                PRO_CR_Plant_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Plant for selected Credit Memo.", max_width=PRO_CR_Plant_Window_geometry[0], max_height=PRO_CR_Plant_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_CR_Plant_Window, Name="Select Plant for selected Credit Memo.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Plant for Credit Memo..", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Fields
                Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"Plant", Field_Type="Input_OptionMenu") 
                Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                Fields_Frame_Var.set(value="")
                Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Inv_Fixed_Plants_List, command=None, GUI_Level_ID=3)

                # Buttons
                PRO_CR_Plant_Variable = StringVar(master=PRO_CR_Plant_Window, value="", name="PRO_CR_Plant_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_CR_Plant(Frame_Body=Frame_Body))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Plant selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_CR_Plant_Variable)
                Plant = PRO_CR_Plant_Variable.get()
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Credit_Memo_Lines:Plant.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Plants Method selected: {Inv_Plant_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Plants Method selected: {Inv_Plant_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # Assign Plant according Invoice_No
    Credit_Memo_Lines_df["plant"] = Plant

    # --------------------------------------------- Country of Origin --------------------------------------------- #
    if Can_Continue == True:
        if Count_Origin_Method == "Fixed":
            Credit_Memo_Lines_df["origin"] = Fixed_Count_Origin
        elif Count_Origin_Method == "Random":
            Credit_Memo_Lines_df["origin"] = Credit_Memo_Lines_df.apply(lambda row: random.choice(Country_ISO_Code_list), axis=1)
        elif Count_Origin_Method == "Empty":
            Credit_Memo_Lines_df["origin"] = ""
        elif Count_Origin_Method == "Prompt":
            if GUI == True:
                def Select_PRO_CR_Country_Origin(Frame_Body: CTkFrame, Lines_No: int):
                    PRO_CR_Country_Origin_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkoptionmenu"]
                        try:
                            Value_Country_Origin = Value_CTkEntry.get()
                        except:
                            Value_Country_Origin = ""
                        PRO_CR_Country_Origin_list.append(Value_Country_Origin)

                    PRO_CR_Country_Origin_list_joined = ";".join(PRO_CR_Country_Origin_list)
                    PRO_CR_Country_Origin_Variable.set(value=PRO_CR_Country_Origin_list_joined)
                    PRO_CR_Country_Origin_Window.destroy()

                # TopUp Window
                PRO_CR_Country_Origin_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_CR_Country_Origin_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_CR_Country_Origin_Window_geometry[1] //2
                PRO_CR_Country_Origin_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Country of Origin for Credit Memo lines.", max_width=PRO_CR_Country_Origin_Window_geometry[0], max_height=PRO_CR_Country_Origin_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_CR_Country_Origin_Window, Name=f"Select Country Origin for Credit Memo lines.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Country of Origin for each Credit Memo..", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Lines_No = Credit_Memo_Lines_df.shape[0]
                for row in Credit_Memo_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Fields_Frame_Var.set(value="")
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Country_ISO_Code_list, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = (content_row_count + 1) * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PRO_CR_Country_Origin_Window_geometry[1]:
                    content_height = PRO_CR_Country_Origin_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PRO_CR_Country_Origin_Window.maxsize(width=PRO_CR_Country_Origin_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PRO_CR_Country_Origin_Variable = StringVar(master=PRO_CR_Country_Origin_Window, value="", name="PRO_CR_Country_Origin_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_CR_Country_Origin(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Country Origin selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_CR_Country_Origin_Variable)
                Country_Origins_List = PRO_CR_Country_Origin_Variable.get().split(";")

                # Apply Country of Origin
                Credit_Memo_Lines_df["origin"] = Country_Origins_List
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Credit_Memo_Lines:Country_of_Origin.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Country of Origin  Method selected: {Count_Origin_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Country of Origin  Method selected: {Count_Origin_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass
    
    # --------------------------------------------- Tariff --------------------------------------------- # 
    if Can_Continue == True:
        if Tariff_Method == "Fixed":
            Credit_Memo_Lines_df["tariff_number"] = Fixed_Tariff
        elif Tariff_Method == "Random":
            Credit_Memo_Lines_df["tariff_number"] = Credit_Memo_Lines_df.apply(lambda row: random.choice(Tariff_Number_list), axis=1)
        elif Tariff_Method == "Empty":
            Credit_Memo_Lines_df["tariff_number"] = ""
        elif Tariff_Method == "Prompt":
            if GUI == True:
                def Select_PRO_CR_Tariff(Frame_Body: CTkFrame, Lines_No: int):
                    PRO_CR_Tariff_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkoptionmenu"]
                        try:
                            Value_Tariff = Value_CTkEntry.get()
                        except:
                            Value_Tariff = ""
                        PRO_CR_Tariff_list.append(Value_Tariff)

                    PRO_CR_Tariff_list_joined = ";".join(PRO_CR_Tariff_list)
                    PRO_CR_Tariff_Variable.set(value=PRO_CR_Tariff_list_joined)
                    PRO_CR_Tariff_Window.destroy()

                # TopUp Window
                PRO_CR_Tariff_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_CR_Tariff_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_CR_Tariff_Window_geometry[1] //2
                PRO_CR_Tariff_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Tariff for Credit Memo lines.", max_width=PRO_CR_Tariff_Window_geometry[0], max_height=PRO_CR_Tariff_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_CR_Tariff_Window, Name=f"Select Tariff for Credit Memo lines.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Tariff for each line of Credit Memo.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Lines_No = Credit_Memo_Lines_df.shape[0]
                for row in Credit_Memo_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Fields_Frame_Var.set(value="")
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Tariff_Number_list, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = (content_row_count + 1) * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PRO_CR_Tariff_Window_geometry[1]:
                    content_height = PRO_CR_Tariff_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PRO_CR_Tariff_Window.maxsize(width=PRO_CR_Tariff_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PRO_CR_Tariff_Variable = StringVar(master=PRO_CR_Tariff_Window, value="", name="PRO_CR_Tariff_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_CR_Tariff(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Tariff selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_CR_Tariff_Variable)
                Tariffs_List = PRO_CR_Tariff_Variable.get().split(";")

                # Apply Tariff
                Credit_Memo_Lines_df["tariff_number"] = Tariffs_List
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Credit_Memo_Lines:Tariff.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Tariff Method selected: {Tariff_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Tariff Method selected: {Tariff_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # Round Values
    Credit_Memo_Lines_df["quantity"] = Credit_Memo_Lines_df["quantity"].round(2)
    Credit_Memo_Lines_df["price_amount"] = Credit_Memo_Lines_df["price_amount"].round(2)
    Credit_Memo_Lines_df["price_line_amount"] = Credit_Memo_Lines_df["price_line_amount"].round(2)

    # Invoice Total data preparation
    Total_Invoice_Lines_Count = len(Credit_Memo_Lines_df)
    Total_invoice_Amount = round(number=float(Credit_Memo_Lines_df["price_line_amount"].sum(axis=0)), ndigits=2)

    # Prepare Json for each line of DataFrame + PDF data
    PO_Invoice_Lines = []
    Table_Data = []
    Table_Data.append(["Item No", "Description", "Quantity", "Price", "Line Amount"])
    for row in Credit_Memo_Lines_df.iterrows():
        row_Series = Series(row[1])
        Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Invoice_Line")

        # Assign Values to JSON
        Current_line_json["line_item_id"] = row_Series["line_item_id"]
        Current_line_json["article_id"]["supplier_aid"] = row_Series["supplier_aid"]
        Current_line_json["article_id"]["description_short"] = row_Series["description_short"]

        Current_line_json["quantity"] = row_Series["quantity"]
        Current_line_json["order_unit"] = row_Series["order_unit"]

        Current_line_json["article_price"]["price_amount"] = row_Series["price_amount"]
        Current_line_json["article_price"]["price_line_amount"] = row_Series["price_line_amount"]

        Current_line_json["order_reference"]["order_id"] = row_Series["order_id"]
        Current_line_json["order_reference"]["line_item_id"] = row_Series["order_line_item_id"]
        Current_line_json["order_reference"]["order_date"] = row_Series["order_date"]
        
        Current_line_json["supplier_order_reference"]["supplier_order_id"] = row_Series["supplier_order_id"]
        Current_line_json["supplier_order_reference"]["supplier_order_item_id"] = row_Series["supplier_order_item_id"]

        Current_line_json["delivery_reference"]["delivery_note_id"] = row_Series["delivery_note_id"]
        Current_line_json["delivery_reference"]["line_item_id"] = row_Series["delivery_line_item_id"]

        Current_line_json["tariff_number"] = row_Series["tariff_number"]
        Current_line_json["remarks"]["origin"] = row_Series["origin"]
        Current_line_json["remarks"]["plant"] = row_Series["plant"]

        PO_Invoice_Lines.append(Current_line_json)
        del Current_line_json

        # Assign Values to PDF PO_Invoice_Table_Data_list
        Line_Data_List = []
        Line_Data_List.append(str(row_Series["supplier_aid"]))
        Line_Data_List.append(str(row_Series["description_short"]))
        Line_Data_List.append(str(row_Series["quantity"]))
        Line_Data_List.append(str(row_Series["price_amount"]))
        Line_Data_List.append(str(row_Series["price_line_amount"]))
        Table_Data.append(Line_Data_List)

    # Add Lines to proper Delivery Header
    PRO_Credit_Memo["invoice"]["invoice_item_list"] = PO_Invoice_Lines
    PRO_Credit_Memo["invoice"]["invoice_summary"]["total_item_num"] = Total_Invoice_Lines_Count
    PRO_Credit_Memo["invoice"]["invoice_summary"]["total_amount"] = Total_invoice_Amount
        
    return PRO_Credit_Memo, Table_Data

