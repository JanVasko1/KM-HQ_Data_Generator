# Import Libraries
from pandas import DataFrame

import Libs.File_Manipulation as File_Manipulation
import Libs.Pandas_Functions as Pandas_Functions
import Libs.GUI.Elements as Elements

from customtkinter import CTk

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Get_Confirmed_HQ_Lines_for_Delivery(Configuration: dict, window: CTk, Purchase_Order: str, headers: dict, tenant_id: str, NUS_version: str, NOC: str, Environment: str, Company: str) -> DataFrame:
    response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery document generation.", message=f"Do you want to download Confirmation from HQ Item Transport Register related to {Purchase_Order} to build data for Delivery?", icon="question", option_1="Download", option_2="Reject", fade_in_duration=1, GUI_Level_ID=1)
    if response == "Download":                    
        import Libs.Downloader.NAV_OData_API as NAV_OData_API

        # HQ_Testing_HQ_Item_Transport_Register
        Confirmed_Lines_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Purchase_Order], Document_Type="Order", Vendor_Document_Type="Confirmation")
        if Confirmed_Lines_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Confirmation for {Purchase_Order} during preparation of Delivery.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            # Set Cancelled
            Confirmed_Lines_df["cancelled"] = False
            Cancelled_conditions = [(Confirmed_Lines_df["Line_Flag"] == "Cancelled")]
            Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Cancelled_conditions, Set_Column="cancelled", Set_Value=True)

            # Set discontinued
            Confirmed_Lines_df["discontinued"] = False
            Discontinued_conditions = [(Confirmed_Lines_df["Line_Flag"] == "Finished")]
            Confirmed_Lines_df = Pandas_Functions.Dataframe_Set_Value_on_Condition(Set_df=Confirmed_Lines_df, conditions=Discontinued_conditions, Set_Column="discontinued", Set_Value=True)

            # Prepare Dataframe for Delivery
            mask_Canceled_Lines = Confirmed_Lines_df["cancelled"] == False
            mask_Discontinued_Lines = Confirmed_Lines_df["discontinued"] == False
            Confirmed_Lines_df = Confirmed_Lines_df[mask_Canceled_Lines & mask_Discontinued_Lines]  

            # Drop Duplicate rows amd reset index
            Confirmed_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
            Confirmed_Lines_df.reset_index(drop=True, inplace=True)
            print("\n----------Confirmed_Lines_df----------")
            print(Confirmed_Lines_df)
    else:
        # TODO --> what to do when Empty be return ???? How to make Confirmaiton Number (as it is part f Delviery)
        Confirmed_Lines_df = DataFrame()

    return Confirmed_Lines_df

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
            PO_Confirmation, PO_Confirmation_Number = Generate_Confirmation_Header.Generate_PO_CON_Header(Settings=Settings, 
                                                                                                            Configuration=Configuration, 
                                                                                                            window=window,
                                                                                                            Purchase_Order=Purchase_Order,
                                                                                                            Purchase_Headers_df=Purchase_Headers_df,
                                                                                                            Company_Information_df=Company_Information_df, 
                                                                                                            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                                            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df)
            
            # Lines
            Confirmation_Lines_df, PO_Confirmation_Lines, Total_Line_Amount, Lines_No = Generate_Confirmation_Lines.Generate_PO_CON_Lines(Settings=Settings, 
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
            PO_Confirmation_Lines = Generate_Confirmation_ATP.Generate_PO_ATP_CON_Lines(Settings=Settings, Configuration=Configuration, window=window, Lines_df=Confirmation_Lines_df, PO_Confirmation_Lines=PO_Confirmation_Lines)

            # Put Header, Lines with ATP together
            PO_Confirmation["orderresponse"]["orderresponse_item_list"] = PO_Confirmation_Lines

            # Update Footer
            PO_Confirmation["orderresponse"]["orderresponse_summary"]["total_item_num"] = Lines_No
            PO_Confirmation["orderresponse"]["orderresponse_summary"]["total_amount"] = round(number=Total_Line_Amount, ndigits=2)

            # Export 
            if Export_NAV_Folder == True:
                File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PO_Confirmation, HQ_File_Type_Path="HQ_Confirm_File_Path", File_Name=PO_Confirmation_Number, File_suffix="json")
            else:
                File_Manipulation.Export_Download_Folders(File_Content=PO_Confirmation, File_Name=PO_Confirmation_Number, File_suffix="json")

            # Prepare Dataframe for Delivery, cannot be done sooner as Confirmation must contain all Items
            mask_Canceled_Lines = Confirmation_Lines_df["cancelled"] == False
            mask_Discontinued_Lines = Confirmation_Lines_df["discontinued"] == False
            mask_Label = Confirmation_Lines_df["bom"] == False
            # BUG --> if Machine is discontinued or canecelled also Label and FOCH should be removed
            Confirmed_Lines_df = Confirmation_Lines_df[mask_Canceled_Lines & mask_Discontinued_Lines & mask_Label]  
            Confirmed_Lines_df.reset_index(drop=True, inplace=True)
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
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Delivery", message=f"Confirmed_Lines_df data are empty, program will use Exported data as source data for delivery?", icon="question", option_1="Confirmation", option_2="Export", fade_in_duration=1, GUI_Level_ID=1)
                    # TODO --> transfer HQ Export to Confirmed_Lines_df so it can be used as source for Delivery + to finish all data transfered to Delviery_Generators like "PO_Confirmation_Number"
                    # TODO --> Data of "Confirmed_Lines_df" msut be exactly same as if it would be generated by program
                else:
                    pass
            else:
                response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Delivery", message=f"Do you want to use Confirmation or Export data as source data for delivery?", icon="question", option_1="Confirmation", option_2="Export", fade_in_duration=1, GUI_Level_ID=1)
                if response == "Confirmation":    
                    Confirmed_Lines_df = Get_Confirmed_HQ_Lines_for_Delivery(Configuration=Configuration, window=window, Purchase_Order=Purchase_Order, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
                    # TODO --> Data of "Confirmed_Lines_df" msut be exactly same as if it would be generated by program
                elif response == "Export":  
                    # TODO --> transfer HQ Export to Confirmed_Lines_df so it can be used as source for Delivery + to finish all data transfered to Delviery_Generators like "PO_Confirmation_Number"
                    # TODO --> Data of "Confirmed_Lines_df" msut be exactly same as if it would be generated by program
                    pass

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
                if Export_NAV_Folder == True:
                    File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=Delivery_Content, HQ_File_Type_Path="HQ_Delivery_File_Path", File_Name=Delivery_Number, File_suffix="json")
                else:
                    File_Manipulation.Export_Download_Folders(File_Content=Delivery_Content, File_Name=Delivery_Number, File_suffix="json")
        else:
            pass

        # ---------------- PreAdvice ---------------- #
        if Generate_PreAdvice == True:
            # TIP --> Pozor na situaci, kdy Preadvice bude generované v jiném běhu než Confirmation / Delivery --> pak by se měl program zeptat na základě čeho chceme PreAdvice dělat
            # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
            print("Process_PreAdvice")
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
                            print("\n----------Deliveries_HQ_Item_Tr_df----------")
                            print(Deliveries_HQ_Item_Tr_df)
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
        BB_Invoice_Lines, Lines_No, Total_Line_Amount, Table_Data = Generate_BB_Lines.Generate_BB_Lines(Settings=Settings, 
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
        BB_Invoice["invoice"]["invoice_summary"]["total_item_num"] = round(number=Lines_No, ndigits=2)
        BB_Invoice["invoice"]["invoice_summary"]["total_amount"] = round(number=Total_Line_Amount, ndigits=2)
        BB_Invoice["invoice"]["invoice_summary"]["total_tax_amount"] = round(number=0, ndigits=2)

        # Export 
        if Export_NAV_Folder == True:
            File_Manipulation.Export_NAV_Folders(NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=BB_Invoice, HQ_File_Type_Path="HQ_Invoice_File_Path", File_Name=BB_Number, File_suffix="json")
        else:
            File_Manipulation.Export_Download_Folders(File_Content=BB_Invoice, File_Name=BB_Number, File_suffix="json")
    else:
        pass

    # ---------------- Invoice PDF ---------------- #
    if Generate_BB_Invoice_PDF == True:
        import Libs.Process.PDF_Generator as PDF_Generator
        BB_Invoice_PDF = PDF_Generator.Generate_PDF(Settings=Settings, Configuration=Configuration, Invoice=BB_Invoice, Table_Data=Table_Data)

        # Export 
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
