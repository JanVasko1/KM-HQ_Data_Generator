# Import Libraries
import random
from pandas import DataFrame, Series

import Libs.Pandas_Functions as Pandas_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

from customtkinter import CTk, CTkFrame, StringVar

def Generate_Invoice_Lines(Settings: dict, Configuration: dict, window: CTk, Purchase_Order: str, Purchase_Lines_df: DataFrame, PO_Invoice_Number_list: list, PO_Invoices: list, PO_Delivery_Number_list: list, Delivery_Lines_df: DataFrame, Confirmed_Lines_df: DataFrame, Items_df: DataFrame, Items_Price_List_Detail_df: DataFrame, Country_ISO_Code_list: list, Tariff_Number_list: list):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Invoice_Lines_df_columns = ["Invoice_No", "line_item_id", "supplier_aid", "description_short", "quantity", "order_unit", "price_amount", "price_line_amount", "order_id", "order_line_item_id", "order_date", "supplier_order_id", "supplier_order_item_id", "delivery_note_id", "delivery_line_item_id", "tariff_number", "origin", "plant"]
    Invoice_Lines_df = DataFrame(columns=Invoice_Lines_df_columns)

    Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Method"]

    Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Method"]
    Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Plants_List"])
    Plants_List = []

    Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Method"]
    Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Method"]
    Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    # Filter Dataframes by Purchase Order
    mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
    Purchase_Lines_df_Filtered = DataFrame(Purchase_Lines_df[mask_Purch_Line])

    # --------------------------------------------- Data from Delivery_Lines_df --------------------------------------------- #
    # General
    supplier_aid_list = Delivery_Lines_df["supplier_aid"].to_list()
    quantity_list = Delivery_Lines_df["quantity"].to_list()
    order_unit_list = Delivery_Lines_df["order_unit"].to_list()
    
    # Purchase Line Information
    order_id_list = Delivery_Lines_df["order_id"].to_list()
    order_line_item_id_list = Delivery_Lines_df["order_ref_line_item_id"].to_list()
    order_date = Delivery_Lines_df["order_date"].to_list()

    # Confirmation Information
    supplier_order_id_list = Delivery_Lines_df["supplier_order_id"].to_list()
    supplier_order_item_id_list = Delivery_Lines_df["supplier_order_item_id"].to_list()

    # Delivery Information
    delivery_note_id_list = Delivery_Lines_df["Delivery_No"].to_list()
    delivery_line_item_id_list = Delivery_Lines_df["line_item_id"].to_list()
    
    # Apply Lists to DataFrame
    Invoice_Lines_df["supplier_aid"] = supplier_aid_list
    Invoice_Lines_df["quantity"] = quantity_list
    Invoice_Lines_df["order_unit"] = order_unit_list

    Invoice_Lines_df["order_id"] = order_id_list
    Invoice_Lines_df["order_line_item_id"] = order_line_item_id_list
    Invoice_Lines_df["order_date"] = order_date

    Invoice_Lines_df["supplier_order_id"] = supplier_order_id_list
    Invoice_Lines_df["supplier_order_item_id"] = supplier_order_item_id_list

    Invoice_Lines_df["delivery_note_id"] = delivery_note_id_list
    Invoice_Lines_df["delivery_line_item_id"] = delivery_line_item_id_list

    Invoice_Lines_df["description_short"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_short", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)

    # Assign Invoice_No according Delivery_No
    for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
        Delivery_conditions = [(Invoice_Lines_df["delivery_note_id"] == Delivery_Number)]
        Invoice_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Invoice_Lines_df, conditions=Delivery_conditions, Set_Column="Invoice_No", Set_Value=PO_Invoice_Number_list[Delivery_Index])

    # Number of Lines in Document
    Invoice_Count = Invoice_Lines_df.shape[0]

    # --------------------------------------------- Calculate Invoice Lines  --------------------------------------------- #
    for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
        mask_Invoice = Invoice_Lines_df["Invoice_No"] == Invoice_Number
        Invoice_Lines_df_Filtered = DataFrame(Invoice_Lines_df[mask_Invoice])

        Line_Counter = 10
        for row in Invoice_Lines_df_Filtered.iterrows():
            row_index = row[0]

            # Update line_item_id
            Invoice_line_item_id = str(f"{Line_Counter :06d}")
            Line_Counter += 10

            Invoice_Lines_df.at[row_index, "line_item_id"] = Invoice_line_item_id

    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        Invoice_Lines_df["price_amount"] = 0
        if Price_Method == "Price List":
            Invoice_Lines_df["price_amount"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["Asset_No"], Search_df=Items_Price_List_Detail_df, Search_Column="DirectUnitCost"), axis=1)
        elif Price_Method == "Purchase Line":
            Invoice_Lines_df["price_amount"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Direct_Unit_Cost"), axis=1)
        elif Price_Method == "From Confirmation":
            Invoice_Lines_df["price_amount"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["supplier_aid", "supplier_order_item_id"], Compare_Column_df2=["supplier_aid", "supplier_order_item_id"], Search_df=Confirmed_Lines_df, Search_Column="price_amount"), axis=1)
        elif Price_Method == "Prompt":
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                mask_Invoice = Invoice_Lines_df["Invoice_No"] == Invoice_Number
                Invoice_Lines_df_Filtered = DataFrame(Invoice_Lines_df[mask_Invoice])
                def Select_PO_INV_Price(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Invoice_Price_list = []
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
                        PO_Invoice_Price_list.append(str(Value_Price))

                    PO_Invoice_Price_list_joined = ";".join(PO_Invoice_Price_list)
                    PO_INV_Price_Variable.set(value=PO_Invoice_Price_list_joined)
                    PO_INV_Price_Window.destroy()

                # TopUp Window
                PO_INV_Price_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_INV_Price_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_INV_Price_Window_geometry[1] //2
                PO_INV_Price_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Price for: {Invoice_Number}.", max_width=PO_INV_Price_Window_geometry[0], max_height=PO_INV_Price_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_INV_Price_Window, Name=f"Select Price for: {Invoice_Number}.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Price for each Invoice..", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Lines_No = Invoice_Lines_df_Filtered.shape[0]
                for row in Invoice_Lines_df_Filtered.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal") 
                    PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PO_Fields_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_INV_Price_Window_geometry[1]:
                    content_height = PO_INV_Price_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_INV_Price_Variable = StringVar(master=PO_INV_Price_Window, value="", name="PO_INV_Price_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_INV_Price(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Price selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_INV_Price_Variable)
                Prices_List = PO_INV_Price_Variable.get().split(";")
                Prices_List = [float(element) for element in Prices_List]

                # Apply Prices
                Invoice_Lines_df_Filtered["price_amount"] = Prices_List
                Invoice_Lines_df["price_amount"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["Invoice_No", "supplier_aid", "line_item_id"], Compare_Column_df2=["Invoice_No", "supplier_aid", "line_item_id"], Search_df=Invoice_Lines_df_Filtered, Search_Column="price_amount"), axis=1)
                del Invoice_Lines_df_Filtered

        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items price Method selected: {Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    Invoice_Lines_df["price_line_amount"] = Invoice_Lines_df["quantity"]*Invoice_Lines_df["price_amount"]

    # --------------------------------------------- Plants --------------------------------------------- #
    if Can_Continue == True:
        if Inv_Plant_Method == "Fixed":
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                Plants_List.append(Inv_Fixed_Plant)
        elif Inv_Plant_Method == "Random":
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                Current_Plant = random.choice(Inv_Fixed_Plants_List)
                Plants_List.append(Current_Plant)
        elif Inv_Plant_Method == "From Delivery":
            pass
            # TODO --> finish 
        elif Inv_Plant_Method == "Empty":
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                Plants_List.append("")
        elif Inv_Plant_Method == "Prompt":
            def Select_PO_INV_Plant(Frame_Body: CTkFrame, Lines_No: int):
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
                PO_INV_Plant_Variable.set(value=Plant_list_joined)
                PO_INV_Plant_Window.destroy()

            # TopUp Window
            PO_INV_Plant_Window_geometry = (520, 500)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_INV_Plant_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_INV_Plant_Window_geometry[1] //2
            PO_INV_Plant_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Plant for selected Invoices.", max_width=PO_INV_Plant_Window_geometry[0], max_height=PO_INV_Plant_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_INV_Plant_Window, Name="Select Plant for selected Invoices.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Plant for each Invoice..", GUI_Level_ID=3)
            Frame_Body = Frame_Main.children["!ctkframe2"]

            # Plants
            Lines_No = len(PO_Invoice_Number_list)
            for Invoice_index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                # Fields
                Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Invoice_Number}", Field_Type="Input_OptionMenu") 
                Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Inv_Fixed_Plants_List, command=None, GUI_Level_ID=3)

            # Dynamic Content height
            content_row_count = len(Frame_Body.winfo_children())
            content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
            if content_height > PO_INV_Plant_Window_geometry[1]:
                content_height = PO_INV_Plant_Window_geometry[1]
            Frame_Main.configure(bg_color = "#000001", height=content_height)

            # Buttons
            PO_INV_Plant_Variable = StringVar(master=PO_INV_Plant_Window, value="", name="PO_INV_Plant_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_INV_Plant(Frame_Body=Frame_Body, Lines_No=Lines_No))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Plant selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_INV_Plant_Variable)
            Plants_List = PO_INV_Plant_Variable.get().split(";")
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Plants Method selected: {Inv_Plant_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    # Assign Plant according Invoice_No
    for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
        Invoice_conditions = [(Invoice_Lines_df["Invoice_No"] == Invoice_Number)]
        Invoice_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Invoice_Lines_df, conditions=Invoice_conditions, Set_Column="plant", Set_Value=Plants_List[Invoice_Index])

    # --------------------------------------------- Country of Origin --------------------------------------------- #
    if Can_Continue == True:
        if Count_Origin_Method == "Fixed":
            Invoice_Lines_df["origin"] = Fixed_Count_Origin
        elif Count_Origin_Method == "Random":
            Invoice_Lines_df["origin"] = Invoice_Lines_df.apply(lambda row: random.choice(Country_ISO_Code_list), axis=1)
        elif Count_Origin_Method == "Empty":
            Invoice_Lines_df["origin"] = ""
        elif Count_Origin_Method == "Prompt":
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                mask_Invoice = Invoice_Lines_df["Invoice_No"] == Invoice_Number
                Invoice_Lines_df_Filtered = DataFrame(Invoice_Lines_df[mask_Invoice])

                def Select_PO_INV_Country_Origin(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Invoice_Country_Origin_list = []
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
                        PO_Invoice_Country_Origin_list.append(Value_Country_Origin)

                    PO_Invoice_Country_Origin_list_joined = ";".join(PO_Invoice_Country_Origin_list)
                    PO_INV_Country_Origin_Variable.set(value=PO_Invoice_Country_Origin_list_joined)
                    PO_INV_Country_Origin_Window.destroy()

                # TopUp Window
                PO_INV_Country_Origin_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_INV_Country_Origin_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_INV_Country_Origin_Window_geometry[1] //2
                PO_INV_Country_Origin_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Country of Origin for: {Invoice_Number}.", max_width=PO_INV_Country_Origin_Window_geometry[0], max_height=PO_INV_Country_Origin_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_INV_Country_Origin_Window, Name=f"Select Country Origin for: {Invoice_Number}.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Country of Origin for each Invoice..", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Lines_No = Invoice_Lines_df_Filtered.shape[0]
                for row in Invoice_Lines_df_Filtered.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Country_ISO_Code_list, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_INV_Country_Origin_Window_geometry[1]:
                    content_height = PO_INV_Country_Origin_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_INV_Country_Origin_Variable = StringVar(master=PO_INV_Country_Origin_Window, value="", name="PO_INV_Country_Origin_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_INV_Country_Origin(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Country Origin selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_INV_Country_Origin_Variable)
                Country_Origins_List = PO_INV_Country_Origin_Variable.get().split(";")

                # Apply Country of Origin
                Invoice_Lines_df_Filtered["origin"] = Country_Origins_List
                Invoice_Lines_df["origin"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="origin", Compare_Column_df1=["Invoice_No", "supplier_aid", "line_item_id"], Compare_Column_df2=["Invoice_No", "supplier_aid", "line_item_id"], Search_df=Invoice_Lines_df_Filtered, Search_Column="origin"), axis=1)
                del Invoice_Lines_df_Filtered

        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Country of Origin  Method selected: {Count_Origin_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass
    
    # --------------------------------------------- Tariff --------------------------------------------- # 
    if Can_Continue == True:
        if Tariff_Method == "Fixed":
            Invoice_Lines_df["tariff_number"] = Fixed_Tariff
        elif Tariff_Method == "Random":
            Invoice_Lines_df["tariff_number"] = Invoice_Lines_df.apply(lambda row: random.choice(Tariff_Number_list), axis=1)
        elif Tariff_Method == "Empty":
            Invoice_Lines_df["tariff_number"] = ""
        elif Tariff_Method == "Prompt":
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                mask_Invoice = Invoice_Lines_df["Invoice_No"] == Invoice_Number
                Invoice_Lines_df_Filtered = DataFrame(Invoice_Lines_df[mask_Invoice])
                
                def Select_PO_INV_Tariff(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Invoice_Tariff_list = []
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
                        PO_Invoice_Tariff_list.append(Value_Tariff)

                    PO_Invoice_Tariff_list_joined = ";".join(PO_Invoice_Tariff_list)
                    PO_INV_Tariff_Variable.set(value=PO_Invoice_Tariff_list_joined)
                    PO_INV_Tariff_Window.destroy()

                # TopUp Window
                PO_INV_Tariff_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_INV_Tariff_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_INV_Tariff_Window_geometry[1] //2
                PO_INV_Tariff_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Tariff for: {Invoice_Number}.", max_width=PO_INV_Tariff_Window_geometry[0], max_height=PO_INV_Tariff_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_INV_Tariff_Window, Name=f"Select Tariff for: {Invoice_Number}.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Tariff for each Invoice..", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Lines_No = Invoice_Lines_df_Filtered.shape[0]
                for row in Invoice_Lines_df_Filtered.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=Tariff_Number_list, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_INV_Tariff_Window_geometry[1]:
                    content_height = PO_INV_Tariff_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_INV_Tariff_Variable = StringVar(master=PO_INV_Tariff_Window, value="", name="PO_INV_Tariff_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_INV_Tariff(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Tariff selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_INV_Tariff_Variable)
                Tariffs_List = PO_INV_Tariff_Variable.get().split(";")

                # Apply Tariff
                Invoice_Lines_df_Filtered["tariff_number"] = Tariffs_List
                Invoice_Lines_df["tariff_number"] = Invoice_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="tariff_number", Compare_Column_df1=["Invoice_No", "supplier_aid", "line_item_id"], Compare_Column_df2=["Invoice_No", "supplier_aid", "line_item_id"], Search_df=Invoice_Lines_df_Filtered, Search_Column="tariff_number"), axis=1)
                del Invoice_Lines_df_Filtered
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Tariff Method selected: {Tariff_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # Round Values
    Invoice_Lines_df["quantity"] = Invoice_Lines_df["quantity"].round(2)
    Invoice_Lines_df["price_amount"] = Invoice_Lines_df["price_amount"].round(2)
    Invoice_Lines_df["price_line_amount"] = Invoice_Lines_df["price_line_amount"].round(2)

    PO_Invoice_Table_Data_list = []
    for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
        mask_Invoice = Invoice_Lines_df["Invoice_No"] == Invoice_Number
        Invoice_Lines_df_Filtered = DataFrame(Invoice_Lines_df[mask_Invoice])

        # Invoice Total data preparation
        Total_Invoice_Lines_Count = len(Invoice_Lines_df_Filtered)
        Total_invoice_Amount = round(number=float(Invoice_Lines_df_Filtered["price_line_amount"].sum(axis=0)), ndigits=2)

        # Prepare Json for each line of DataFrame + PDF data
        PO_Invoice_Lines = []
        Table_Data = []
        Table_Data.append(["Item No", "Description", "Quantity", "Price", "Line Amount"])
        for row in Invoice_Lines_df_Filtered.iterrows():
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
        PO_Invoices[Invoice_Index]["invoice"]["invoice_item_list"] = PO_Invoice_Lines
        PO_Invoices[Invoice_Index]["invoice"]["invoice_summary"]["total_item_num"] = Total_Invoice_Lines_Count
        PO_Invoices[Invoice_Index]["invoice"]["invoice_summary"]["total_amount"] = Total_invoice_Amount
           
        # Add data to List of PDF Table Data for multiple PDFs
        PO_Invoice_Table_Data_list.append(Table_Data)

    return PO_Invoices, PO_Invoice_Table_Data_list

