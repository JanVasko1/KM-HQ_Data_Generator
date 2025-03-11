# Import Libraries
import random
from pandas import DataFrame, Series

import Libs.GUI.Elements as Elements
import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements_Groups as Elements_Groups

from customtkinter import CTk, CTkFrame, StringVar

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
    Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group", "Exported_Line_No"]
    Lines_df = DataFrame(columns=Lines_df_Columns)

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

    Others_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["Number"]
    Others_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["Description"]
    Others_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["QTY_per_Machine"]
    Others_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Others"]["Price"]
    Free_Others_Number = ""
    Free_Others_Description = ""
    Free_Others_Quantity = ""
    Free_Others_Price = ""

    Line_Flags_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Use"]
    Line_Flags_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Method"]
    Line_Flag_Label_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Labels_always"]
    Line_Flag_Item_EOL_Finished = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Item_EOL_Finish"]
    

    # Filter Dataframes by Purchase Order
    mask_HQ_Item_Tr_Reg = HQ_Item_Transport_Register_df["Document_No"] == Purchase_Order
    HQ_Item_Tr_Reg_Filtered = HQ_Item_Transport_Register_df[mask_HQ_Item_Tr_Reg]    

    mask_Machines = Items_df["Material_Group_NUS"] == "0100"
    Machines_df = Items_df[mask_Machines]  

    mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
    Purchase_Lines_df_Filtered = Purchase_Lines_df[mask_Purch_Line] 
    # --------------------------------------------- Items Definition --------------------------------------------- #
    Exported_Items_list = HQ_Item_Tr_Reg_Filtered["Item_No"].to_list()
    Lines_df["buyer_aid"] = Exported_Items_list
    Lines_df["supplier_aid"] = Exported_Items_list
    Lines_df["Exported_Line_No"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="Exported_Line_No", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Item_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Exported_Line_No"), axis=1)
    Lines_df["quantity"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="quantity", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Item_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Quantity"), axis=1)
    Lines_df["ordered_quantity"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="ordered_quantity", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Item_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Quantity"), axis=1)
    Lines_df["description_long"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="description_long", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df, Search_Column="Description"), axis=1)
    Lines_df["discontinued"] = False
    Lines_df["set"] = False
    Lines_df["bom"] = False
    Lines_df["bom_with_delivery_group"] = False

    # Number of Lines in Document
    Lines_No = len(Lines_df)

    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        if Price_Method == "Price List":
            Lines_df["price_amount"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["Asset_No"], Search_df=Items_Price_List_Detail_df, Search_Column="DirectUnitCost"), axis=1)
        elif Price_Method == "Purchase Line":
            Lines_df["price_amount"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="price_amount", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Direct_Unit_Cost"), axis=1)
        elif Price_Method == "Prompt":
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
                    Price_list.append(Value_Price)

                Lines_df["price_amount"] = Price_list
                PO_Price_Variable.set(value="Selected")
                PO_Price_Window.destroy()

            # TopUp Window
            PO_Price_Window_geometry = (300, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Price_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Price_Window_geometry[1] //2
            PO_Price_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Select Price for Items Items.", width=PO_Price_Window_geometry[0], height=PO_Price_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_Price_Window, Name="Select BackBone Billing Qty for selected Items.", Additional_Text="", Widget_size="Half_size", Widget_Label_Tooltip="To select proper Qty for each Item of Confirmation.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            # Vendor_Service_ID
            for row in Lines_df.iterrows():
                # Dataframe
                row_Series = Series(row[1])
                Item_No = row_Series["buyer_aid"]

                # Fields
                Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal", Validation="Float") 
                PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                PO_Fields_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")
                
            # Buttons
            PO_Price_Variable = StringVar(master=PO_Price_Window, value="", name="PO_Price_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_Prices(Frame_Body=Frame_Body, Lines_No=Lines_No))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Price selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_Price_Variable)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Items price Method selected: {Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Unit of Measure --------------------------------------------- #
    if Can_Continue == True:
        if UoM_Method == "Fixed":
            Lines_df["order_unit"] = Fixed_UoM
        elif UoM_Method == "Purchase Line":
            Lines_df["PO_UoM"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="PO_UoM", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Unit_of_Measure_Code"), axis=1)
            Lines_df["order_unit"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="order_unit", Compare_Column_df1=["PO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
            Lines_df.drop(labels=["PO_UoM"], inplace=True, axis=1)
        elif UoM_Method == "HQ Item Transport Export":
            Lines_df["PO_UoM"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="PO_UoM", Compare_Column_df1=["buyer_aid", "Exported_Line_No"], Compare_Column_df2=["Item_No", "Exported_Line_No"], Search_df=HQ_Item_Tr_Reg_Filtered, Search_Column="Unit_of_Measure"), axis=1)
            Lines_df["order_unit"] = Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value(row=row, Fill_Column="order_unit", Compare_Column_df1=["PO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
            Lines_df.drop(labels=["PO_UoM"], inplace=True, axis=1)
        elif UoM_Method == "Prompt":
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

                Lines_df["order_unit"] = UoM_list
                PO_UoM_Variable.set(value="Selected")
                PO_UoM_Window.destroy()

            # TopUp Window
            PO_UoM_Window_geometry = (300, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_UoM_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_UoM_Window_geometry[1] //2
            PO_UoM_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Select Unit of Measure for Items Items.", width=PO_UoM_Window_geometry[0], height=PO_UoM_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_UoM_Window, Name="Select Unit of Measure for Items Items.", Additional_Text="", Widget_size="Half_size", Widget_Label_Tooltip="To select proper Unit of Measure for each Item of Confirmation.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            # Vendor_Service_ID
            for row in Lines_df.iterrows():
                # Dataframe
                row_Series = Series(row[1])
                Item_No = row_Series["buyer_aid"]

                # Fields
                Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal") 
                PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                PO_Fields_Frame_Var.configure(placeholder_text="Manual Unit of Measure", placeholder_text_color="#949A9F")
                
            # Buttons
            PO_UoM_Variable = StringVar(master=PO_UoM_Window, value="", name="PO_UoM_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_UoM(Frame_Body=Frame_Body, Lines_No=Lines_No))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Confirmation Unit of Measure selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_UoM_Variable)

        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Items Unit of Measure Method selected: {UoM_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
    else:
        pass

    print(Lines_df)

    # -------------------- BEU Set -------------------- #
    # Not existing Case now - discontinued

    # -------------------- Free of Charge -------------------- #
    # Find Machine in Lines_df
    print(Machines_df)
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
            Machine_Exported_Line_No = str(Machine_row_Series["Exported_Line_No"])
            Machine_Quantity = Machine_row_Series["Quantity"]

            # TODO --> prozkoumat významy "item_category" které příjdou z BEU aby byli správně k jednotlivým Free of Charge

            if Can_Continue == True:
                if Free_Method == "Fixed":
                    # Cable
                    if Cable_Number != "":
                        Free_Cable_Number = Cable_Number
                        Free_Cable_Description = Cable_Description
                        Free_Cable_Quantity = Cable_QTY_per_Machine * Machine_Quantity
                        Free_Cable_Price = Cable_Price
                        Free_Cable_Line_list = [0, Free_Cable_Number, "", Free_Cable_Description, Free_Cable_Quantity, "C62", Free_Cable_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, f"{Machine_Exported_Line_No}"]

                        Free_Cable_dict = dict(zip(Lines_df_Columns, Free_Cable_Line_list))
                        Insert_Index += 1
                        Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Cable_dict)
                    else:
                        pass

                    # Documentation
                    if Documentation_Number != "":
                        Free_Documentation_Number = Documentation_Number
                        Free_Documentation_Description = Documentation_Description
                        Free_Documentation_Quantity = Documentation_QTY_per_Machine * Machine_Quantity
                        Free_Documentation_Price = Documentation_Price
                        Free_Documentation_Line_list = [0, Free_Documentation_Number, "", Free_Documentation_Description, Free_Documentation_Quantity, "C62", Free_Documentation_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, f"{Machine_Exported_Line_No}"]

                        Free_Documentation_dict = dict(zip(Lines_df_Columns, Free_Documentation_Line_list))
                        Insert_Index += 1
                        Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Documentation_dict)
                    else:
                        pass

                    # Other
                    if Others_Number != "":
                        Free_Others_Number = Others_Number
                        Free_Others_Description = Others_Description
                        Free_Others_Quantity = Others_QTY_per_Machine * Machine_Quantity
                        Free_Others_Price = Others_Price
                        Free_Others_Line_list = [0, Free_Others_Number, "", Free_Others_Description, Free_Others_Quantity, "C62", Free_Others_Price, 0, "", "", Machine_Quantity, "", "YNF1", False, False, False, False, f"{Machine_Exported_Line_No}"]

                        Free_Others_dict = dict(zip(Lines_df_Columns, Free_Others_Line_list))
                        Insert_Index += 1
                        Lines_df = Pandas_Functions.Dataframe_Insert_Row_at_position(Insert_DataFrame=Lines_df, Insert_At_index=Insert_Index, New_Row=Free_Others_dict)
                    else:
                        pass

                elif Free_Method == "Connected Items":
                    # Connected Items - Free of Charge
                    pass
                elif Free_Method == "Prompt":
                    pass
                else:
                    Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Free of Charge Method selected: {Free_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    Can_Continue = False
            else:
                pass
   
    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    Lines_df["price_line_amount"] = Lines_df["quantity"]*Lines_df["price_amount"]

    Total_Line_Amount = float(Lines_df["price_line_amount"].sum(axis=0))

    print(Lines_df)

    # --------------------------------------------- Line Flags --------------------------------------------- #
    if Can_Continue == True:
        # If Use
        if Line_Flags_Enabled == True:
            if Line_Flags_Method == "Random Cancel":
                # TODO 
                pass
            elif Line_Flags_Method == "Random Finished":
                # TODO 
                pass
            elif Line_Flags_Method == "Prompt":
                # TODO 
                pass
            else:
                Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Free of Charge Method selected: {Free_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                Can_Continue = False
        else:
            pass
    else:
        pass
    
    # After General Definition
    # Label Always
    # TODO --> asi nastavit "bom = True" a ""item_category": "ZST""

    # Finished for EOL Items

    
    # --------------------------------------------- Apply Header information --------------------------------------------- #


    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # TODO -- převést Exported_Line_No na supplier_order_item_id

    # Delete unnecessary columns
    Lines_df.drop(labels=["Exported_Line_No"], inplace=True, axis=1)
