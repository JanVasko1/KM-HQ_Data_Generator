# Import Libraries
from pandas import DataFrame

import Libs.File_Manipulation as File_Manipulation
import Libs.Pandas_Functions as Pandas_Functions
import Libs.GUI.Elements as Elements

from customtkinter import CTk

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Update_Confirm_df_for_Delivery(Confirmed_Lines_df: DataFrame) -> DataFrame:
    mask_Canceled_Lines = Confirmed_Lines_df["cancelled"] == False
    mask_Discontinued_Lines = Confirmed_Lines_df["discontinued"] == False
    mask_Label = Confirmed_Lines_df["bom"] == False
    # BUG --> if Machine is discontinued or canecelled also Label and FOCH should be removed
    Confirmed_Lines_df = Confirmed_Lines_df[mask_Canceled_Lines & mask_Discontinued_Lines & mask_Label]  
    Confirmed_Lines_df.reset_index(drop=True, inplace=True)

    Confirmed_Lines_df.to_csv(path_or_buf="Confirmed_Lines_df.csv", sep=";")
    return Confirmed_Lines_df

def Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration: dict, window: CTk, headers: dict, tenant_id: str, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Order: str, Purchase_Lines_df: DataFrame, Items_df: DataFrame, UoM_df: DataFrame) -> DataFrame:
    import Libs.Downloader.NAV_OData_API as NAV_OData_API
    
    Confirmed_Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group", "cancelled", "Exported_Line_No"]
    Confirmed_Lines_df = DataFrame(columns=Confirmed_Lines_df_Columns)

    # HQ_Testing_HQ_Item_Transport_Register
    HQ_Confirmed_Lines_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Purchase_Order], Document_Type="Order", Vendor_Document_Type="Confirmation")
    print(HQ_Confirmed_Lines_df)
    if HQ_Confirmed_Lines_df.empty:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Confirmation for {Purchase_Order} during preparation of Delivery.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        PO_Confirmation_Number = HQ_Confirmed_Lines_df.iloc[0]["Vendor_Document_No"]

        # Preparation
        mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
        Purchase_Lines_df_Filtered = Purchase_Lines_df[mask_Purch_Line] 

        # Assing Data to Dataframe
        Exported_Items_list = HQ_Confirmed_Lines_df["Item_No"].to_list()
        Confirmed_Lines_df["supplier_aid"] = Exported_Items_list
        Confirmed_Lines_df["buyer_aid"] = Exported_Items_list
        Confirmed_Lines_df["item_category"] = "YN01"
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
        Confirmed_Lines_df["supplier_order_item_id"] = HQ_Confirmed_Lines_df["Vendor_Line_No"].to_list()
        
        # Round Values
        Confirmed_Lines_df["quantity"] = Confirmed_Lines_df["quantity"].round(2)
        Confirmed_Lines_df["ordered_quantity"] = Confirmed_Lines_df["ordered_quantity"].round(2)
        Confirmed_Lines_df["price_amount"] = Confirmed_Lines_df["price_amount"].round(2)
        Confirmed_Lines_df["price_line_amount"] = Confirmed_Lines_df["price_line_amount"].round(2)

        # Drop Duplicate rows amd reset index
        Confirmed_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
        Confirmed_Lines_df.reset_index(drop=True, inplace=True)
        Confirmed_Lines_df.to_csv(path_or_buf="From_Confirmation.csv", sep=";")
       
    return Confirmed_Lines_df, PO_Confirmation_Number

