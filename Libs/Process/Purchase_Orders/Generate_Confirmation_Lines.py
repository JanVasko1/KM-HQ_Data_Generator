# Import Libraries
import random
from pandas import DataFrame, Series

import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

from customtkinter import CTk, CTkFrame, StringVar

def Generate_PO_CON_Lines(Settings: dict, 
                            Configuration: dict|None, 
                            window: CTk|None,
                            Purchase_Order: str,
                            Purchase_Lines_df: DataFrame, 
                            HQ_Item_Transport_Register_df: DataFrame,
                            Items_df: DataFrame, 
                            Items_Substitutions_df: DataFrame, 
                            Items_Connected_Items_df: DataFrame, 
                            Items_Price_List_Detail_df: DataFrame, 
                            Items_Distr_Status_df: DataFrame,
                            UoM_df: DataFrame,
                            PO_Confirmation_Currency: str,
                            GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Confirmed_Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group", "cancelled", "Exported_Line_No", "Distribution_Status_NUS", "Blocked_for_Purchase", "price_currency"]
    Confirmed_Lines_df = DataFrame(columns=Confirmed_Lines_df_Columns)

    Price_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Prices"]["Method"]

    UoM_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Method"]
    Fixed_UoM = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Fixed_Options"]["Fix_UoM"]

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

    Face_Sheet_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Number"]
    Face_Sheet_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Description"]
    Face_Sheet_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["QTY_per_Machine"]
    Face_Sheet_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Price"]
    Free_Face_Sheet_Number = ""
    Free_Face_Sheet_Description = ""
    Free_Face_Sheet_Quantity = ""
    Free_Face_Sheet_Price = ""

    Line_Flags_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Use"]
    Line_Flags_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Method"]
    Line_Flag_Label_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Labels_always"]
    Line_Flag_Item_EOL_Finished = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Item_EOL_Finish"]
    Line_Flag_Always_Substitute = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Always_Substitute"]
    
    # Filter Dataframes by Purchase Order
    mask_HQ_Item_Tr_Reg = HQ_Item_Transport_Register_df["Document_No"] == Purchase_Order
    HQ_Item_Tr_Reg_Filtered = DataFrame(HQ_Item_Transport_Register_df[mask_HQ_Item_Tr_Reg])

    mask_Machines = Items_df["Material_Group_NUS"] == "0100"
    Machines_df = DataFrame(Items_df[mask_Machines])

    mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
    Purchase_Lines_df_Filtered = DataFrame(Purchase_Lines_df[mask_Purch_Line])

    # --------------------------------------------- Items Definition --------------------------------------------- #
    Exported_Items_list = HQ_Item_Tr_Reg_Filtered["Item_No"].to_list()
    Confirmed_Lines_df["buyer_aid"] = Exported_Items_list
    Confirmed_Lines_df["supplier_aid"] = Exported_Items_list
    Confirmed_Lines_df["Exported_Line_No"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Exported_Line_No", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Item_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Exported_Line_No"), axis=1)
    Confirmed_Lines_df["quantity"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="quantity", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Item_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Quantity"), axis=1)
    Confirmed_Lines_df["ordered_quantity"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="ordered_quantity", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Item_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Quantity"), axis=1)
    Confirmed_Lines_df["item_category"] = "YN01"
    Confirmed_Lines_df["price_currency"] = PO_Confirmation_Currency     # Because of Invoice Generation
    Confirmed_Lines_df["discontinued"] = False
    Confirmed_Lines_df["set"] = False
    Confirmed_Lines_df["bom"] = False
    Confirmed_Lines_df["bom_with_delivery_group"] = False
    Confirmed_Lines_df["cancelled"] = False

    # Number of Lines in Document
    Lines_No = len(Confirmed_Lines_df)

    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        if Price_Method == "Price List":
            Confirmed_Lines_df["price_amount"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Asset_No"], Search_df=Items_Price_List_Detail_df, Search_Column="DirectUnitCost"), axis=1)
        elif Price_Method == "Purchase Line":
            Confirmed_Lines_df["price_amount"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Direct_Unit_Cost"), axis=1)
        elif Price_Method == "Prompt":
            if GUI == True:
                def Select_PO_Prices(Frame_Body: CTkFrame, Lines_No: int):
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

                    Confirmed_Lines_df["price_amount"] = Price_list
                    PO_Price_Variable.set(value="Selected")
                    PO_Price_Window.destroy()

                # TopUp Window
                PO_Price_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Price_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Price_Window_geometry[1] //2
                PO_Price_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Price for Items Items.", max_width=PO_Price_Window_geometry[0], max_height=PO_Price_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_Price_Window, Name="Select Price for Items Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Price for each Item of Confirmation.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Prices
                for row in Confirmed_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["buyer_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal", Validation="Float") 
                    PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PO_Fields_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_Price_Window_geometry[1]:
                    content_height = PO_Price_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_Price_Variable = StringVar(master=PO_Price_Window, value="", name="PO_Price_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_Prices(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Price selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_Price_Variable)
            else:
                pass
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items price Method selected: {Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                pass
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Unit of Measure --------------------------------------------- #
    if Can_Continue == True:
        if UoM_Method == "Fixed":
            Confirmed_Lines_df["order_unit"] = Fixed_UoM
        elif UoM_Method == "Purchase Line":
            Confirmed_Lines_df["PO_UoM"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="PO_UoM", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Unit_of_Measure_Code"), axis=1)
            Confirmed_Lines_df["order_unit"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit", Compare_Column_df1=["PO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
            Confirmed_Lines_df.drop(labels=["PO_UoM"], inplace=True, axis=1)
        elif UoM_Method == "HQ Item Transport Export":
            Confirmed_Lines_df["PO_UoM"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="PO_UoM", Compare_Column_df1=["buyer_aid", "Exported_Line_No"], Compare_Column_df2=["Item_No", "Exported_Line_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Unit_of_Measure"), axis=1)
            Confirmed_Lines_df["order_unit"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit", Compare_Column_df1=["PO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
            Confirmed_Lines_df.drop(labels=["PO_UoM"], inplace=True, axis=1)
        elif UoM_Method == "Prompt":
            if GUI == True:
                def Select_UoM(Frame_Body: CTkFrame, Lines_No: int):
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

                    Confirmed_Lines_df["order_unit"] = UoM_list
                    PO_UoM_Variable.set(value="Selected")
                    PO_UoM_Window.destroy()

                # TopUp Window
                PO_UoM_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_UoM_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_UoM_Window_geometry[1] //2
                PO_UoM_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Unit of Measure for Items Items.", max_width=PO_UoM_Window_geometry[0], max_height=PO_UoM_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_UoM_Window, Name="Select Unit of Measure for Items Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Unit of Measure for each Item of Confirmation.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Unit of Measure
                for row in Confirmed_Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["buyer_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal") 
                    PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PO_Fields_Frame_Var.configure(placeholder_text="Manual Unit of Measure", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_UoM_Window_geometry[1]:
                    content_height = PO_UoM_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_UoM_Variable = StringVar(master=PO_UoM_Window, value="", name="PO_UoM_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_UoM(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Unit of Measure selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_UoM_Variable)
            else:
                pass
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items Unit of Measure Method selected: {UoM_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                pass
            Can_Continue = False
    else:
        pass

    # -------------------- BEU Set -------------------- #
    # Not existing Case now - discontinued

    # -------------------- Free of Charge -------------------- #
    # Find Machine in Confirmed_Lines_df
    if Machines_df.empty:
        pass
    else:
        # Prepare data
        Machines_list = Machines_df["No"].to_list()
        Machines_HQ_Item_Tr_df = Pandas_Functions.Dataframe_Filter_on_Multiple(Filter_df=HQ_Item_Tr_Reg_Filtered, Filter_Column="Item_No", Filter_Values=Machines_list)
        Machines_HQ_Item_Tr_df_desc = Machines_HQ_Item_Tr_df.sort_index(ascending=False)

        # Loop Over Machines 
        for machine_row in Machines_HQ_Item_Tr_df_desc.iterrows():
            Machine_Index = machine_row[0]
            Insert_Index = Machine_Index
            Machine_row_Series = Series(machine_row[1])
            Machine = Machine_row_Series["Item_No"]
            Machine_Exported_Line_No = str(Machine_row_Series["Exported_Line_No"])
            Machine_Quantity = Machine_row_Series["Quantity"]

            if Can_Continue == True:
                if Free_Method == "Fixed":
                    # Cable
                    if Cable_Number != "":
                        Free_Cable_Number = Cable_Number
                        Free_Cable_Description = Cable_Description
                        Free_Cable_Quantity = Cable_QTY_per_Machine * Machine_Quantity
                        Free_Cable_Price = Cable_Price
                        Free_Cable_Line_list = [0, Free_Cable_Number, "", Free_Cable_Description, Free_Cable_Quantity, "C62", Free_Cable_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, False, f"{Machine_Exported_Line_No}"]

                        # Add to Confirmed_Lines_df
                        Free_Cable_dict = dict(zip(Confirmed_Lines_df_Columns, Free_Cable_Line_list))
                        Insert_Index += 1
                        Confirmed_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Confirmed_Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Cable_dict)
                    else:
                        pass

                    # Documentation
                    if Documentation_Number != "":
                        Free_Documentation_Number = Documentation_Number
                        Free_Documentation_Description = Documentation_Description
                        Free_Documentation_Quantity = Documentation_QTY_per_Machine * Machine_Quantity
                        Free_Documentation_Price = Documentation_Price
                        Free_Documentation_Line_list = [0, Free_Documentation_Number, "", Free_Documentation_Description, Free_Documentation_Quantity, "C62", Free_Documentation_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, False, f"{Machine_Exported_Line_No}"]

                        # Add to Confirmed_Lines_df
                        Free_Documentation_dict = dict(zip(Confirmed_Lines_df_Columns, Free_Documentation_Line_list))
                        Insert_Index += 1
                        Confirmed_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Confirmed_Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Documentation_dict)
                    else:
                        pass

                    # FaceSheet
                    if Face_Sheet_Number != "":
                        Free_Face_Sheet_Number = Face_Sheet_Number
                        Free_Face_Sheet_Description = Face_Sheet_Description
                        Free_Face_Sheet_Quantity = Face_Sheet_QTY_per_Machine * Machine_Quantity
                        Free_Face_Sheet_Price = Face_Sheet_Price
                        Free_Face_Sheet_Line_list = [0, Free_Face_Sheet_Number, "", Free_Face_Sheet_Description, Free_Face_Sheet_Quantity, "C62", Free_Face_Sheet_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, False, f"{Machine_Exported_Line_No}"]

                        # Add to Confirmed_Lines_df
                        Free_Face_Sheet_dict = dict(zip(Confirmed_Lines_df_Columns, Free_Face_Sheet_Line_list))
                        Insert_Index += 1
                        Confirmed_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Confirmed_Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Face_Sheet_dict)
                    else:
                        pass

                elif Free_Method == "Connected Items":
                    Connected_Items_mask1 = Items_Connected_Items_df["Main_Item_No"] == Machine
                    Connected_Items_mask2 = Items_Connected_Items_df["Connection_Type"] == "Free of Charge"
                    Connected_Items_Filtered = DataFrame(Items_Connected_Items_df[Connected_Items_mask1 & Connected_Items_mask2])

                    for Connected_Free_row in Connected_Items_Filtered.iterrows():
                        Free_Item_row_Series = Series(Connected_Free_row[1])
                        Free_Item_No = Free_Item_row_Series["No"]
                        Free_Item_Quantity = int(Free_Item_row_Series["Quantity"]) * Machine_Quantity
                        Free_Item_Line_list = [0, Free_Item_No, "", "", Free_Item_Quantity, "C62", 0, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, False, f"{Machine_Exported_Line_No}"]

                        # Add to Confirmed_Lines_df
                        Free_Item_dict = dict(zip(Confirmed_Lines_df_Columns, Free_Item_Line_list))
                        Insert_Index += 1
                        Confirmed_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Confirmed_Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Item_dict)

                elif Free_Method == "Prompt":
                    if GUI == True:
                        def Select_Free(Frame_Body: CTkFrame, Insert_Index: int):
                            global Confirmed_Lines_df
                            for i in range(2, 5):                           
                                No_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkentry"]
                                Description_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkentry2"]
                                Qty_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkentry3"]
                                Price_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkentry4"]

                                # Number
                                try:
                                    Value_Free_No = No_CTkEntry.get()
                                except:
                                    Value_Free_No = ""

                                if Value_Free_No != "":
                                    # Description
                                    try:
                                        Value_Free_Desc = Description_CTkEntry.get()
                                    except:
                                        Value_Free_Desc = ""

                                    # Qty
                                    try:
                                        Value_Free_Qty = int(Qty_CTkEntry.get())
                                    except:
                                        Value_Free_Qty = 0

                                    # Prices
                                    try:
                                        Value_Free_Price = float(Price_CTkEntry.get())
                                    except:
                                        Value_Free_Price = 0
                                    Free_Item_Line_list = [0, Value_Free_No, "", Value_Free_Desc, Value_Free_Qty, "C62", Value_Free_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, False, f"{Machine_Exported_Line_No}"]
                                    
                                    # Add to Confirmed_Lines_df
                                    Free_Item_dict = dict(zip(Confirmed_Lines_df_Columns, Free_Item_Line_list))
                                    Insert_Index += 1
                                    # BUG --> do not write to Global Confirmed_Lines_df somehow !!! -> zkusit nastavit prázdný dataframe hned po načtení knihoven (funguje u CPDI Delivery --> asi že hned pod Global je zapsano přiřazení do promněné)
                                    Confirmed_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Confirmed_Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Item_dict)
                                else:
                                    pass

                            PO_Free_Variable.set(value="Selected")
                            PO_Free_Window.destroy()

                        # TopUp Window
                        PO_Free_Window_geometry = (520, 230)
                        Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                        Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Free_Window_geometry[0] // 2
                        Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Free_Window_geometry[1] //2
                        PO_Free_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Free of Charge Items for: {Machine}.", max_width=PO_Free_Window_geometry[0], max_height=PO_Free_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                        # Frame - General
                        Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_Free_Window, Name=f"Select Free of Charge Items for: {Machine}.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip=f"To select proper Free of Charge Item for {Machine} of Confirmation.", GUI_Level_ID=3)
                        Frame_Main.configure(bg_color = "#000001", height=230)
                        Frame_Body = Frame_Main.children["!ctkframe2"]

                        Description = Elements_Groups.Get_Prompt_Free_Of_Charge_Description_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column")
                        Cable_Row = Elements_Groups.Get_Prompt_Free_Of_Charge_row(Settings=Settings, Configuration=Configuration, window=window,  Frame=Frame_Body, Field_Frame_Type="Double_Column", Label="Cable")
                        Documentation_Row = Elements_Groups.Get_Prompt_Free_Of_Charge_row(Settings=Settings, Configuration=Configuration, window=window,  Frame=Frame_Body, Field_Frame_Type="Double_Column", Label="Documentation")
                        FaceSheet_Row = Elements_Groups.Get_Prompt_Free_Of_Charge_row(Settings=Settings, Configuration=Configuration, window=window,  Frame=Frame_Body, Field_Frame_Type="Double_Column", Label="Face Sheet")

                        # Buttons
                        PO_Free_Variable = StringVar(master=PO_Free_Window, value="", name="PO_Free_Variable")
                        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                        Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Free(Frame_Body=Frame_Body, Insert_Index=Insert_Index))
                        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Free of charge Selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                        Button_Confirm_Var.wait_variable(PO_Free_Variable)
                    else:
                        pass
                else:
                    if GUI == True:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Free of Charge Method selected: {Free_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    else:
                        pass
                    Can_Continue = False
            else:
                pass

    # Update after assigning Free of Charge
    Confirmed_Lines_df["description_long"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_long", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)

    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    Confirmed_Lines_df["price_line_amount"] = Confirmed_Lines_df["quantity"]*Confirmed_Lines_df["price_amount"]

    Total_Line_Amount = float(Confirmed_Lines_df["price_line_amount"].sum(axis=0))

    # --------------------------------------------- Line Flags --------------------------------------------- #
    # -------- Before General Definition -------- #
    # Run this before generation as Prompt then can also show already marked Lines Flags
    # Label Always
    if Can_Continue == True:
        if Line_Flag_Label_Enabled == True:
            # Find Machines
            Confirmed_Lines_df["Material_Group_help"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Material_Group_help", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Material_Group_NUS"), axis=1)
            mask_Machines = Confirmed_Lines_df["Material_Group_help"] == "0100"
            Machines_df = DataFrame(Confirmed_Lines_df[mask_Machines])
            Machines_df = Machines_df.sort_index(ascending=False)
            Confirmed_Lines_df.drop(labels=["Material_Group_help"], inplace=True, axis=1)

            if Machines_df.empty:
                pass
            else:
                # Loop Over Machines 
                for machine_row in Machines_df.iterrows():
                    Machine_Index = machine_row[0]
                    Machine_row_Series = Series(machine_row[1])
                    Machine = Machine_row_Series["supplier_aid"]
                    Machine_Description = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Items_df, Search_Column="Description", Filter_Column="No", Filter_Value=Machine)
                    Machine_Exported_Line_No = str(Machine_row_Series["Exported_Line_No"])
                    Machine_Quantity = Machine_row_Series["quantity"]

                    Label_Number = f"Label{Machine}"
                    Label_Line_list = [0, Label_Number, Machine, Machine_Description, Machine_Quantity, "C62", 0, 0, "", "", Machine_Quantity, "", "ZST", False, False, True, False, False, f"{Machine_Exported_Line_No}"]

                    # Add to Confirmed_Lines_df
                    Label_dict = dict(zip(Confirmed_Lines_df_Columns, Label_Line_list))
                    Confirmed_Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Confirmed_Lines_df, Insert_At_index=Machine_Index, New_Row=Label_dict)
        else:
            pass
    else:
        pass

    # Finished for EOL Items (Distribution status set as blocked for Purchase)
    if Can_Continue == True:
        if Line_Flag_Item_EOL_Finished == True:
            Confirmed_Lines_df["Distribution_Status_NUS"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Distribution_Status_NUS", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Distribution_Status_NUS"), axis=1)
            Confirmed_Lines_df["Blocked_for_Purchase"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Blocked_for_Purchase", Compare_Column_df1=["Distribution_Status_NUS"], Compare_Column_df2=["Distribution_Status"], Search_df=Items_Distr_Status_df, Search_Column="Blocked_for_Purchase"), axis=1)
            conditions = [(Confirmed_Lines_df["Blocked_for_Purchase"] == True)]
            Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=conditions, Set_Column="item_category", Set_Value="TAPA")
            Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=conditions, Set_Column="discontinued", Set_Value=True)
            Confirmed_Lines_df.drop(labels=["Distribution_Status_NUS", "Blocked_for_Purchase"], inplace=True, axis=1)
        else:
            pass
    else:
        pass

    # Substitution
    if Can_Continue == True:
        if Line_Flag_Always_Substitute == True:
            Confirmed_Lines_df["Substitute_No"] = ""
            Confirmed_Lines_df["Substitute_No"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Substitute_No", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_Substitutions_df, Search_Column="Substitute_No"), axis=1)
            Confirmed_Lines_df.loc[Confirmed_Lines_df["Substitute_No"] != "", "supplier_aid"] = Confirmed_Lines_df["Substitute_No"]
            Confirmed_Lines_df.loc[Confirmed_Lines_df["Substitute_No"] != "", "discontinued"] = False
            Confirmed_Lines_df.drop(labels=["Substitute_No"], inplace=True, axis=1)
        else:
            pass
    else:
        pass

    # -------- Lines Flags General -------- #
    if Can_Continue == True:
        # If Use
        if Line_Flags_Enabled == True:
            if Line_Flags_Method == "Random Cancel":
                index_list = Confirmed_Lines_df.index.to_list()
                random_index = random.choice(seq=index_list)
                Confirmed_Lines_df.at[random_index, "cancelled"] = True
            elif Line_Flags_Method == "Random Finished":
                index_list = Confirmed_Lines_df.index.to_list()
                random_index = random.choice(seq=index_list)
                Confirmed_Lines_df.at[random_index, "item_category"] = "TAPA"
                Confirmed_Lines_df.at[random_index, "discontinued"] = True
                Confirmed_Lines_df.at[random_index, "cancelled"] = "No longer available"
            elif Line_Flags_Method == "Prompt":
                if GUI == True:
                    Lines_No = len(Confirmed_Lines_df) 
                    def Select_Flags(Frame_Body: CTkFrame, Lines_No: int, Confirmed_Lines_df: DataFrame):
                        Confirmed_Lines_df_index = 0
                        for i in range(2, Lines_No + 2):    
                            Substitution_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkcheckbox"]
                            Substitution_Item_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkentry"]
                            Cancel_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkcheckbox2"]
                            Finished_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe2"].children["!ctkcheckbox3"]
                            
                            # Substitution
                            Use_Substitution = Substitution_CTkEntry.get()
                            if Use_Substitution == True:
                                Sub_Item_No = Substitution_Item_CTkEntry.get()
                                if Sub_Item_No != "":
                                    Confirmed_Lines_df.at[Confirmed_Lines_df_index, "supplier_aid"] = Sub_Item_No
                                else:
                                    # Changed form Substituted into Non-Substituted
                                    Confirmed_Lines_df.at[Confirmed_Lines_df_index, "supplier_aid"] = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["buyer_aid"] 
                                    Confirmed_Lines_df.at[Confirmed_Lines_df_index, "item_category"] = "YN01"
                            elif Use_Substitution == False:
                                # Changed form Substituted into Non-Substituted
                                Confirmed_Lines_df.at[Confirmed_Lines_df_index, "supplier_aid"] = Confirmed_Lines_df.iloc[Confirmed_Lines_df_index]["buyer_aid"] 
                                Confirmed_Lines_df.at[Confirmed_Lines_df_index, "item_category"] = "YN01"
                            else:
                                pass

                            # Cancel
                            Use_Cancel = Cancel_CTkEntry.get()
                            if Use_Cancel == True:
                                Confirmed_Lines_df.at[Confirmed_Lines_df_index, "cancelled"] = True
                            else:
                                pass

                            # Finished
                            Use_Finished = Finished_CTkEntry.get()
                            if Use_Finished == True:
                                Confirmed_Lines_df.at[Confirmed_Lines_df_index, "discontinued"] = True
                            else:
                                pass

                            Confirmed_Lines_df_index += 1

                        PO_Flags_Variable.set(value="Selected")
                        PO_Flags_Window.destroy()


                    # TopUp Window
                    PO_Flags_Window_geometry = (520, 500)
                    Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                    Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Flags_Window_geometry[0] //2
                    Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Flags_Window_geometry[1] //2
                    PO_Flags_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Line Flags of Items.", max_width=PO_Flags_Window_geometry[0], max_height=PO_Flags_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                    # Frame - General
                    Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_Flags_Window, Name=f"Select Line Flags of Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip=f"To select proper Line Flags Items in Confirmation.", GUI_Level_ID=3)
                    Frame_Body = Frame_Main.children["!ctkframe2"]

                    Description = Elements_Groups.Get_Prompt_Line_Flags_Description_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Double_Column")

                    # Lines Flags
                    for row in Confirmed_Lines_df.iterrows():
                        # Dataframe
                        row_Series = Series(row[1])
                        Item_No = row_Series["supplier_aid"]
                        Item_Line = row_Series["Exported_Line_No"]

                        # Analyze Substitution
                        Item_Bought = row_Series["buyer_aid"]
                        Item_Label = row_Series["bom"]
                        if (Item_Bought != Item_No) and (Item_Label == False) and (Item_Bought != ""):
                            Item_Substituted = True

                            # Items switched because of correct show on popup page
                            Item_No_Substituted = Item_No
                            Item_No = Item_Bought
                        else:
                            Item_Substituted = False
                            Item_No_Substituted = ""

                        # Analyze Finished
                        Item_Finished = row_Series["discontinued"]
                        
                        Item_Row = Elements_Groups.Get_Prompt_Line_Flags_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Double_Column", Label=f"{Item_Line} - {Item_No}", Item_Substituted=Item_Substituted, Item_No_Substituted=Item_No_Substituted, Item_Finished=Item_Finished)
                    
                    # Dynamic Content height
                    content_row_count = len(Frame_Body.winfo_children())
                    content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                    if content_height > PO_Flags_Window_geometry[1]:
                        content_height = PO_Flags_Window_geometry[1]
                    Frame_Main.configure(bg_color = "#000001", height=content_height)

                    # Buttons
                    PO_Flags_Variable = StringVar(master=PO_Flags_Window, value="", name="PO_Flags_Variable")
                    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                    Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                    Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Flags(Frame_Body=Frame_Body, Lines_No=Lines_No, Confirmed_Lines_df=Confirmed_Lines_df))
                    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Flags of charge Selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                    Button_Confirm_Var.wait_variable(PO_Flags_Variable)
                else:
                    pass
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Line Flags Charge Method selected: {Line_Flags_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    pass
                Can_Continue = False
        else:
            pass
    else:
        pass

    # Update after assigning Possible Substitution changes
    Confirmed_Lines_df["description_long"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_long", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)

    # Check if Machine is Canceled / Finished --> to do it with FOCHs too
    # TODO --> when Machine marked --> free of charge Items must be deleted according to Exported_Line_No

    # --------------------------------------------- Solution Items --------------------------------------------- #
    # Set: "item_category": "TAS" --> cannot create PreAdvice and Delivery for that Item marked this way

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # line_item_id
    Confirmed_Lines_df["Exported_Line_No"] = Confirmed_Lines_df["Exported_Line_No"].astype(int)
    Confirmed_Lines_df["line_item_id"] = Confirmed_Lines_df["Exported_Line_No"] // 100

    # supplier_order_item_id
    Lines_No = len(Confirmed_Lines_df)
    line_item_id_list= []
    for i in range(1, Lines_No + 1):
        line_item_id = i * 10
        line_item_id_list.append((f"{line_item_id :06d}"))
    Confirmed_Lines_df["supplier_order_item_id"] = line_item_id_list

    # Round Values
    Confirmed_Lines_df["quantity"] = Confirmed_Lines_df["quantity"].round(2)
    Confirmed_Lines_df["ordered_quantity"] = Confirmed_Lines_df["ordered_quantity"].round(2)
    Confirmed_Lines_df["price_amount"] = Confirmed_Lines_df["price_amount"].round(2)
    Confirmed_Lines_df["price_line_amount"] = Confirmed_Lines_df["price_line_amount"].round(2)

    # Prepare Json for each line of DataFrame
    PO_Confirmation_Lines = []
    for row in Confirmed_Lines_df.iterrows():
        row_Series = Series(row[1])
        Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Confirmation_Line")

        # Assign Values
        Current_line_json["line_item_id"] = row_Series["line_item_id"]
        Current_line_json["article_id"]["supplier_aid"] = row_Series["supplier_aid"]
        Current_line_json["article_id"]["buyer_aid"] = row_Series["buyer_aid"]
        Current_line_json["article_id"]["description_long"] = row_Series["description_long"]

        Current_line_json["quantity"] = row_Series["quantity"]
        Current_line_json["order_unit"] = row_Series["order_unit"]

        Current_line_json["article_price"]["price_amount"] = row_Series["price_amount"]
        Current_line_json["article_price"]["price_line_amount"] = row_Series["price_line_amount"]

        Current_line_json["remarks"]["ordered_quantity"] = row_Series["ordered_quantity"]
        Current_line_json["remarks"]["supplier_order_item_id"] = row_Series["supplier_order_item_id"]
        Current_line_json["remarks"]["item_category"] = row_Series["item_category"]
        Current_line_json["remarks"]["discontinued"] = row_Series["discontinued"]
        Current_line_json["remarks"]["set"] = row_Series["set"]
        Current_line_json["remarks"]["bom"] = row_Series["bom"]
        Current_line_json["remarks"]["bom_with_delivery_group"] = row_Series["bom_with_delivery_group"]
        Current_line_json["remarks"]["cancelled"] = row_Series["cancelled"]

        PO_Confirmation_Lines.append(Current_line_json)
        del Current_line_json

    Lines_No = len(Confirmed_Lines_df)
    return Confirmed_Lines_df, PO_Confirmation_Lines, Total_Line_Amount, Lines_No