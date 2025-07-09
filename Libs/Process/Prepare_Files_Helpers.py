# Import Libraries
from pandas import DataFrame, Series
from Libs.Azure.API_Error_Handler import APIError

import Libs.Pandas_Functions as Pandas_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

try:
    # Front-End Library
    from customtkinter import CTk, CTkFrame, StringVar
    import Libs.CustomTkinter_Functions as CustomTkinter_Functions
except:
    pass

# ---------------------------------------------------------- For Delivery ---------------------------------------------------------- #
def Update_Confirm_df_for_Delivery(Confirmed_Lines_df: DataFrame, Items_df: DataFrame) -> DataFrame:
    Confirmed_Lines_df["Material_Group_help"] = ""
    Confirmed_Lines_df["Material_Group_help"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Material_Group_help", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Material_Group_NUS"), axis=1)

    # Check if Machine is cancelled or Discontinued
    for row in Confirmed_Lines_df.iterrows():
        Confirmed_Lines_Index = row[0]
        Confirmed_Lines_Series = Series(row[1])
        
        Material_Group_help = Confirmed_Lines_Series["Material_Group_help"]

        if Material_Group_help == "0100":
            Canceled_Machine = Confirmed_Lines_Series["cancelled"]
            Discontinued_Machine = Confirmed_Lines_Series["discontinued"]

            if (Canceled_Machine == True) or (Discontinued_Machine == True):
                Machine_Exported_Line_No = Confirmed_Lines_Series["Exported_Line_No"]
                Exported_Line_No_conditions = [(Confirmed_Lines_df["Exported_Line_No"] == Machine_Exported_Line_No)]
                Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Exported_Line_No_conditions, Set_Column="cancelled", Set_Value=True)
            else:
                pass
        else:
            pass

    Confirmed_Lines_df.drop(labels=["Material_Group_help"], inplace=True, axis=1)

    # Filter Dataframe
    mask_Canceled_Lines = Confirmed_Lines_df["cancelled"] == False
    mask_Discontinued_Lines = Confirmed_Lines_df["discontinued"] == False
    mask_Label = Confirmed_Lines_df["bom"] == False
    Confirmed_Lines_df = DataFrame(Confirmed_Lines_df[mask_Canceled_Lines & mask_Discontinued_Lines & mask_Label])
    Confirmed_Lines_df.reset_index(drop=True, inplace=True)

    return Confirmed_Lines_df

def Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration: dict|None, window: CTk|None, headers: dict, tenant_id: str, NUS_version: str, NOC: str, Environment: str, Company: str, Document_Number: str, Document_Type: str, Document_Lines_df: DataFrame, Items_df: DataFrame, UoM_df: DataFrame, GUI: bool=True) -> DataFrame:
    import Libs.Downloader.NAV_OData_API as NAV_OData_API
    
    Confirmed_Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group", "cancelled", "Exported_Line_No", "PO_UoM"]
    Confirmed_Lines_df = DataFrame(columns=Confirmed_Lines_df_Columns)

    # HQ_Testing_HQ_Item_Transport_Register
    HQ_Confirmed_Lines_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Document_Number], Document_Type=Document_Type, Vendor_Document_Type="Confirmation", GUI=GUI)
    if HQ_Confirmed_Lines_df.empty:
        if GUI == True:
            if Document_Type == "Order":
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Confirmation for {Document_Number} during preparation of Delivery.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            elif Document_Type == "Return Order":
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Confirmation for {Document_Number} during preparation of Return Credit Memo.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                pass
        else:
            if Document_Type == "Order":
                raise APIError(message=f"It is not possible to download Confirmation for {Document_Number} during preparation of Delivery.", status_code=500, charset="utf-8")
            elif Document_Type == "Return Order":
                raise APIError(message=f"It is not possible to download Confirmation for {Document_Number} during preparation of Return Credit Memo.", status_code=500, charset="utf-8")
            else:
                pass
    else:
        PO_Confirmation_Number = HQ_Confirmed_Lines_df.iloc[0]["Vendor_Document_No"]

        # Preparation
        mask_Purch_Line = Document_Lines_df["Document_No"] == Document_Number
        Purchase_Lines_df_Filtered = DataFrame(Document_Lines_df[mask_Purch_Line])

        # Assing Data to Dataframe
        Exported_Items_list = HQ_Confirmed_Lines_df["Item_No"].to_list()
        Confirmed_Lines_df["supplier_aid"] = Exported_Items_list
        Confirmed_Lines_df["buyer_aid"] = Exported_Items_list
        Confirmed_Lines_df["Vendor_Document_No"] = HQ_Confirmed_Lines_df["Vendor_Document_No"].to_list()
        Confirmed_Lines_df["item_category"] = "YN01"
        Confirmed_Lines_df["price_currency"] = HQ_Confirmed_Lines_df["Currency_Code"].to_list()      # Because of Invoice Generation
        Confirmed_Lines_df["delivery_start_date"] = HQ_Confirmed_Lines_df["Order_Date"].to_list()
        Confirmed_Lines_df["discontinued"] = False
        Confirmed_Lines_df["set"] = False
        Confirmed_Lines_df["bom"] = False
        Confirmed_Lines_df["bom_with_delivery_group"] = False
        Confirmed_Lines_df["cancelled"] = False

        Confirmed_Lines_df["Exported_Line_No"] = HQ_Confirmed_Lines_df["Exported_Line_No"].to_list()
        Confirmed_Lines_df["quantity"] = HQ_Confirmed_Lines_df["Quantity"].to_list()
        Confirmed_Lines_df["ordered_quantity"] = HQ_Confirmed_Lines_df["Ordered_Quantity"].to_list()
        Confirmed_Lines_df["price_amount"] = HQ_Confirmed_Lines_df["Unit_Price"].to_list()
        Confirmed_Lines_df["price_line_amount"] = Confirmed_Lines_df["quantity"]*Confirmed_Lines_df["price_amount"]
        Confirmed_Lines_df["PO_UoM"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="PO_UoM", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Unit_of_Measure_Code"), axis=1)
        Confirmed_Lines_df["order_unit"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit", Compare_Column_df1=["PO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
        Confirmed_Lines_df.drop(labels=["PO_UoM"], inplace=True, axis=1)
        Confirmed_Lines_df["description_long"] = Confirmed_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_long", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)
        
        # Line Flags
        Confirmed_Lines_df["Line_Flag"] = HQ_Confirmed_Lines_df["Line_Flag"].to_list()
        # Set Label
        Cancelled_conditions = [(Confirmed_Lines_df["Line_Flag"] == "Label")]
        Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Cancelled_conditions, Set_Column="bom", Set_Value=True)
        Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Cancelled_conditions, Set_Column="item_category", Set_Value="ZST")

        # Set Cancelled
        Cancelled_conditions = [(Confirmed_Lines_df["Line_Flag"] == "Cancelled")]
        Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Cancelled_conditions, Set_Column="cancelled", Set_Value=True)
        Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Cancelled_conditions, Set_Column="item_category", Set_Value="TAPA")

        # Set discontinued
        Discontinued_conditions = [(Confirmed_Lines_df["Line_Flag"] == "Finished")]
        Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Discontinued_conditions, Set_Column="discontinued", Set_Value=True)
        Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Discontinued_conditions, Set_Column="item_category", Set_Value="TAPA")

        Confirmed_Lines_df.drop(labels=["Line_Flag"], inplace=True, axis=1)

        # line_item_id
        Confirmed_Lines_df["line_item_id"] = Confirmed_Lines_df["Exported_Line_No"] // 100
        
        # supplier_order_item_id
        Vendor_Line_No_list = HQ_Confirmed_Lines_df["Vendor_Line_No"].to_list()
        line_item_id_list = []
        for Index, Value in enumerate(Vendor_Line_No_list):
            line_item_id_list.append(f"{Value :06d}")
        Confirmed_Lines_df["supplier_order_item_id"] = line_item_id_list

        # Round Values
        Confirmed_Lines_df["quantity"] = Confirmed_Lines_df["quantity"].round(2)
        Confirmed_Lines_df["ordered_quantity"] = Confirmed_Lines_df["ordered_quantity"].round(2)
        Confirmed_Lines_df["price_amount"] = Confirmed_Lines_df["price_amount"].round(2)
        Confirmed_Lines_df["price_line_amount"] = Confirmed_Lines_df["price_line_amount"].round(2)

        # Drop Duplicate rows amd reset index
        Confirmed_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
        Confirmed_Lines_df.reset_index(drop=True, inplace=True)

    return Confirmed_Lines_df, PO_Confirmation_Number