def Prepare_Confirmed_Lines_df_from_HQ_Exported(Configuration: dict, window: CTk, Purchase_Order: str, Purchase_Lines_df: DataFrame, HQ_Item_Transport_Register_df: DataFrame, Items_df: DataFrame, UoM_df: DataFrame) -> DataFrame:
    PO_Confirmation_Number = "Fictive_Num_01"
    Exported_Lines_df_Columns = ["line_item_id", "supplier_aid", "buyer_aid", "description_long", "quantity", "order_unit", "price_amount", "price_line_amount", "delivery_start_date", "delivery_end_date", "ordered_quantity", "supplier_order_item_id", "item_category", "discontinued", "set", "bom", "bom_with_delivery_group", "cancelled", "Exported_Line_No"]
    Exported_Lines_df = DataFrame(columns=Exported_Lines_df_Columns)
    
    # Preparation
    mask_Purch_Line = Purchase_Lines_df["Document_No"] == Purchase_Order
    Purchase_Lines_df_Filtered = Purchase_Lines_df[mask_Purch_Line] 

    # Assing Data to Dataframe
    Exported_Items_list = HQ_Item_Transport_Register_df["Item_No"].to_list()
    Exported_Lines_df["supplier_aid"] = Exported_Items_list
    Exported_Lines_df["buyer_aid"] = Exported_Items_list
    Exported_Lines_df["item_category"] = "YN01"
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
    Exported_Lines_df["supplier_order_item_id"] = Exported_Lines_df["Exported_Line_No"] // 1000
    
    # Round Values
    Exported_Lines_df["quantity"] = Exported_Lines_df["quantity"].round(2)
    Exported_Lines_df["ordered_quantity"] = Exported_Lines_df["ordered_quantity"].round(2)
    Exported_Lines_df["price_amount"] = Exported_Lines_df["price_amount"].round(2)
    Exported_Lines_df["price_line_amount"] = Exported_Lines_df["price_line_amount"].round(2)

    # Drop Duplicate rows amd reset index
    Exported_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
    Exported_Lines_df.reset_index(drop=True, inplace=True)
    Exported_Lines_df.to_csv(path_or_buf="From_Export.csv", sep=";")

    return Exported_Lines_df, PO_Confirmation_Number


