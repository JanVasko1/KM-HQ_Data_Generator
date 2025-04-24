# Import Libraries
from pandas import DataFrame

import Libs.File_Manipulation as File_Manipulation
import Libs.GUI.Elements as Elements
import Libs.Process.Prepare_Files_Helpers as Prepare_Files_Helpers

from customtkinter import CTk

# ---------------------------------------------------------- Main Functions ---------------------------------------------------------- #
def Process_Purchase_Orders(Settings: dict, 
                            Configuration: dict|None,
                            window: CTk|None,
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
                            UoM_df: DataFrame,
                            GUI: bool=True) -> None:
    
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

    for Purchase_Order_index, Purchase_Order in enumerate(Purchase_Orders_List):
        # Purchase Order index --> because of multiple POs processing 
        Purchase_Order_index = str(Purchase_Order_index)

        # Get Vendor for correct Export NAV folders for each PO (might be different Vendors)
        mask_PO = Purchase_Headers_df["No"] == Purchase_Order
        Single_PO_df = DataFrame(Purchase_Headers_df[mask_PO])
        Buy_from_Vendor_No = Single_PO_df.iloc[0]["Buy_from_Vendor_No"]
        PDICenterFieldNUS = Single_PO_df.iloc[0]["PDICenterFieldNUS"]

        # -------------------------------- Confirmation -------------------------------- #
        if Generate_Confirmation == True:
            import Libs.Process.Purchase_Orders.Generate_Confirmation_Header as Generate_Confirmation_Header
            import Libs.Process.Purchase_Orders.Generate_Confirmation_Lines as Generate_Confirmation_Lines
            import Libs.Process.Purchase_Orders.Generate_Confirmation_ATP as Generate_Confirmation_ATP

            # Header
            PO_Confirmation_Header, PO_Confirmation_Number, PO_Confirmation_Currency = Generate_Confirmation_Header.Generate_PO_CON_Header(Settings=Settings, 
                                                                                                                                            Configuration=Configuration, 
                                                                                                                                            window=window,
                                                                                                                                            Purchase_Order=Purchase_Order,
                                                                                                                                            Purchase_Order_index=Purchase_Order_index,
                                                                                                                                            Purchase_Headers_df=Purchase_Headers_df,
                                                                                                                                            Company_Information_df=Company_Information_df, 
                                                                                                                                            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                                                                            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df,
                                                                                                                                            GUI=GUI)
                        
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
                                                                                                                                            UoM_df=UoM_df, 
                                                                                                                                            PO_Confirmation_Currency=PO_Confirmation_Currency,
                                                                                                                                            GUI=GUI)

            # ATP
            PO_Confirmation_Lines = Generate_Confirmation_ATP.Generate_PO_ATP_CON_Lines(Settings=Settings, Configuration=Configuration, window=window, Confirmed_Lines_df=Confirmed_Lines_df, PO_Confirmation_Lines=PO_Confirmation_Lines, GUI=GUI)

            # Put Header, Lines with ATP together
            PO_Confirmation_Header["orderresponse"]["orderresponse_item_list"] = PO_Confirmation_Lines

            # Update Footer
            PO_Confirmation_Header["orderresponse"]["orderresponse_summary"]["total_item_num"] = Lines_No
            PO_Confirmation_Header["orderresponse"]["orderresponse_summary"]["total_amount"] = round(number=Total_Line_Amount, ndigits=2)

            # Export 
            Confirmation_File_Name = f"ORDRSP_{PO_Confirmation_Number}_Test"
            if Export_NAV_Folder == True:
                File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PO_Confirmation_Header, HQ_File_Type_Path="HQ_Confirm_File_Path", File_Name=Confirmation_File_Name, File_suffix="json", GUI=GUI)
            else:
                File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=PO_Confirmation_Header, File_Name=Confirmation_File_Name, File_suffix="json", GUI=GUI)

            # Prepare Dataframe for Delivery, cannot be done sooner as Confirmation must contain all Items
            Confirmed_Lines_df = Prepare_Files_Helpers.Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Confirmed_Lines_df, Items_df=Items_df)
        else:
            pass

        # -------------------------------- Delivery -------------------------------- #
        if Generate_Delivery == True:
            import Libs.Process.Purchase_Orders.Generate_Delivery_Header as Generate_Delivery_Header
            import Libs.Process.Purchase_Orders.Generate_Delivery_Lines as Generate_Delivery_Lines
            import Libs.Process.Purchase_Orders.Generate_Delivery_Packages_Headers as Generate_Delivery_Packages_Headers
            import Libs.Process.Purchase_Orders.Generate_Delivery_Packages_Lines as Generate_Delivery_Packages_Lines

            # Define if Confirmation lines existing
            if Generate_Confirmation == True:
                if Confirmed_Lines_df.empty:
                    if GUI == True:
                        response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Delivery", message=f"Confirmed_Lines_df data are empty (not created or all data are Cancelled/Finished ..), do you want to use already imported Confirmation or Export data as source data for delivery?", icon="question", option_1="Confirmation", option_2="Export", fade_in_duration=1, GUI_Level_ID=1)
                    else:
                        response = "Confirmation"
                    if response == "Confirmation":    
                        Confirmed_Lines_df, PO_Confirmation_Number = Prepare_Files_Helpers.Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Document_Number=Purchase_Order, Document_Type="Order", Document_Lines_df=Purchase_Lines_df, Items_df=Items_df, UoM_df=UoM_df, GUI=GUI)
                        Confirmed_Lines_df = Prepare_Files_Helpers.Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Confirmed_Lines_df, Items_df=Items_df)
                    elif response == "Export":  
                        Exported_Lines_df, PO_Confirmation_Number = Prepare_Files_Helpers.Prepare_Confirmed_Lines_df_from_HQ_Exported(Configuration=Configuration, window=window, Purchase_Order=Purchase_Order, Purchase_Lines_df=Purchase_Lines_df, HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, Items_df=Items_df, UoM_df=UoM_df, GUI=GUI)
                        Confirmed_Lines_df = Prepare_Files_Helpers.Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Exported_Lines_df, Items_df=Items_df)
                else:
                    # Just pass as all is already prepared
                    pass
            else:
                if GUI == True:
                    response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Delivery", message=f"You select to create Delivery without creation of Confirmation, do you want to use already imported Confirmation or Export data as source data for delivery?", icon="question", option_1="Confirmation", option_2="Export", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    response = "Confirmation"
                if response == "Confirmation":    
                    Confirmed_Lines_df, PO_Confirmation_Number = Prepare_Files_Helpers.Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Document_Number=Purchase_Order, Document_Type="Order", Document_Lines_df=Purchase_Lines_df, Items_df=Items_df, UoM_df=UoM_df, GUI=GUI)
                    Confirmed_Lines_df = Prepare_Files_Helpers.Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Confirmed_Lines_df, Items_df=Items_df)
                elif response == "Export":  
                    Exported_Lines_df, PO_Confirmation_Number = Prepare_Files_Helpers.Prepare_Confirmed_Lines_df_from_HQ_Exported(Configuration=Configuration, window=window, Purchase_Order=Purchase_Order, Purchase_Lines_df=Purchase_Lines_df, HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, Items_df=Items_df, UoM_df=UoM_df, GUI=GUI)
                    Confirmed_Lines_df = Prepare_Files_Helpers.Update_Confirm_df_for_Delivery(Confirmed_Lines_df=Exported_Lines_df, Items_df=Items_df)

            # Header
            PO_Deliveries, PO_Delivery_Number_list, PO_Delivery_Date_list, Delivery_Count = Generate_Delivery_Header.Generate_Delivery_Header(Settings=Settings, 
                                                                                                                                                Configuration=Configuration, 
                                                                                                                                                window=window, 
                                                                                                                                                Purchase_Order=Purchase_Order,
                                                                                                                                                Purchase_Order_index=Purchase_Order_index,
                                                                                                                                                Purchase_Headers_df=Purchase_Headers_df,
                                                                                                                                                Company_Information_df=Company_Information_df, 
                                                                                                                                                HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                                                                                Confirmed_Lines_df=Confirmed_Lines_df,
                                                                                                                                                Shipping_Agent_list=Shipping_Agent_list, 
                                                                                                                                                Shipment_Method_list=Shipment_Method_list,
                                                                                                                                                GUI=GUI)

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
                                                                                                Items_df=Items_df,
                                                                                                Items_Tracking_df=Items_Tracking_df,
                                                                                                GUI=GUI)
            # Package Headers
            PO_Deliveries, Package_Header_df, Weight_UoM, Volume_UoM = Generate_Delivery_Packages_Headers.Generate_Delivery_Packages_Headers(Settings=Settings, 
                                                                                                                                            Configuration=Configuration, 
                                                                                                                                            window=window,
                                                                                                                                            PO_Deliveries=PO_Deliveries, 
                                                                                                                                            PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                                                                                            Delivery_Lines_df=Delivery_Lines_df, 
                                                                                                                                            UoM_df=UoM_df,
                                                                                                                                            GUI=GUI)

            # Package Lines
            PO_Deliveries, Delivery_Lines_df, Package_Lines_df = Generate_Delivery_Packages_Lines.Generate_Delivery_Packages_Lines(Settings=Settings, 
                                                                                                                                    Configuration=Configuration, 
                                                                                                                                    window=window,
                                                                                                                                    PO_Deliveries=PO_Deliveries, 
                                                                                                                                    PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                                                                                    Delivery_Lines_df=Delivery_Lines_df, 
                                                                                                                                    Package_Header_df=Package_Header_df, 
                                                                                                                                    Items_UoM_df=Items_UoM_df, 
                                                                                                                                    UoM_df=UoM_df,
                                                                                                                                    GUI=GUI)

            # Update Footer
            for Delivery_Index, Delivery_Number in enumerate(PO_Delivery_Number_list):
                mask_Delivery = Delivery_Lines_df["Delivery_No"] == Delivery_Number
                Delivery_Lines_df_Filtered = DataFrame(Delivery_Lines_df[mask_Delivery])
                
                mask_Delivery = Package_Lines_df["Delivery_No"] == Delivery_Number
                Package_Lines_df_Filtered = DataFrame(Package_Lines_df[mask_Delivery])

                Delivery_total_item_num = Delivery_Lines_df_Filtered.shape[0]
                Delivery_total_weight = round(number=float(Package_Lines_df_Filtered["Package_Line_Total_Weight"].sum()), ndigits=2)
                Delivery_total_volume = round(number=float(Package_Lines_df_Filtered["Package_Line_Total_Volume"].sum()), ndigits=2)

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
                    File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=Delivery_Content, HQ_File_Type_Path="HQ_Delivery_File_Path", File_Name=Delivery_File_Name, File_suffix="json", GUI=GUI)
                else:
                    File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=Delivery_Content, File_Name=Delivery_File_Name, File_suffix="json", GUI=GUI)
        else:
            pass

        # -------------------------------- PreAdvice -------------------------------- #
        if Generate_PreAdvice == True:
            import Libs.Process.Purchase_Orders.Generate_PreAdvice_File as Generate_PreAdvice_File

            # Define if Confirmation lines existing
            if Generate_Delivery == True:
                PO_PreAdviceNumber_list = PO_Delivery_Number_list
                PO_PreAdvices = Generate_PreAdvice_File.Generate_PreAdvice_from_Delivery_dict(Settings=Settings, Configuration=Configuration, window=window, PO_Deliveries=PO_Deliveries, GUI=GUI)
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It should not be possible to create PreAdvice without Delivery.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    pass

            # Export 
            for PreAdvice_Index, PreAdvice_Number in enumerate(PO_PreAdviceNumber_list):
                PreAdvice_Content = PO_PreAdvices[PreAdvice_Index]
                Delivery_File_Name = f"PREADV02_{PreAdvice_Number}_Test"
                if Export_NAV_Folder == True:
                    File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PreAdvice_Content, HQ_File_Type_Path="HQ_PreAdvice_File_Path", File_Name=Delivery_File_Name, File_suffix="json", GUI=GUI)
                else:
                    File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=PreAdvice_Content, File_Name=Delivery_File_Name, File_suffix="json", GUI=GUI)
        else:
            pass

        # -------------------------------- CPDI -------------------------------- #
        if Generate_CPDI == True:
            if PDICenterFieldNUS == "BEU":      # Must check if PO is related to CPDI even if Generation enabled
                import Libs.Process.Purchase_Orders.Generate_CPDI_Status as Generate_CPDI_Status

                if Generate_Delivery == False:      # Check if process is called from Delivery or standalone
                    PO_Delivery_Number_list = []
                    if GUI == True:
                        response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="CPDI document generation.", message=f"Do you want to download Deliveries from HQ Item Transport Register related to {Purchase_Order} to make an choice?", icon="question", option_1="Download", option_2="Reject", fade_in_duration=1, GUI_Level_ID=1)
                    else:
                        response = "Download"
                    if response == "Download":                    
                        import Libs.Downloader.NAV_OData_API as NAV_OData_API

                        # HQ_Testing_HQ_Item_Transport_Register
                        Deliveries_HQ_Item_Tr_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=[Purchase_Order], Document_Type="Order", Vendor_Document_Type="Delivery", GUI=GUI)
                        if Deliveries_HQ_Item_Tr_df.empty:
                            if GUI == True:
                                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It is not possible to download Delivery for {Purchase_Order} during preparation of CPDI, when Delivery is not generated by full path script.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                            else:
                                pass
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
                                                                HQ_CPDI_Status_df=HQ_CPDI_Status_df,
                                                                Tariff_Number_list=Tariff_Number_list,
                                                                GUI=GUI)
            else:
                pass
        else:
            pass

        # -------------------------------- Invoice -------------------------------- #
        if Generate_Invoice == True:
            import Libs.Process.Purchase_Orders.Generate_Invoice_Header as Generate_Invoice_Header
            import Libs.Process.Purchase_Orders.Generate_Invoice_Lines as Generate_Invoice_Lines

            # Define if Delivery lines existing
            if Generate_Delivery == True:
                if Delivery_Lines_df.empty:
                    if GUI == True:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Invoice", message=f"Delivery_Lines_df data are empty (not created or all data are Cancelled/Finished ..), do you want to use already imported Delivery data as source data for invoice?", icon="question", option_1="OK", fade_in_duration=1, GUI_Level_ID=1)
                    else:
                        pass 
                    PO_Confirmation_Number, PO_Delivery_Number_list, PO_Delivery_Date_list, Delivery_Lines_df, Confirmed_Lines_df = Prepare_Files_Helpers.Prepare_Delivery_Lines_df_from_HQ_Deliveries(Settings=Settings, Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order=Purchase_Order, GUI=GUI)
                else:
                    # Just pass as all is already prepared
                    pass
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Data for Invoice", message=f"You select to create Invoice without creation of Delivery, do you want to use already imported Delivery data as source data for Invoice?", icon="question", option_1="OK", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    pass
                PO_Confirmation_Number, PO_Delivery_Number_list, PO_Delivery_Date_list, Delivery_Lines_df, Confirmed_Lines_df = Prepare_Files_Helpers.Prepare_Delivery_Lines_df_from_HQ_Deliveries(Settings=Settings, Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order=Purchase_Order, GUI=GUI)

            # Header
            PO_Invoices, PO_Invoice_Number_list = Generate_Invoice_Header.Generate_Invoice_Header(Settings=Settings, 
                                                                                                  Configuration=Configuration, 
                                                                                                  window=window, 
                                                                                                  Purchase_Order=Purchase_Order, 
                                                                                                  Purchase_Order_index=Purchase_Order_index,
                                                                                                  Purchase_Headers_df=Purchase_Headers_df, 
                                                                                                  PO_Confirmation_Number=PO_Confirmation_Number, 
                                                                                                  PO_Delivery_Number_list=PO_Delivery_Number_list, 
                                                                                                  PO_Delivery_Date_list=PO_Delivery_Date_list,
                                                                                                  Confirmed_Lines_df=Confirmed_Lines_df,
                                                                                                  Delivery_Lines_df=Delivery_Lines_df,
                                                                                                  Company_Information_df=Company_Information_df, 
                                                                                                  HQ_Communication_Setup_df=HQ_Communication_Setup_df,
                                                                                                  GUI=GUI)

            # Lines
            PO_Invoices, PO_Invoice_Table_Data_list = Generate_Invoice_Lines.Generate_Invoice_Lines(Settings=Settings, 
                                                                                                    Configuration=Configuration, 
                                                                                                    window=window, 
                                                                                                    Purchase_Order=Purchase_Order, 
                                                                                                    Purchase_Lines_df=Purchase_Lines_df, 
                                                                                                    PO_Invoices=PO_Invoices,
                                                                                                    PO_Invoice_Number_list=PO_Invoice_Number_list,
                                                                                                    PO_Delivery_Number_list=PO_Delivery_Number_list,
                                                                                                    Delivery_Lines_df=Delivery_Lines_df, 
                                                                                                    Confirmed_Lines_df=Confirmed_Lines_df,
                                                                                                    Items_df=Items_df,
                                                                                                    Items_Price_List_Detail_df=Items_Price_List_Detail_df,
                                                                                                    Country_ISO_Code_list=Country_ISO_Code_list,
                                                                                                    Tariff_Number_list=Tariff_Number_list,
                                                                                                    GUI=GUI)

            # Export 
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                Invoice_Content = PO_Invoices[Invoice_Index]
                Invoice_File_Name = f"INVOIC02_{Invoice_Number}_Test"
                if Export_NAV_Folder == True:
                    File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=Invoice_Content, HQ_File_Type_Path="HQ_Invoice_File_Path", File_Name=Invoice_File_Name, File_suffix="json", GUI=GUI)
                else:
                    File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=Invoice_Content, File_Name=Invoice_File_Name, File_suffix="json", GUI=GUI)
        else:
            pass
        
        # -------------------------------- Invoice PDF -------------------------------- #
        if Generate_Invoice_PDF == True:
            import Libs.Process.PDF_Generator as PDF_Generator
            for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                Invoice_Content = PO_Invoices[Invoice_Index]
                PO_Invoice_Table_Data = PO_Invoice_Table_Data_list[Invoice_Index]
                PO_Invoice_PDF = PDF_Generator.Generate_PDF(Settings=Settings, Configuration=Configuration, Document_Content=Invoice_Content, Document_Type="Order", Table_Data=PO_Invoice_Table_Data)

                # Export 
                # File name must be same as Invoice Number
                if Export_NAV_Folder == True:
                    File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PO_Invoice_PDF, HQ_File_Type_Path="HQ_PDF_File_Path", File_Name=Invoice_Number, File_suffix="pdf", GUI=GUI)
                else:
                    File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=PO_Invoice_PDF, File_Name=Invoice_Number, File_suffix="pdf", GUI=GUI)
        else:
            pass

