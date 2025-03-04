# Import Libraries
import pandas
from pandas import DataFrame

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Azure.Authorization as Authorization
import Libs.Downloader.NAV_OData_API as NAV_OData_API

client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_env()

def Get_Companies_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str,) -> list:
    Companies_list = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    Companies_list = NAV_OData_API.Get_Companies(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment)
    return Companies_list

def Get_Logistic_Process_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str) -> list:
    Log_Process_List = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    Log_Process_List = NAV_OData_API.Get_HQ_Testing_Logistic_Process_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    return Log_Process_List

def Get_Orders_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Document_Type: str, Logistic_Process_Filter: str) -> list:
    Can_Process = True
    Purchase_Order_list = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    if HQ_Communication_Setup_df.empty:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        Can_Process = False
    else:
        pass

    # HQ_Testing_Purchase_Headers
    if Can_Process == True:
        Purchase_Order_list = NAV_OData_API.Get_Purchase_Headers_list_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Document_Type=Document_Type, HQ_Vendors_list=HQ_Vendors_list, Logistic_Process_Filter=Logistic_Process_Filter)
        if len(Purchase_Order_list) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"There is no purchase header downloaded that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass
    else:
        pass

    return Purchase_Order_list

# Get Access Token
def Download_Data_Purchase_Orders(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Order_list: list) -> list[DataFrame]:
    Can_Process = True

    Purchase_Headers_df = DataFrame()
    Purchase_Lines_df = DataFrame()
    HQ_Communication_Setup_df = DataFrame()
    Company_Information_df = DataFrame()
    Country_Regions_df = DataFrame()
    HQ_CPDI_Levels_df = DataFrame()
    HQ_CPDI_Status_df = DataFrame()
    HQ_Item_Transport_Register_df = DataFrame()
    Items_df = DataFrame()
    Items_For_BOM_df = DataFrame()
    Items_For_Substitution_df = DataFrame()
    Items_For_Connected_Items_df = DataFrame()
    Items_BOMs_df = DataFrame()
    Items_Substitutions_df = DataFrame()
    Items_Connected_Items_df = DataFrame()
    Items_Price_List_Detail_df = DataFrame()
    Items_Tracking_df = DataFrame()
    Items_UoM_df = DataFrame()
    NVR_FS_Connect_df = DataFrame()
    Plants_df = DataFrame()
    Shipment_Method_df = DataFrame()
    Shipping_Agent_df = DataFrame()
    Tariff_Numbers_df = DataFrame()
    UoM_df = DataFrame()

    # Headers for all pages
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    if HQ_Communication_Setup_df.empty:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        Can_Process = False
    else:
        pass

    # HQ_Testing_NVR_FS_Connect
    if Can_Process == True:
        NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list)
        if NVR_FS_Connect_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            pass
    else:
        pass

    # HQ_Testing_Purchase_Headers
    if Can_Process == True:
        Purchase_Headers_df, Purchase_Order_list = NAV_OData_API.Get_Purchase_Headers_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, HQ_Vendors_list=HQ_Vendors_list)
        if Purchase_Headers_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"There is no purchase header downloaded that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            pass
    else:
        pass

    # HQ_Testing_Purchase_Lines
    if Can_Process == True:
        Purchase_Lines_df, Items_list = NAV_OData_API.Get_Purchase_Lines_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list)
        if Purchase_Lines_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"There is no purchase lines downloaded, that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            pass
    else:
        pass

    # HQ_Testing_HQ_Item_Transport_Register
    if Can_Process == True:
        HQ_Item_Transport_Register_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, Document_Type="Order")
        if HQ_Item_Transport_Register_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"All Order/s you select were not exported by HQ, canceling download. Please Export them first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            pass
    else:
        pass

    # HQ_Testing_Items
    if Can_Process == True:
        Items_df, Substitution_Item_list, BOM_Item_list, BEU_Set_Item_list, Item_Tracking_Code_list = NAV_OData_API.Get_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list)
        if Items_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"It was not possible to download any Item detail information from Item Cards.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            pass
    else:
        pass

    # HQ_Testing_Items_BOM
    if Can_Process == True:
        Items_BOMs_df, Items_For_BOM_df = NAV_OData_API.Get_Items_BOM_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=BOM_Item_list)
    else:
        pass

    # HQ_Testing_Items_Substitutions
    if Can_Process == True:
        Items_Substitutions_df, Items_For_Substitution_df = NAV_OData_API.Get_Items_Substitutions_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Substitution_Item_list)
    else:
        pass

    # HQ_Testing_Items_Connected_Items
    if Can_Process == True:
        Items_Connected_Items_df, Items_For_Connected_Items_df = NAV_OData_API.Get_Items_Connected_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, Connection_Type_list=["Free of Charge", "Distribution"])
    else:
        pass
    
    # Concat Items
    if Can_Process == True:
        Items_df = pandas.concat(objs=[Items_df, Items_For_BOM_df, Items_For_Substitution_df, Items_For_Connected_Items_df])
    else:
        pass

    # HQ_Testing_Items_Price_Detail_List
    if Can_Process == True:
        Active_Price_Lists_df, BEU_Price_list = NAV_OData_API.Get_Items_Price_Lists_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        Items_Price_List_Detail_df = NAV_OData_API.Get_Items_Price_List_detail_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, BEU_Price_list=BEU_Price_list, Amount_Type_List=["Price", "Price & Discount"])
    else:
        pass

    # HQ_Testing_Items_Tracking_Codes
    if Can_Process == True:
        Items_Tracking_df = NAV_OData_API.Get_Items_Tracking_Codes_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Item_Tracking_Code_list=Item_Tracking_Code_list)
    else:
        pass

    # HQ_Testing_Items_UoM
    if Can_Process == True:
        Items_UoM_df = NAV_OData_API.Get_Items_UoM_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list)
    else:
        pass

    # HQ_Testing_Plans
    if Can_Process == True:
        Plants_df = NAV_OData_API.Get_Plants_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_Shipment_Method
    if Can_Process == True:
        Shipment_Method_df = NAV_OData_API.Get_Shipment_Method_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_Shipping_Agent
    if Can_Process == True:
        Shipping_Agent_df = NAV_OData_API.Get_Shipping_Agent_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_Tariff_Numbers
    if Can_Process == True:
        Tariff_Numbers_df = NAV_OData_API.Get_Tariff_Numbers_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

     # HQ_Testing_Company_Information
    if Can_Process == True:
        Company_Information_df = NAV_OData_API.Get_Company_Information_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_Country_Regions
    if Can_Process == True:
        Country_Regions_df = NAV_OData_API.Get_Country_Regions_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_HQ_CPDI_Levels
    if Can_Process == True:
        HQ_CPDI_Levels_df = NAV_OData_API.Get_HQ_CPDI_Levels_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_HQ_CPDI_Status
    if Can_Process == True:
        HQ_CPDI_Status_df = NAV_OData_API.Get_HQ_CPDI_Status_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    # HQ_Testing_UoM
    if Can_Process == True:
        UoM_df =  NAV_OData_API.Get_UoM_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    else:
        pass

    return Can_Process, Purchase_Headers_df, Purchase_Lines_df, HQ_Communication_Setup_df, Company_Information_df, Country_Regions_df, HQ_CPDI_Levels_df, HQ_CPDI_Status_df, HQ_Item_Transport_Register_df, Items_df, Items_BOMs_df, Items_Substitutions_df, Items_Connected_Items_df, Items_Price_List_Detail_df, Items_Tracking_df, Items_UoM_df, NVR_FS_Connect_df, Plants_df, Shipment_Method_df, Shipping_Agent_df, Tariff_Numbers_df, UoM_df
        

def Download_Data_Purchase_Invoice(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Buy_from_Vendor_No_list: list) -> list[DataFrame]:
    # TODO --> Completaly finish
    # Headers for all pages
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}
    
    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No_list=Buy_from_Vendor_No_list)

    # HQ_Testing_NVR_FS_Connect
    NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list)

    # HQ_Testing_Vendor_Service_Functions
    Vendor_Service_Functions_df = NAV_OData_API.Get_Vendor_Service_Functions_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No_list=Buy_from_Vendor_No_list)

    print("Finished")


def Download_Data_Return_Order(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Return_Order_list: list) -> list[DataFrame]:
    # Headers for all pages
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    print("Finished")