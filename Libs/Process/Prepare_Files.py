# Import Libraries
from pandas import DataFrame

import Libs.File_Manipulation as File_Manipulation

from customtkinter import CTk

def Process_Purchase_Orders(Settings: dict, 
                            Configuration: dict,
                            window: CTk,
                            Can_Process: bool, 
                            Purchase_Headers_df: DataFrame, 
                            Purchase_Lines_df: DataFrame, 
                            HQ_Communication_Setup_df: DataFrame, 
                            Company_Information_df: DataFrame, 
                            Country_ISO_Code_list: list, 
                            CPDI_Level_list: list, 
                            CPDI_Status_list: list, 
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

        # ---------------- Confirmation ---------------- #
        if Generate_Confirmation == True:
            import Libs.Process.Purchase_Orders.PO_CON_Header_Generator as PO_CON_Header_Generator
            import Libs.Process.Purchase_Orders.PO_CON_Lines_Generator as PO_CON_Lines_Generator
            import Libs.Process.Purchase_Orders.PO_CON_ATP_Generator as PO_CON_ATP_Generator

            # Header
            PO_Confirmation, PO_Confirmation_Number = PO_CON_Header_Generator.Generate_PO_CON_Header(Settings=Settings, 
                                                                                    Configuration=Configuration, 
                                                                                    window=window,
                                                                                    Purchase_Order=Purchase_Order,
                                                                                    Purchase_Headers_df=Purchase_Headers_df,
                                                                                    Company_Information_df=Company_Information_df, 
                                                                                    HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
                                                                                    HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df)
            
            # Lines
            Lines_df, PO_Confirmation_Lines, Total_Line_Amount, Lines_No = PO_CON_Lines_Generator.Generate_PO_CON_Lines(Settings=Settings, 
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
            PO_CON_ATP_Generator.Generate_PO_ATP_CON_Lines(Settings=Settings, Configuration=Configuration, window=window, Lines_df=Lines_df, PO_Confirmation_Lines=PO_Confirmation_Lines)

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

            # Prepare Dataframe for Delivery
            mask_Canceled_Lines = Lines_df["cancelled"] == False
            mask_Canceled_Lines = Lines_df["discontinued"] == False
            Lines_df = Lines_df[mask_Canceled_Lines & mask_Canceled_Lines]  
        else:
            pass

        # ---------------- CPDI ---------------- #
        if Generate_CPDI == True:
            # TIP --> Pozor na situaci, kdy CPDI bude generované v jiném běhu než Delivery --> pak by se měl program zeptat na základě čeho chceme Delivery dělat
            print("Process_CPDI")
        else:
            pass

        # ---------------- PreAdvice ---------------- #
        if Generate_PreAdvice == True:
            # TIP --> Pozor na situaci, kdy Preadvice bude generované v jiném běhu než Confirmation / Delivery --> pak by se měl program zeptat na základě čeho chceme PreAdvice dělat
            # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
            print("Process_PreAdvice")
        else:
            pass

        # ---------------- Delivery ---------------- #
        if Generate_Delivery == True:
            # TIP --> Pozor na situaci, kdy Delivery bude generované v jiném běhu než Confirmation --> pak by se měl program zeptat na základě čeho chceme Delivery dělat
            # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
            print("Process_Delivery")
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
        import Libs.Process.BackBone_Billing.BB_Header_Generator as BB_Header_Generator
        import Libs.Process.BackBone_Billing.BB_Lines_Generator as BB_Lines_Generator

        # Header
        BB_Invoice, BB_Number, BB_Order_ID, BB_supplier_order_id, BB_Order_Date = BB_Header_Generator.Generate_BB_Header(Settings=Settings, 
                                                                                                                        Configuration=Configuration, 
                                                                                                                        window=window, 
                                                                                                                        Company_Information_df=Company_Information_df, 
                                                                                                                        HQ_Communication_Setup_df=HQ_Communication_Setup_df)
        
        # Lines
        BB_Invoice_Lines, Lines_No, Total_Line_Amount, Table_Data = BB_Lines_Generator.Generate_BB_Lines(Settings=Settings, 
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
