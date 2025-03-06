from pandas import DataFrame


def Process_Purchase_Orders(Settings: dict, 
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

    # Generate Purchase Order List

    if Generate_Confirmation == True:
        print("Process_Confirmation")
    else:
        pass

    if Generate_CPDI == True:
        # TIP --> Pozor na situaci, kdy CPDI bude generované v jiném běhu než Delivery --> pak by se měl program zeptat na základě čeho chceme Delivery dělat
        print("Process_CPDI")
    else:
        pass

    if Generate_PreAdvice == True:
        # TIP --> Pozor na situaci, kdy Preadvice bude generované v jiném běhu než Confirmation / Delivery --> pak by se měl program zeptat na základě čeho chceme PreAdvice dělat
        # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
        print("Process_PreAdvice")
    else:
        pass

    if Generate_Delivery == True:
        # TIP --> Pozor na situaci, kdy Delivery bude generované v jiném běhu než Confirmation --> pak by se měl program zeptat na základě čeho chceme Delivery dělat
        # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
        print("Process_Delivery")
    else:
        pass

    if Generate_Invoice == True:
        # TIP --> Pozor na situaci, kdy Invoice bude generovaná v jiném běhu než Delivery --> pak by se měl program zeptat na základě čeho chceme Invoice dělat
        # TIP --> Pozor obsahuje informace i z Confirmation (Line No a číslo dokumentu)
        print("Process_Invoice")
    else:
        pass

    if Generate_Invoice_PDF == True:
        print("Generate_Invoice_PDF")
    else:
        pass

def Process_BackBoneBilling(Settings: dict, 
                            Can_Process: bool, 
                            Buy_from_Vendor_No: str,
                            HQ_Communication_Setup_df: DataFrame, 
                            NVR_FS_Connect_df: DataFrame, 
                            Vendor_Service_Function_df: DataFrame, 
                            Plants_df: DataFrame, 
                            Country_ISO_Code_list: list, 
                            Tariff_Number_list: list) -> None:
    # Get what should be prepared from Settings
    Generate_BB_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Use"]
    Generate_BB_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["PDF"]["Generate"]
    Generate_BB_IAL = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["IAL"]["Use"]


    if Generate_BB_Invoice == True:
        print("Generate_BB_Invoice")
    else:
        pass

    if Generate_BB_Invoice_PDF == True:
        print("Generate_BB_Invoice_PDF")
    else:
        pass

    if Generate_BB_IAL == True:
        print("Generate_BB_IAL")
    else:
        pass


def Process_Purchase_Return_Orders(Settings: dict) -> None:
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