def Process_BackBoneBilling(Settings: dict, 
                            Configuration: dict|None,
                            window: CTk|None,
                            Can_Process: bool, 
                            Buy_from_Vendor_No: str,
                            HQ_Communication_Setup_df: DataFrame, 
                            NVR_FS_Connect_df: DataFrame, 
                            Vendor_Service_Function_df: DataFrame, 
                            Company_Information_df: DataFrame,
                            Plants_df: DataFrame, 
                            Country_ISO_Code_list: list, 
                            Tariff_Number_list: list,
                            GUI: bool=True) -> None:
    
    # Get what should be prepared from Settings
    Generate_BB_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Use"]
    Generate_BB_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["PDF"]["Generate"]
    Generate_BB_IAL = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["IAL"]["Use"]
    Export_NAV_Folder = Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"]

    # -------------------------------- Invoice -------------------------------- #
    if Generate_BB_Invoice == True:
        import Libs.Process.BackBone_Billing.Generate_BB_Header as Generate_BB_Header
        import Libs.Process.BackBone_Billing.Generate_BB_Lines as Generate_BB_Lines

        # Header
        BB_Invoice, BB_Number, BB_Order_ID, BB_supplier_order_id, BB_Order_Date = Generate_BB_Header.Generate_BB_Header(Settings=Settings, 
                                                                                                                        Configuration=Configuration, 
                                                                                                                        window=window, 
                                                                                                                        Company_Information_df=Company_Information_df, 
                                                                                                                        HQ_Communication_Setup_df=HQ_Communication_Setup_df,
                                                                                                                        GUI=GUI)
        
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
                                                                                                                BB_Order_Date=BB_Order_Date,
                                                                                                                GUI=GUI)
                                                    
        # Update Lines
        BB_Invoice["invoice"]["invoice_item_list"] = BB_Invoice_Lines

        # Update Footer
        BB_Invoice["invoice"]["invoice_summary"]["total_item_num"] = round(number=BB_Lines_No, ndigits=2)
        BB_Invoice["invoice"]["invoice_summary"]["total_amount"] = round(number=BB_Total_Line_Amount, ndigits=2)
        BB_Invoice["invoice"]["invoice_summary"]["total_tax_amount"] = round(number=0, ndigits=2)

        # Export 
        BB_Invoice_File_Name = f"INVOIC02_{BB_Number}_Test"
        if Export_NAV_Folder == True:
            File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=BB_Invoice, HQ_File_Type_Path="HQ_Invoice_File_Path", File_Name=BB_Invoice_File_Name, File_suffix="json", GUI=GUI)
        else:
            File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=BB_Invoice, File_Name=BB_Invoice_File_Name, File_suffix="json", GUI=GUI)
    else:
        pass

    # -------------------------------- Invoice PDF -------------------------------- #
    if Generate_BB_Invoice_PDF == True:
        import Libs.Process.PDF_Generator as PDF_Generator
        BB_Invoice_PDF = PDF_Generator.Generate_PDF(Settings=Settings, Configuration=Configuration, Document_Content=BB_Invoice, Document_Type="Order", Table_Data=BB_Table_Data)

        # Export 
        # File name must be same as Invoice Number
        if Export_NAV_Folder == True:
            File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=BB_Invoice_PDF, HQ_File_Type_Path="HQ_PDF_File_Path", File_Name=BB_Number, File_suffix="pdf", GUI=GUI)
        else:
            File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=BB_Invoice_PDF, File_Name=BB_Number, File_suffix="pdf", GUI=GUI)
    else:
        pass

    # -------------------------------- IAL File -------------------------------- #
    if Generate_BB_IAL == True:
        print("Generate_BB_IAL")
    else:
        pass


