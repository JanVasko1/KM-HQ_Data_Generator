from pandas import DataFrame


def Process_Purchase_Orders(Settings: dict, Can_Process: bool, Purchase_Headers_df: DataFrame, Purchase_Lines_df: DataFrame, HQ_Communication_Setup_df: DataFrame, Company_Information_df: DataFrame, Country_Regions_df: DataFrame, HQ_CPDI_Levels_df: DataFrame, HQ_CPDI_Status_df: DataFrame, HQ_Item_Transport_Register_df: DataFrame, Items_df: DataFrame, Items_BOMs_df: DataFrame, Items_Substitutions_df: DataFrame, Items_Connected_Items_df: DataFrame, Items_Price_List_Detail_df: DataFrame, Items_Tracking_df: DataFrame, Items_UoM_df: DataFrame, NVR_FS_Connect_df: DataFrame, Plants_df: DataFrame, Shipment_Method_df: DataFrame, Shipping_Agent_df: DataFrame, Tariff_Numbers_df: DataFrame, UoM_df: DataFrame) -> None:
    # Get what should be prepared from Settings
    Generate_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Use"]
    Generate_CPDI = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Use"]
    Generate_PreAdvice = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Use"]
    Generate_Delivery = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Use"]
    Generate_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Use"]
    Generate_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["PDF"]["Generate"]

    
    if Generate_Confirmation == True:
        print("Process_Confirmation")
    else:
        pass

    if Generate_CPDI == True:
        print("Process_CPDI")
    else:
        pass

    if Generate_PreAdvice == True:
        print("Process_PreAdvice")
    else:
        pass

    if Generate_Delivery == True:
        print("Process_Delivery")
    else:
        pass

    if Generate_Invoice == True:
        print("Process_Invoice")
    else:
        pass

    if Generate_Invoice_PDF == True:
        print("Process_Invoice")
    else:
        pass

def Process_BackBoneBilling() -> None:
    print("Process_Purchase_Return_Orders")
    pass

def Process_Purchase_Return_Orders() -> None:
    print("Process_Purchase_Return_Orders")
    pass