# ---------------------------------------------------------- Main Functions ---------------------------------------------------------- #
def Process_Purchase_Orders(Settings: dict, 
                            Configuration: dict,
                            window: CTk,
                            headers: dict, 
                            tenant_id: str, 
                            NUS_version: str, 
                            NOC: str, 
                            Environment: str, 
                            Company: str,
                            Can_Process: bool, 
                            Purchase_Headers_df: DataFrame, 
                            Purchase_Lines_df: DataFrame, 
                            HQ_Communication_Setup_df: DataFrame, 
                            Company_Information_df: DataFrame, 
                            Country_ISO_Code_list: list, 
                            HQ_CPDI_Level_df: DataFrame, 
                            HQ_CPDI_Status_df: DataFrame, 
                            HQ_Item_Transport_Register_df: DataFrame, 
                            Items_df: DataFrame, 
                            Items_BOMs_df: DataFrame, 
                            Items_Substitutions_df: DataFrame, 
                            Items_Connected_Items_df: DataFrame, 
                            Items_Price_List_Detail_df: DataFrame, 
                            Items_Tracking_df: DataFrame, 
                            Items_UoM_df: DataFrame, 
                            Items_Distr_Status_df: DataFrame,
                            NVR_FS_Connect_df: DataFrame, 
                            Plants_df: DataFrame, 
                            Shipment_Method_list: list, 
                            Shipping_Agent_list: list, 
                            Tariff_Number_list: list, 
                            UoM_df: DataFrame) -> None:
    # Get what should be prepared from Settings
    Generate_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Use"]
    Generate_CPDI = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Use"]
    Generate_PreAdvice = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Use"]
    Generate_Delivery = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Use"]
    Generate_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Use"]
    Generate_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["PDF"]["Generate"]
    Export_NAV_Folder = Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"]

    # Generate Purchase Order List
    Purchase_Orders_List = Purchase_Headers_df["No"].to_list()

    for Purchase_Order in Purchase_Orders_List:
        # Get Vendor for correct Export NAV folders for each PO (might be different Vendors)
        mask_PO = Purchase_Headers_df["No"] == Purchase_Order
        Single_PO_df = Purchase_Headers_df[mask_PO]  
        Buy_from_Vendor_No = Single_PO_df.iloc[0]["Buy_from_Vendor_No"]
        PDICenterFieldNUS = Single_PO_df.iloc[0]["PDICenterFieldNUS"]

        # ---------------- Confirmation ---------------- #
        if Generate_Confirmation == True:
            import Libs.Process.Purchase_Orders.Generate_Confirmation_Header as Generate_Confirmation_Header
            import Libs.Process.Purchase_Orders.Generate_Confirmation_Lines as Generate_Confirmation_Lines
            import Libs.Process.Purchase_Orders.Generate_Confirmation_ATP as Generate_Confirmation_ATP

            # Header
            PO_Confirmation_Header, PO_Confirmation_Number = Generate_Confirmation_Header.Generate_PO_CON_Header(Settings=Settings, 
                                                                                                            Configuration=Configuration, 
                                                                                                            window=window,
                                                                                                            Purchase_Order=Purchase_Order,
                                                                                                            Purchase_Headers_df=Purchase_Headers_df,
                                                                                                            Company_Information_df=Company_Information_df, 
                                                                                                            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                                            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df)
            
            # Lines
            Confirmed_Lines_df, PO_Confirmation_Lines, Total_Line_Amount, Lines_No = Generate_Confirmation_Lines.Generate_PO_CON_Lines(Settings=Settings, 
                                                                                                                                            Configuration=Configuration, 
                                                                                                                                            window=window,
                                                                                                                                            Purchase_Order=Purchase_Order,
                                                                                                                                            Purchase_Lines_df=Purchase_Lines_df,
                                                                                                                                            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df,
                                                                                                                                            Items_df=Items_df,
                                                                                                                                            Items_Substitutions_df=Items_Substitutions_df, 
                                                                                                                                            Items_Connected_Items_df=Items_Connected_Items_df, 
                                                                                                                                            Items_Price_List_Detail_df=Items_Price_List_Detail_df, 
                                                                                                                                            Items_Distr_Status_df=Items_Distr_Status_df,
                                                                                                                                            UoM_df=UoM_df)

            # ATP
            PO_Confirmation_Lines = Generate_Confirmation_ATP.Generate_PO_ATP_CON_Lines(Settings=Settings, Configuration=Configuration, window=window, Confirmed_Lines_df=Confirmed_Lines_df, PO_Confirmation_Lines=PO_Confirmation_Lines)

            # Put Header, Lines with ATP together
            PO_Confirmation_Header["orderresponse"]["orderresponse_item_list"] = PO_Confirmation_Lines

            # Update Footer
            PO_Confirmation_Header["orderresponse"]["orderresponse_summary"]["total_item_num"] = Lines_No
            PO_Confirmation_Header["orderresponse"]["orderresponse_summary"]["total_amount"] = round(number=Total_Line_Amount, ndigits=2)

            # Export 
            Confirmation_File_Name = f"ORDRSP_{PO_Confirmation_Number}_Test"
            if Export_NAV_Folder == True:
                File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PO_Confirmation_Header, HQ_File_Type_Path="HQ_Confirm_File_Path", File_Name=Confirmation_File_Name, File_suffix="json")
            else:
                File_Manipulation.Export_Download_Folders(File_Content=PO_Confirmation_Header, File_Name=Confirmation_File_Name, File_suffix="json")

            # Prepare Dataframe for Delivery, cannot be done sooner as Confirmation must contain all Items
            Confirmed_Lines_df = Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Confirmed_Lines_df)
        else:
            pass

        # ---------------- Delivery ---------------- #
        if Generate_Delivery == True:
            import Libs.Process.Purchase_Orders.Generate_Delivery_Header as Generate_Delivery_Header
            import Libs.Process.Purchase_Orders.Generate_Delivery_Lines as Generate_Delivery_Lines
            import Libs.Process.Purchase_Orders.Generate_Delivery_Packages_Headers as Generate_Delivery_Packages_Headers
            import Libs.Process.Purchase_Orders.Generate_Delivery_Packages_Lines as Generate_Delivery_Packages_Lines

            # Define if Confirmation lines existing
            if Generate_Confirmation == True:
                if Confirmed_Lines_df.empty:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Delivery", message=f"Confirmed_Lines_df data are empty (not created or all data are CAncelled/Finished ..), do you want to use already imported Confirmation or Export data as source data for delivery?", icon="question", option_1="Confirmation", option_2="Export", fade_in_duration=1, GUI_Level_ID=1)
                    if response == "Confirmation":    
                        Confirmed_Lines_df, PO_Confirmation_Number = Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order=Purchase_Order, Purchase_Lines_df=Purchase_Lines_df, Items_df=Items_df, UoM_df=UoM_df)
                        Confirmed_Lines_df = Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Confirmed_Lines_df)
                    elif response == "Export":  
                        Exported_Lines_df, PO_Confirmation_Number = Prepare_Confirmed_Lines_df_from_HQ_Exported(Configuration=Configuration, window=window, Purchase_Order=Purchase_Order, Purchase_Lines_df=Purchase_Lines_df, HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, Items_df=Items_df, UoM_df=UoM_df)
                        Confirmed_Lines_df = Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Exported_Lines_df)
                else:
                    # Just pass as all is already prepared
                    pass
            else:
                response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Delivery", message=f"You select to create Delivery without creation of Confirmation, do you want to use already imported Confirmation or Export data as source data for delivery?", icon="question", option_1="Confirmation", option_2="Export", fade_in_duration=1, GUI_Level_ID=1)
                if response == "Confirmation":    
                    Confirmed_Lines_df, PO_Confirmation_Number = Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order=Purchase_Order, Purchase_Lines_df=Purchase_Lines_df, Items_df=Items_df, UoM_df=UoM_df)
                    Confirmed_Lines_df = Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Confirmed_Lines_df)
                    print(Confirmed_Lines_df)
                elif response == "Export":  
                    Exported_Lines_df, PO_Confirmation_Number = Prepare_Confirmed_Lines_df_from_HQ_Exported(Configuration=Configuration, window=window, Purchase_Order=Purchase_Order, Purchase_Lines_df=Purchase_Lines_df, HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, Items_df=Items_df, UoM_df=UoM_df)
                    Confirmed_Lines_df = Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Exported_Lines_df)

            # Header
            PO_Deliveries, PO_Delivery_Number_list, PO_Delivery_Date_list, Delivery_Count = Generate_Delivery_Header.Generate_Delivery_Header(Settings=Settings, 
                                                                                                                                                Configuration=Configuration, 
                                                                                                                                                window=window, 
                                                                                                                                                Purchase_Order=Purchase_Order,
                                                                                                                                                Purchase_Headers_df=Purchase_Headers_df,
                                                                                                                                                Company_Information_df=Company_Information_df, 
                                                                                                                                                HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                                                                                Confirmed_Lines_df=Confirmed_Lines_df,
                                                                                                                                                Shipping_Agent_list=Shipping_Agent_list, 
                                                                                                                                                Shipment_Method_list=Shipment_Method_list)

            # Lines
            PO_Deliveries, Delivery_Lines_df = Generate_Delivery_Lines.Generate_Delivery_Lines(Settings=Settings, 
                                                                                                Configuration=Configuration, 
                                                                                                window=window, 
                                                                                                Purchase_Order=Purchase_Order, 
                                                                                                PO_Deliveries=PO_Deliveries,
                                                                                                Delivery_Count=Delivery_Count, 
                                                                                                PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                                                PO_Delivery_Date_list=PO_Delivery_Date_list, 
                                                                                                Confirmed_Lines_df=Confirmed_Lines_df, 
                                                                                                PO_Confirmation_Number=PO_Confirmation_Number, 
                                                                                                HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, 
                                                                                                Items_df=Items_df)

            # Package Headers
            PO_Deliveries, Package_Header_df, Weight_UoM, Volume_UoM = Generate_Delivery_Packages_Headers.Generate_Delivery_Packages_Headers(Settings=Settings, 
                                                                                                                                            Configuration=Configuration, 
                                                                                                                                            window=window,
                                                                                                                                            PO_Deliveries=PO_Deliveries, 
                                                                                                                                            PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                                                                                            Delivery_Lines_df=Delivery_Lines_df, 
                                                                                                                                            UoM_df=UoM_df)

            # Package Lines
            PO_Deliveries, Delivery_Lines_df, Package_Lines_df = Generate_Delivery_Packages_Lines.Generate_Delivery_Packages_Lines(Settings=Settings, 
                                                                                                                                    Configuration=Configuration, 
                                                                                                                                    window=window,
                                                                                                                                    PO_Deliveries=PO_Deliveries, 
                                                                                                                                    PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                                                                                    Delivery_Lines_df=Delivery_Lines_df, 
                                                                                                                                    Package_Header_df=Package_Header_df, 
                                                                                                                                    Items_UoM_df=Items_UoM_df, 
                                                                                                                                    UoM_df=UoM_df)

            # Update Footer
            for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
                mask_Delivery = Package_Lines_df["Delivery_No"] == Delivery_Number
                Package_Lines_df_Filtered = Package_Lines_df[mask_Delivery]

                Delivery_total_item_num = Package_Lines_df_Filtered.shape[0]
                Delivery_total_weight = round(number=Package_Lines_df_Filtered["Package_Line_Total_Weight"].sum(), ndigits=2)
                Delivery_total_volume = round(number=Package_Lines_df_Filtered["Package_Line_Total_Volume"].sum(), ndigits=2)

                PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_summary"]["total_item_num"] = Delivery_total_item_num
                PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_summary"]["total_weight"] = Delivery_total_weight
                PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_summary"]["weight_unit"] = Weight_UoM
                PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_summary"]["volume"] = Delivery_total_volume
                PO_Deliveries[Delivery_Index]["dispatchnotification"]["dispatchnotification_summary"]["volume_unit"] = Volume_UoM

            # Export 
            for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
                Delivery_Content = PO_Deliveries[Delivery_Index]
                Delivery_File_Name = f"DELVRY02_{Delivery_Number}_Test"
                if Export_NAV_Folder == True:
                    File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=Delivery_Content, HQ_File_Type_Path="HQ_Delivery_File_Path", File_Name=Delivery_File_Name, File_suffix="json")
                else:
                    File_Manipulation.Export_Download_Folders(File_Content=Delivery_Content, File_Name=Delivery_File_Name, File_suffix="json")
        else:
            pass

        # ---------------- PreAdvice ---------------- #
        if Generate_PreAdvice == True:
            import Libs.Process.Purchase_Orders.Generate_PreAdvice_File as Generate_PreAdvice_File

            # Define if Confirmation lines existing
            if Generate_Delivery == True:
                PO_PreAdviceNumber_list = PO_Delivery_Number_list
                PO_PreAdvices = Generate_PreAdvice_File.Generate_PreAdvice_from_Delivery_dict(Settings=Settings, Configuration=Configuration, window=window, PO_Deliveries=PO_Deliveries)
            else:
                # TODO --> postavit tuhle cestu podobně jako s Delviery / Cpnfirmation nechat vybrat na základě čeho postavit
                pass


            # Export 
            for PreAdvice_Index, PreAdvice_Number in enumerate(PO_PreAdviceNumber_list):
                PreAdvice_Content = PO_PreAdvices[PreAdvice_Index]
                Delivery_File_Name = f"PREADV02_{PreAdvice_Number}_Test"
                if Export_NAV_Folder == True:
                    File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PreAdvice_Content, HQ_File_Type_Path="HQ_PreAdvice_File_Path", File_Name=Delivery_File_Name, File_suffix="json")
                else:
                    File_Manipulation.Export_Download_Folders(File_Content=PreAdvice_Content, File_Name=Delivery_File_Name, File_suffix="json")
        else:
            pass

        # ---------------- CPDI ---------------- #
        if Generate_CPDI == True:
            if PDICenterFieldNUS == "BEU":      # Must check if PO is related to CPDI even if Generation enabled
                import Libs.Process.Purchase_Orders.Generate_CPDI_Status as Generate_CPDI_Status

                if Generate_Delivery == False:      # Check if process is called from Delivery or standalone
                    PO_Delivery_Number_list = []
                    response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="CPDI document generation.", message=f"Do you want to download Deliveries from HQ Item Transport Register related to {Purchase_Order} to make an choice?", icon="question", option_1="Download", option_2="Reject", fade_in_duration=1, GUI_Level_ID=1)
                    if response == "Download":                    
                        import Libs.Downloader.NAV_OData_API as NAV_OData_API

                        # HQ_Testing_HQ_Item_Transport_Register
                        Deliveries_HQ_Item_Tr_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Purchase_Order], Document_Type="Order", Vendor_Document_Type="Delivery")
                        if Deliveries_HQ_Item_Tr_df.empty:
                            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Delivery for {Purchase_Order} during preparation of CPDI, when Delivery is not generated by full path script.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                        else:
                            # Drop Duplicate rows amd reset index
                            Deliveries_HQ_Item_Tr_df.drop_duplicates(inplace=True, ignore_index=True)
                            Deliveries_HQ_Item_Tr_df.reset_index(drop=True, inplace=True)
                            PO_Delivery_Number_list = Deliveries_HQ_Item_Tr_df["Vendor_Document_No"].to_list()
                    else:
                        pass
                else:
                    pass

                Generate_CPDI_Status.Generate_PO_CPDI_Messages(Settings=Settings, 
                                                                Configuration=Configuration, 
                                                                window=window, 
                                                                Export_NAV_Folder=Export_NAV_Folder,
                                                                NVR_FS_Connect_df=NVR_FS_Connect_df,
                                                                HQ_Communication_Setup_df=HQ_Communication_Setup_df,
                                                                PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                Purchase_Order=Purchase_Order, 
                                                                Buy_from_Vendor_No=Buy_from_Vendor_No,
                                                                Purchase_Headers_df=Purchase_Headers_df, 
                                                                HQ_CPDI_Level_df=HQ_CPDI_Level_df, 
                                                                HQ_CPDI_Status_df=HQ_CPDI_Status_df)
            else:
                pass
        else:
            pass

        # ---------------- Invoice ---------------- #
        if Generate_Invoice == True:
            # TIP --> Pozor na situaci, kdy Invoice bude generovaná v jiném běhu než Delivery --> pak by se měl program zeptat na základě čeho chceme Invoice dělat
            # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
            print("Process_Invoice")
        else:
            pass
        
        # ---------------- Invoice PDF ---------------- #
        if Generate_Invoice_PDF == True:
            print("Generate_Invoice_PDF")
        else:
            pass