def Prepare_Confirmed_Lines_df_from_HQ_Exported(Configuration: dict|None, window: CTk|None, Purchase_Order: str, Purchase_Lines_df: DataFrame, HQ_Item_Transport_Register_df: DataFrame, Items_df: DataFrame, UoM_df: DataFrame, GUI: bool=True) -> DataFrame:
    PO_Confirmation_Number = "Fictive_Num_01"
    Exported_Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group", "cancelled", "Exported_Line_No", "PO_UoM"]
    Exported_Lines_df = DataFrame(columns=Exported_Lines_df_Columns)
    
    # Preparation
    mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
    Purchase_Lines_df_Filtered = DataFrame(Purchase_Lines_df[mask_Purch_Line])

    # Assing Data to Dataframe
    Exported_Items_list = HQ_Item_Transport_Register_df["Item_No"].to_list()
    Exported_Lines_df["supplier_aid"] = Exported_Items_list
    Exported_Lines_df["buyer_aid"] = Exported_Items_list
    Exported_Lines_df["item_category"] = "YN01"
    Exported_Lines_df["price_currency"] = HQ_Item_Transport_Register_df["Currency_Code"].to_list()      # Because of Invoice Generation
    Exported_Lines_df["discontinued"] = False
    Exported_Lines_df["set"] = False
    Exported_Lines_df["bom"] = False
    Exported_Lines_df["bom_with_delivery_group"] = False
    Exported_Lines_df["cancelled"] = False

    Exported_Lines_df["Exported_Line_No"] = HQ_Item_Transport_Register_df["Exported_Line_No"].to_list()
    Exported_Lines_df["quantity"] = HQ_Item_Transport_Register_df["Quantity"].to_list()
    Exported_Lines_df["ordered_quantity"] = HQ_Item_Transport_Register_df["Ordered_Quantity"].to_list()
    Exported_Lines_df["price_amount"] = Purchase_Lines_df["Direct_Unit_Cost"].to_list()
    Exported_Lines_df["price_line_amount"] = Exported_Lines_df["quantity"]*Exported_Lines_df["price_amount"]
    Exported_Lines_df["PO_UoM"] = Exported_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="PO_UoM", Compare_Column_df1=["buyer_aid"], Compare_Column_df2=["No"], Search_df=Purchase_Lines_df_Filtered, Search_Column="Unit_of_Measure_Code"), axis=1)
    Exported_Lines_df["order_unit"] = Exported_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="order_unit", Compare_Column_df1=["PO_UoM"], Compare_Column_df2=["Code"], Search_df=UoM_df, Search_Column="International_Standard_Code"), axis=1)
    Exported_Lines_df.drop(labels=["PO_UoM"], inplace=True, axis=1)
    Exported_Lines_df["description_long"] = Exported_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="description_long", Compare_Column_df1=["supplier_aid"], Compare_Column_df2=["No"], Search_df=Items_df, Search_Column="Description"), axis=1)
    
    # Line Flags
    Exported_Lines_df["Line_Flag"] = HQ_Item_Transport_Register_df["Line_Flag"].to_list()
    # Set Label
    Cancelled_conditions = [(Exported_Lines_df["Line_Flag"] == "Label")]
    Exported_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Exported_Lines_df, conditions=Cancelled_conditions, Set_Column="bom", Set_Value=True)
    Exported_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Exported_Lines_df, conditions=Cancelled_conditions, Set_Column="item_category", Set_Value="ZST")

    # Set Cancelled
    Cancelled_conditions = [(Exported_Lines_df["Line_Flag"] == "Cancelled")]
    Exported_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Exported_Lines_df, conditions=Cancelled_conditions, Set_Column="cancelled", Set_Value=True)
    Exported_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Exported_Lines_df, conditions=Cancelled_conditions, Set_Column="item_category", Set_Value="TAPA")

    # Set discontinued
    Discontinued_conditions = [(Exported_Lines_df["Line_Flag"] == "Finished")]
    Exported_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Exported_Lines_df, conditions=Discontinued_conditions, Set_Column="discontinued", Set_Value=True)
    Exported_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Exported_Lines_df, conditions=Discontinued_conditions, Set_Column="item_category", Set_Value="TAPA")

    Exported_Lines_df.drop(labels=["Line_Flag"], inplace=True, axis=1)

    # line_item_id
    Exported_Lines_df["line_item_id"] = Exported_Lines_df["Exported_Line_No"] // 100

    # supplier_order_item_id
    Exported_Line_No_list = Exported_Lines_df["Exported_Line_No"].to_list()
    supplier_order_item_id_list = []
    for Index, Value in enumerate(Exported_Line_No_list):
        Exported_Line_No = Value // 1000
        supplier_order_item_id_list.append(f"{Exported_Line_No :06d}")
    Exported_Lines_df["supplier_order_item_id"] = supplier_order_item_id_list
    
    # Round Values
    Exported_Lines_df["quantity"] = Exported_Lines_df["quantity"].round(2)
    Exported_Lines_df["ordered_quantity"] = Exported_Lines_df["ordered_quantity"].round(2)
    Exported_Lines_df["price_amount"] = Exported_Lines_df["price_amount"].round(2)
    Exported_Lines_df["price_line_amount"] = Exported_Lines_df["price_line_amount"].round(2)

    # Drop Duplicate rows amd reset index
    Exported_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
    Exported_Lines_df.reset_index(drop=True, inplace=True)

    return Exported_Lines_df, PO_Confirmation_Number

