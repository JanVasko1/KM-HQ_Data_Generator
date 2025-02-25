# Import Libraries
from pandas import DataFrame

import Libs.Defaults_Lists as Defaults_Lists
import Libs.Azure.Authorization as Authorization
import Libs.Downloader.NAV_OData_API as NAV_OData_API

client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()

# Get Access Token
def Download_Data_Purchase_Orders(Settings: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Order_list: list) -> list[DataFrame]:
    # Headers for all pages
    access_token = Authorization.Exchange_OAuth(Settings=Settings, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_Purchase_Headers
    Purchase_Headers_df, Buy_from_Vendor_No_list = NAV_OData_API.Get_Purchase_Headers_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list)

    # HQ_Testing_Purchase_Lines
    Purchase_Lines_df, Items_list = NAV_OData_API.Get_Purchase_Lines_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list)

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list = NAV_OData_API.Get_HQ_Communication_Setup_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No_list=Buy_from_Vendor_No_list)

    # HQ_Testing_Company_Information
    Company_Information_df = NAV_OData_API.Get_Company_Information_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_Country_Regions
    Country_Regions_df = NAV_OData_API.Get_Country_Regions_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_HQ_CPDI_Levels
    HQ_CPDI_Levels_df = NAV_OData_API.Get_HQ_CPDI_Levels_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_HQ_CPDI_Status
    HQ_CPDI_Status_df = NAV_OData_API.Get_HQ_CPDI_Status_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_HQ_Item_Transport_Register

    # HQ_Testing_Items

    # HQ_Testing_Items_BOM

    # HQ_Testing_Items_Substitutions

    # HQ_Testing_Items_Tracking_Codes
    Item_Tracking_df = NAV_OData_API.Get_Tracking_Codes_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_Items_UoM

    # HQ_Testing_NVR_FS_Connect
    NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list)

    # HQ_Testing_Plans
    Plants_df = NAV_OData_API.Get_Plants_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_Shipment_Method
    Shipment_Method_df = NAV_OData_API.Get_Shipment_Method_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_Shipping_Agent
    Shipping_Agent_df = NAV_OData_API.Get_Shipping_Agent_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_Tariff_Numbers
    Tariff_Numbers_df = NAV_OData_API.Get_Tariff_Numbers_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)

    # HQ_Testing_UoM
    print("Finished")

def Download_Data_Purchase_Invoice(Settings: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Buy_from_Vendor_No_list: list) -> list[DataFrame]:
    # Headers for all pages
    access_token = Authorization.Exchange_OAuth(Settings=Settings, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}
    
    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list = NAV_OData_API.Get_HQ_Communication_Setup_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No_list=Buy_from_Vendor_No_list)

    # HQ_Testing_NVR_FS_Connect
    NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list)

    # HQ_Testing_Vendor_Service_Functions
    Vendor_Service_Functions_df = NAV_OData_API.Get_Vendor_Service_Functions_df(headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No_list=Buy_from_Vendor_No_list)

    print("Finished")