def Process_Purchase_Return_Orders(Settings: dict, 
                                    Configuration: dict|None,
                                    window: CTk|None,
                                    headers: dict, 
                                    tenant_id: str, 
                                    NUS_version: str, 
                                    NOC: str, 
                                    Environment: str, 
                                    Company: str,
                                    Can_Process: bool, 
                                    HQ_Vendors_list: list,
                                    Purchase_Return_Headers_df: DataFrame, 
                                    Purchase_Return_Lines_df: DataFrame, 
                                    HQ_Communication_Setup_df: DataFrame, 
                                    Company_Information_df: DataFrame, 
                                    Country_ISO_Code_list: list, 
                                    HQ_Item_Transport_Register_df: DataFrame, 
                                    Items_df: DataFrame, 
                                    Items_Price_List_Detail_df: DataFrame, 
                                    NVR_FS_Connect_df: DataFrame, 
                                    UoM_df: DataFrame,
                                    Tariff_Number_list: list,
                                    GUI: bool=True) -> None:
    
    # Get what should be prepared from Settings
    Generate_PRO_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Use"]
    Generate_PRO_Credit_Memo = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Use"]
    Generate_PRO_Credit_Memo_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["PDF"]["Generate"]
    Export_NAV_Folder = Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"]

    # Generate Purchase Return Order List
    Purchase_Return_Orders_List = Purchase_Return_Headers_df["No"].to_list()

    for Purchase_Return_Order_index, Purchase_Return_Order in enumerate(Purchase_Return_Orders_List):
        # Purchase Return Order index --> because of multiple PROs processing 
        Purchase_Return_Order_index = str(Purchase_Return_Order_index)

        # Get Vendor for correct Export NAV folders for each PO (might be different Vendors)
        mask_PRO = Purchase_Return_Headers_df["No"] == Purchase_Return_Order
        Single_PRO_df = DataFrame(Purchase_Return_Headers_df[mask_PRO])
        Buy_from_Vendor_No = Single_PRO_df.iloc[0]["Buy_from_Vendor_No"]

        # -------------------------------- Confirmation -------------------------------- #
        if Generate_PRO_Confirmation == True:
            import Libs.Process.Purchase_Return_Orders.Generate_PRO_Confirmation_Header as Generate_PRO_Confirmation_Header
            import Libs.Process.Purchase_Return_Orders.Generate_PRO_Confirmation_Lines as Generate_PRO_Confirmation_Lines
            import Libs.Process.Purchase_Return_Orders.Generate_PRO_Confirmation_ATP as Generate_PRO_Confirmation_ATP

            # Header
            PRO_Confirmation_Header, PRO_Confirmation_Number = Generate_PRO_Confirmation_Header.Generate_PRO_CON_Header(Settings=Settings, 
                                                                                                                        Configuration=Configuration, 
                                                                                                                        window=window,
                                                                                                                        Purchase_Return_Order=Purchase_Return_Order,
                                                                                                                        Purchase_Return_Order_index=Purchase_Return_Order_index,
                                                                                                                        Purchase_Return_Headers_df=Purchase_Return_Headers_df,
                                                                                                                        Company_Information_df=Company_Information_df, 
                                                                                                                        HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                                                        HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df,
                                                                                                                        GUI=GUI)

            # Lines
            PRO_Confirmed_Lines_df, PRO_Confirmation_Lines, Total_Line_Amount, Lines_No = Generate_PRO_Confirmation_Lines.Generate_PRO_CON_Lines(Settings=Settings, 
                                                                                                                                            Configuration=Configuration, 
                                                                                                                                            window=window,
                                                                                                                                            Purchase_Return_Order=Purchase_Return_Order,
                                                                                                                                            Purchase_Return_Lines_df=Purchase_Return_Lines_df,
                                                                                                                                            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df,
                                                                                                                                            Items_df=Items_df,
                                                                                                                                            Items_Price_List_Detail_df=Items_Price_List_Detail_df, 
                                                                                                                                            UoM_df=UoM_df, 
                                                                                                                                            GUI=GUI)

            # ATP
            PRO_Confirmation_Lines = Generate_PRO_Confirmation_ATP.Generate_PRO_ATP_CON_Lines(Settings=Settings, Configuration=Configuration, window=window, PRO_Confirmed_Lines_df=PRO_Confirmed_Lines_df, PRO_Confirmation_Lines=PRO_Confirmation_Lines, GUI=GUI)

            # Put Header, Lines with ATP together
            PRO_Confirmation_Header["orderresponse"]["orderresponse_item_list"] = PRO_Confirmation_Lines

            # Update Footer
            PRO_Confirmation_Header["orderresponse"]["orderresponse_summary"]["total_item_num"] = Lines_No
            PRO_Confirmation_Header["orderresponse"]["orderresponse_summary"]["total_amount"] = round(number=Total_Line_Amount, ndigits=2)

            # Export 
            Confirmation_File_Name = f"ORDRSP_{PRO_Confirmation_Number}_Test"
            if Export_NAV_Folder == True:
                File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PRO_Confirmation_Header, HQ_File_Type_Path="HQ_R_O_Confirm_File_Path", File_Name=Confirmation_File_Name, File_suffix="json", GUI=GUI)
            else:
                File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=PRO_Confirmation_Header, File_Name=Confirmation_File_Name, File_suffix="json", GUI=GUI)
        else:
            pass

        # -------------------------------- Credit Memo -------------------------------- #
        if Generate_PRO_Credit_Memo == True:
            import Libs.Process.Purchase_Return_Orders.Generate_PRO_Invoice_Header as Generate_PRO_Invoice_Header
            import Libs.Process.Purchase_Return_Orders.Generate_PRO_Invoice_Lines as Generate_PRO_Invoice_Lines

            # Download Confirmation lines 
            PRO_Confirmed_Lines_df, PRO_Confirmation_Number = Prepare_Files_Helpers.Prepare_Confirmed_Lines_df_from_HQ_Confirmed(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Document_Number=Purchase_Return_Order, Document_Type="Return Order", Document_Lines_df=Purchase_Return_Lines_df, Items_df=Items_df, UoM_df=UoM_df, GUI=GUI)    

            # ---------------- Posted Return Shipments ---------------- #
            # PRO_Return_Shipment_list
            import Libs.Downloader.NAV_OData_API as NAV_OData_API
            if Can_Process == True:
                PRO_Return_Shipment_list = NAV_OData_API.Get_Purchase_Ret_Shipment_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Return_Orders_List=Purchase_Return_Orders_List, HQ_Vendors_list=HQ_Vendors_list, GUI=GUI)
            else:
                pass

            # HQ_Testing_PRO_Ship_Lines
            if Can_Process == True:
                PRO_Shipment_Lines_df = NAV_OData_API.Get_Purchase_Ret_Shipment_Lines_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, PRO_Return_Shipment_list=PRO_Return_Shipment_list, GUI=GUI)
                # Drop Duplicate rows amd reset index
                PRO_Shipment_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
                PRO_Shipment_Lines_df.reset_index(drop=True, inplace=True)
            else:
                pass

            # Header
            PRO_Credit_Memo, PRO_Credit_Number, PRO_Return_Shipment_Number = Generate_PRO_Invoice_Header.Generate_Credit_Memo_Header(Settings=Settings, 
                                                                                                                                        Configuration=Configuration, 
                                                                                                                                        window=window, 
                                                                                                                                        Purchase_Return_Order=Purchase_Return_Order, 
                                                                                                                                        Purchase_Return_Headers_df=Purchase_Return_Headers_df, 
                                                                                                                                        PRO_Confirmation_Number=PRO_Confirmation_Number, 
                                                                                                                                        PRO_Return_Shipment_list=PRO_Return_Shipment_list, 
                                                                                                                                        PRO_Confirmed_Lines_df=PRO_Confirmed_Lines_df,
                                                                                                                                        Company_Information_df=Company_Information_df, 
                                                                                                                                        HQ_Communication_Setup_df=HQ_Communication_Setup_df,
                                                                                                                                        GUI=GUI)

            # Lines
            PRO_Credit_Memo, PRO_Credit_Memo_Table_Data = Generate_PRO_Invoice_Lines.Generate_Credit_Memo_Lines(Settings=Settings, 
                                                                                                                Configuration=Configuration, 
                                                                                                                window=window, 
                                                                                                                Purchase_Return_Order=Purchase_Return_Order, 
                                                                                                                Purchase_Return_Lines_df=Purchase_Return_Lines_df, 
                                                                                                                PRO_Credit_Memo=PRO_Credit_Memo,
                                                                                                                PRO_Return_Shipment_Number=PRO_Return_Shipment_Number,
                                                                                                                PRO_Shipment_Lines_df=PRO_Shipment_Lines_df, 
                                                                                                                PRO_Confirmed_Lines_df=PRO_Confirmed_Lines_df,
                                                                                                                Items_df=Items_df,
                                                                                                                Items_Price_List_Detail_df=Items_Price_List_Detail_df,
                                                                                                                Country_ISO_Code_list=Country_ISO_Code_list,
                                                                                                                Tariff_Number_list=Tariff_Number_list,
                                                                                                                GUI=GUI)

            # Export 
            Credit_Memo_File_Name = f"INVOIC02_{PRO_Credit_Number}_Test"
            if Export_NAV_Folder == True:
                File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PRO_Credit_Memo, HQ_File_Type_Path="HQ_R_O_Cr_Memo_File_Path", File_Name=Credit_Memo_File_Name, File_suffix="json", GUI=GUI)
            else:
                File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=PRO_Credit_Memo, File_Name=Credit_Memo_File_Name, File_suffix="json", GUI=GUI)
        else:
            pass

        # -------------------------------- Credit Memo PDF -------------------------------- #
        if Generate_PRO_Credit_Memo_PDF == True:
            import Libs.Process.PDF_Generator as PDF_Generator 
            PRO_Credit_Memo_PDF = PDF_Generator.Generate_PDF(Settings=Settings, Configuration=Configuration, Document_Content=PRO_Credit_Memo, Document_Type="Return Order", Table_Data=PRO_Credit_Memo_Table_Data)

            # Export 
            # File name must be same as Credit Memo Number
            if Export_NAV_Folder == True:
                File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=PRO_Credit_Memo_PDF, HQ_File_Type_Path="HQ_PDF_File_Path", File_Name=PRO_Credit_Number, File_suffix="pdf", GUI=GUI)
            else:
                File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=PRO_Credit_Memo_PDF, File_Name=PRO_Credit_Number, File_suffix="pdf", GUI=GUI)
        else:
            pass