# ---------------------------------------------------------- For Invoice ---------------------------------------------------------- #
def Prepare_Delivery_Lines_df_from_HQ_Deliveries(Settings: dict, Configuration: dict|None, window: CTk|None, headers: dict, tenant_id: str, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Order: str, GUI: bool=True):
    import Libs.Downloader.NAV_OData_API as NAV_OData_API
    
    Delivery_Lines_df_Columns = ["Delivery_No", "line_item_id", "supplier_aid", "quantity", "order_unit", "delivery_start_date", "delivery_end_date", "order_id", "order_ref_line_item_id", "order_date", "supplier_order_id", "supplier_order_item_id", "serial_numbers"]
    Delivery_Lines_df = DataFrame(columns=Delivery_Lines_df_Columns)

    # Confirmed_Lines_df
    Confirmed_Lines_df_columns = ["supplier_aid", "supplier_order_item_id", "price_amount"]
    Confirmed_Lines_df = DataFrame(columns=Confirmed_Lines_df_columns)

    # HQ_Testing_HQ_Item_Transport_Register
    HQ_Delivery_Lines_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Purchase_Order], Document_Type="Order", Vendor_Document_Type="Delivery", GUI=GUI)
    if HQ_Delivery_Lines_df.empty:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Delivery/s for {Purchase_Order} during preparation of Invoice.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise APIError(message=f"It is not possible to download Delivery/s for {Purchase_Order} during preparation of Invoice.", status_code=500, charset="utf-8")
    else:
        # --------------------------------- Confirmation --------------------------------- # 
        # Confirmation Number
        HQ_Confirmation_Lines_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Purchase_Order], Document_Type="Order", Vendor_Document_Type="Confirmation", GUI=GUI)
        if HQ_Confirmation_Lines_df.empty:
            PO_Confirmation_Number = ""
        else:
            PO_Confirmation_Number = HQ_Confirmation_Lines_df.iloc[0]["Vendor_Document_No"]

        # Prepare Confirmed_Lines_df for Invoice process
        Confirmed_Lines_df["supplier_aid"] = HQ_Confirmation_Lines_df["Item_No"].to_list()
        Confirmed_Lines_df["supplier_order_item_id"] = HQ_Confirmation_Lines_df["Vendor_Line_No"].to_list()
        Confirmed_Lines_df["price_amount"] = HQ_Confirmation_Lines_df["Unit_Price"].to_list()
        Confirmed_Lines_df["price_currency"] = HQ_Confirmation_Lines_df["Currency_Code"].to_list()      # Because of Invoice Generation

        # supplier_order_item_id
        Vendor_Line_No_list = HQ_Confirmation_Lines_df["Vendor_Line_No"].to_list()
        Lines_No = len(Confirmed_Lines_df)
        line_item_id_list= []
        for Index, Value in enumerate(Vendor_Line_No_list):
            line_item_id_list.append((f"{Value :06d}"))
        Confirmed_Lines_df["supplier_order_item_id"] = line_item_id_list

        # --------------------------------- Delivery --------------------------------- # 
        # Prepare lists
        Downloaded_Delivery_List = HQ_Delivery_Lines_df["Vendor_Document_No"].to_list()
        Downloaded_Delivery_List = list(set(Downloaded_Delivery_List))
        Downloaded_Delivery_List.sort()
        
        if GUI == True:
            # Select Delivery PopUp
            def Select_PO_DEL_Number(Frame_Body: CTkFrame, Lines_No: int):
                PO_DEL_Number_list = []
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
                        Selected_Delivery_No_label = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe"].children["!ctklabel"]
                        Selected_Delivery_No = str(Selected_Delivery_No_label.cget("text"))
                        Selected_Delivery_No = Selected_Delivery_No.replace(":", "")
                        PO_DEL_Number_list.append(Selected_Delivery_No)
                    else:
                        pass

                PO_DEL_Number_list_joined = ";".join(PO_DEL_Number_list)
                PO_DEL_Number_Variable.set(value=PO_DEL_Number_list_joined)
                PO_DEL_Number_Window.destroy()

            # TopUp Window
            PO_DEL_Number_Window_geometry = (520, 500)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_DEL_Number_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_DEL_Number_Window_geometry[1] //2
            PO_DEL_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select Delivery/s", max_width=PO_DEL_Number_Window_geometry[0], max_height=PO_DEL_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_DEL_Number_Window, Name=f"Select Delivery/s", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Delivery Numbers for each Invoice creation..", GUI_Level_ID=3)
            Frame_Body = Frame_Main.children["!ctkframe2"]

            Lines_No = len(Downloaded_Delivery_List)
            for Delivery_Index, Delivery_Number in enumerate(Downloaded_Delivery_List):
                # Fields
                Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Delivery_Number}", Field_Type="Input_CheckBox") 
                Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                Fields_Frame_Var.configure(text="")

            # Dynamic Content height
            content_row_count = len(Frame_Body.winfo_children())
            content_height = (content_row_count + 1) * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
            if content_height > PO_DEL_Number_Window_geometry[1]:
                content_height = PO_DEL_Number_Window_geometry[1]
            else:
                # Update height of TopUp when content is smaller than max_height
                PO_DEL_Number_Window.maxsize(width=PO_DEL_Number_Window_geometry[0], height=content_height)
            Frame_Main.configure(bg_color = "#000001", height=content_height)

            # Buttons
            PO_DEL_Number_Variable = StringVar(master=PO_DEL_Number_Window, value="", name="PO_DEL_Number_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_DEL_Number(Frame_Body=Frame_Body, Lines_No=Lines_No))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Number selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_DEL_Number_Variable)
            PO_Delivery_Number_list = PO_DEL_Number_Variable.get().split(";")
        else:
            PO_Delivery_Number_list = Downloaded_Delivery_List

        # Filter HQ_Delivery_Lines_df by selected Delivery Numbers
        mask_Delivery_No = HQ_Delivery_Lines_df["Vendor_Document_No"].isin(PO_Delivery_Number_list) 
        HQ_Delivery_Lines_df_Filtered = DataFrame(HQ_Delivery_Lines_df[mask_Delivery_No])
        HQ_Delivery_Lines_df_Filtered.reset_index(drop=True, inplace=True)

        # Apply Data to Delivery_Lines_df
        Delivery_Lines_df["Delivery_No"] = HQ_Delivery_Lines_df_Filtered["Vendor_Document_No"].to_list()
        Delivery_Lines_df["supplier_aid"] = HQ_Delivery_Lines_df_Filtered["Item_No"].to_list()
        Delivery_Lines_df["quantity"] = HQ_Delivery_Lines_df_Filtered["Quantity"].to_list()
        Delivery_Lines_df["order_unit"] = HQ_Delivery_Lines_df_Filtered["Unit_of_Measure"].to_list()
        Delivery_Lines_df["delivery_start_date"] = HQ_Delivery_Lines_df_Filtered["Delivery_Date"].to_list()
        Delivery_Lines_df["delivery_end_date"] = HQ_Delivery_Lines_df_Filtered["Delivery_Date"].to_list()
        Delivery_Lines_df["order_id"] = Purchase_Order
        Delivery_Lines_df["order_date"] = HQ_Delivery_Lines_df_Filtered["Order_Date"].to_list()
        Delivery_Lines_df["supplier_order_id"] = PO_Confirmation_Number
        Delivery_Lines_df["serial_numbers"] = ""

        # supplier_order_item_id
        Vendor_Line_No_list = HQ_Delivery_Lines_df_Filtered["Vendor_Line_No"].to_list()
        supplier_order_item_id_list = []
        for Index, Value in enumerate(Vendor_Line_No_list):
            supplier_order_item_id_list.append(f"{Value :06d}")
        Delivery_Lines_df["supplier_order_item_id"] = supplier_order_item_id_list

        # order_ref_line_item_id
        Exported_Line_No_list = HQ_Delivery_Lines_df_Filtered["Exported_Line_No"].to_list()
        order_ref_line_item_id_list = []
        for Index, Value in enumerate(Exported_Line_No_list):
            order_ref_line_item_id = Value // 100
            order_ref_line_item_id_list.append(f"{order_ref_line_item_id :06d}")
        Delivery_Lines_df["order_ref_line_item_id"] = order_ref_line_item_id_list

        # Delivery Date and line_item_id
        PO_Delivery_Date_list = []
        for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
            mask_Delivery = HQ_Delivery_Lines_df_Filtered["Vendor_Document_No"] == Delivery_Number
            Delivery_Date_List_df_Filtered = DataFrame(HQ_Delivery_Lines_df_Filtered[mask_Delivery])
            
            # Delivery Date
            Delivery_Date = Delivery_Date_List_df_Filtered.iloc[0]["Delivery_Date"]
            PO_Delivery_Date_list.append(Delivery_Date)

            # line_item_id
            Line_Counter = 1
            for row in Delivery_Date_List_df_Filtered.iterrows():
                row_index = row[0]
                row_Series = Series(row[1])

                # Update Delivery_line_item_id
                Delivery_line_item_id = str(f"9{(Line_Counter) :05d}")
                Line_Counter += 1
                Delivery_Lines_df.at[row_index, "line_item_id"] = Delivery_line_item_id

        # --------------------------------- Package Tracking Register --------------------------------- # ¨
        # Plant --> because use on Invoice Lines
        Delivery_Lines_df["Plant_Help"] = ""
        HQ_HQ_Testing_HQ_Pack_Reg_df = NAV_OData_API.Get_HQ_Testing_HQ_Pack_Reg_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order=Purchase_Order, PO_Delivery_Number_list=PO_Delivery_Number_list, GUI=GUI)
        HQ_HQ_Testing_HQ_Pack_Reg_df.drop_duplicates(inplace=True, ignore_index=True)

        if HQ_HQ_Testing_HQ_Pack_Reg_df.empty:
            pass
        else:
            Delivery_Lines_df["Plant_Help"] = Delivery_Lines_df.apply(lambda row: Pandas_Functions.Dataframe_Apply_Value_from_df2(row=row, Fill_Column="Plant_Help", Compare_Column_df1=["Delivery_No"], Compare_Column_df2=["Delivery_No"], Search_df=HQ_HQ_Testing_HQ_Pack_Reg_df, Search_Column="Plant_No"), axis=1)
        
    return PO_Confirmation_Number, PO_Delivery_Number_list, PO_Delivery_Date_list, Delivery_Lines_df, Confirmed_Lines_df