def Process_BackBoneBilling(Settings: dict, 
                            Configuration: dict,
                            window: CTk,
                            Can_Process: bool, 
                            Buy_from_Vendor_No: str,
                            HQ_Communication_Setup_df: DataFrame, 
                            NVR_FS_Connect_df: DataFrame, 
                            Vendor_Service_Function_df: DataFrame, 
                            Company_Information_df: DataFrame,
                            Plants_df: DataFrame, 
                            Country_ISO_Code_list: list, 
                            Tariff_Number_list: list) -> None:
    # Get what should be prepared from Settings
    Generate_BB_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Use"]
    Generate_BB_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["PDF"]["Generate"]
    Generate_BB_IAL = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["IAL"]["Use"]
    Export_NAV_Folder = Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"]

    # ---------------- Invoice ---------------- #
    if Generate_BB_Invoice == True:
        import Libs.Process.BackBone_Billing.Generate_BB_Header as Generate_BB_Header
        import Libs.Process.BackBone_Billing.Generate_BB_Lines as Generate_BB_Lines

        # Header
        BB_Invoice, BB_Number, BB_Order_ID, BB_supplier_order_id, BB_Order_Date = Generate_BB_Header.Generate_BB_Header(Settings=Settings, 
                                                                                                                        Configuration=Configuration, 
                                                                                                                        window=window, 
                                                                                                                        Company_Information_df=Company_Information_df, 
                                                                                                                        HQ_Communication_Setup_df=HQ_Communication_Setup_df)
        
        # Lines
        BB_Invoice_Lines, BB_Lines_No, BB_Total_Line_Amount, BB_Table_Data = Generate_BB_Lines.Generate_BB_Lines(Settings=Settings, 
                                                                                                            Configuration=Configuration, 
                                                                                                            window=window, 
                                                                                                            Vendor_Service_Function_df=Vendor_Service_Function_df, 
                                                                                                            Plants_df=Plants_df,
                                                                                                            Country_ISO_Code_list=Country_ISO_Code_list,
                                                                                                            Tariff_Number_list=Tariff_Number_list,
                                                                                                            BB_Number=BB_Number, 
                                                                                                            BB_Order_ID=BB_Order_ID, 
                                                                                                            BB_supplier_order_id=BB_supplier_order_id,
                                                                                                            BB_Order_Date=BB_Order_Date)
                                                    
        # Update Lines
        BB_Invoice["invoice"]["invoice_item_list"] = BB_Invoice_Lines

        # Update Footer
        BB_Invoice["invoice"]["invoice_summary"]["total_item_num"] = round(number=BB_Lines_No, ndigits=2)
        BB_Invoice["invoice"]["invoice_summary"]["total_amount"] = round(number=BB_Total_Line_Amount, ndigits=2)
        BB_Invoice["invoice"]["invoice_summary"]["total_tax_amount"] = round(number=0, ndigits=2)

        # Export 
        BB_Invoice_File_Name = f"INVOIC02_{BB_Number}_Test"
        if Export_NAV_Folder == True:
            File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=BB_Invoice, HQ_File_Type_Path="HQ_Invoice_File_Path", File_Name=BB_Invoice_File_Name, File_suffix="json")
        else:
            File_Manipulation.Export_Download_Folders(File_Content=BB_Invoice, File_Name=BB_Invoice_File_Name, File_suffix="json")
    else:
        pass

    # ---------------- Invoice PDF ---------------- #
    if Generate_BB_Invoice_PDF == True:
        import Libs.Process.PDF_Generator as PDF_Generator
        BB_Invoice_PDF = PDF_Generator.Generate_PDF(Settings=Settings, Configuration=Configuration, Invoice=BB_Invoice, Table_Data=BB_Table_Data)

        # Export 
        # File name must be same as Invoice Number
        if Export_NAV_Folder == True:
            File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=BB_Invoice_PDF, HQ_File_Type_Path="HQ_PDF_File_Path", File_Name=BB_Number, File_suffix="pdf")
        else:
            File_Manipulation.Export_Download_Folders(File_Content=BB_Invoice_PDF, File_Name=BB_Number, File_suffix="pdf")
    else:
        pass

    # ---------------- IAL File ---------------- #
    if Generate_BB_IAL == True:
        print("Generate_BB_IAL")
    else:
        pass


def Process_Purchase_Return_Orders(Settings: dict,
                                   Configuration: dict) -> None:
    Generate_PRO_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Use"]
    Generate_PRO_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["Use"]
    Generate_PRO_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["PDF"]["Generate"]

    if Generate_PRO_Confirmation == True:
        print("Generate_PRO_Confirmation")
    else:
        pass

    if Generate_PRO_Invoice == True:
        # TIP --> Pozor na situaci, kdy Invoice bude generovaná v jiném běhu než Confirmation --> pak by se měl program zeptat na základě čeho chceme Invoice dělat (Většinou je Credit Memo = Confirmaiton)
        print("Generate_PRO_Invoice")
    else:
        pass

    if Generate_PRO_Invoice_PDF == True:
        print("Generate_PRO_Invoice_PDF")
    else:
        pass
