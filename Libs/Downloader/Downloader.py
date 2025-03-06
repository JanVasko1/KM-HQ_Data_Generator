# Import Libraries
import pandas
from pandas import DataFrame

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions
import Libs.Azure.Authorization as Authorization
import Libs.Downloader.NAV_OData_API as NAV_OData_API
import Libs.Process.Prepare_Files as Prepare_Files

from customtkinter import CTkProgressBar, CTk

Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()

# ---------------------------------------------------------- Local Function ---------------------------------------------------------- #
def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar) -> None:
    Progress_Bar.step()
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, value: int) -> None:
    Progress_Bar.set(value=value)
    window.update_idletasks()


# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Get_Companies_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str,) -> list:
    Companies_list = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    Companies_list = NAV_OData_API.Get_Companies(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment)
    return Companies_list

def Get_Logistic_Process_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str) -> list:
    Company = Data_Functions.Company_Name_prepare(Company=Company)
    Log_Process_List = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    Log_Process_List = NAV_OData_API.Get_HQ_Testing_Logistic_Process_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    return Log_Process_List

def Get_HQ_Vendors_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str) -> list:
    Company = Data_Functions.Company_Name_prepare(Company=Company)
    HQ_Vendors_list = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    return HQ_Vendors_list

def Get_Orders_List(Configuration: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Document_Type: str, Logistic_Process_Filter: str) -> list:
    Company = Data_Functions.Company_Name_prepare(Company=Company)
    Can_Process = True
    Purchase_Header_list = []

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
        Purchase_Header_list = NAV_OData_API.Get_Purchase_Headers_list_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Document_Type=Document_Type, HQ_Vendors_list=HQ_Vendors_list, Logistic_Process_Filter=Logistic_Process_Filter)
        if len(Purchase_Header_list) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"There is no purchase header downloaded that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass
    else:
        pass

    return Purchase_Header_list


def Download_Data_Purchase_Orders(Settings: dict, Configuration: dict, window: CTk, Progress_Bar: CTkProgressBar, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Order_list: list) -> bool:
    Company = Data_Functions.Company_Name_prepare(Company=Company)

    Progress_Bar.configure(determinate_speed = round(number=50 / 22, ndigits=3), progress_color="#517A31")
    Can_Process = True

    Purchase_Headers_df = DataFrame()
    Purchase_Lines_df = DataFrame()
    HQ_Communication_Setup_df = DataFrame()
    Company_Information_df = DataFrame()
    Country_ISO_Code_list = []
    CPDI_Level_list = []
    CPDI_Status_list = []
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
    Shipment_Method_list = []
    Shipping_Agent_list = []
    Tariff_Number_list = []
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
        # Drop Duplicate rows amd reset index
        HQ_Communication_Setup_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_Communication_Setup_df.reset_index(drop=True, inplace=True)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        print("\n----------HQ_Communication_Setup_df----------")
        print(HQ_Communication_Setup_df)
    

    # HQ_Testing_NVR_FS_Connect
    if Can_Process == True:
        NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list)
        if NVR_FS_Connect_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            NVR_FS_Connect_df.drop_duplicates(inplace=True, ignore_index=True)
            NVR_FS_Connect_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            print("\n----------NVR_FS_Connect_df----------")
            print(NVR_FS_Connect_df)
    else:
        pass

    # HQ_Testing_Purchase_Headers
    if Can_Process == True:
        Purchase_Headers_df, Purchase_Order_list = NAV_OData_API.Get_Purchase_Headers_info_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, HQ_Vendors_list=HQ_Vendors_list)
        if Purchase_Headers_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"There is no purchase header downloaded that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Purchase_Headers_df.drop_duplicates(inplace=True, ignore_index=True)
            Purchase_Headers_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            print("\n----------Purchase_Headers_df----------")
            print(Purchase_Headers_df)
    else:
        pass

    # HQ_Testing_Purchase_Lines
    if Can_Process == True:
        Purchase_Lines_df, Items_list = NAV_OData_API.Get_Purchase_Lines_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list)
        if Purchase_Lines_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"There is no purchase lines downloaded, that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Purchase_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
            Purchase_Lines_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            print("\n----------Purchase_Lines_df----------")
            print(Purchase_Lines_df)
    else:
        pass

    # HQ_Testing_HQ_Item_Transport_Register
    if Can_Process == True:
        HQ_Item_Transport_Register_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, Document_Type="Order")
        if HQ_Item_Transport_Register_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"All Order/s you select were not exported by HQ, canceling download. Please Export them first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            HQ_Item_Transport_Register_df.drop_duplicates(inplace=True, ignore_index=True)
            HQ_Item_Transport_Register_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            print("\n----------HQ_Item_Transport_Register_df----------")
            print(HQ_Item_Transport_Register_df)
    else:
        pass

    # HQ_Testing_Items
    if Can_Process == True:
        Items_df, Substitution_Item_list, BOM_Item_list, BEU_Set_Item_list, Item_Tracking_Code_list = NAV_OData_API.Get_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list)
        if Items_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"It was not possible to download any Item detail information from Item Cards.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Items_df.drop_duplicates(inplace=True, ignore_index=True)
            Items_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            print("\n----------Items_df----------")
            print(Items_df)
    else:
        pass

    # HQ_Testing_Items_BOM
    if Can_Process == True:
        Items_BOMs_df, Items_For_BOM_df = NAV_OData_API.Get_Items_BOM_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=BOM_Item_list)
        Items_BOMs_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_BOMs_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_BOMs_df----------")
        print(Items_BOMs_df)
        Items_For_BOM_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_For_BOM_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_For_BOM_df----------")
        print(Items_For_BOM_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Items_Substitutions
    if Can_Process == True:
        Items_Substitutions_df, Items_For_Substitution_df = NAV_OData_API.Get_Items_Substitutions_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Substitution_Item_list)
        Items_Substitutions_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Substitutions_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_Substitutions_df----------")
        print(Items_Substitutions_df)
        Items_For_Substitution_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_For_Substitution_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_For_Substitution_df----------")
        print(Items_For_Substitution_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Items_Connected_Items
    if Can_Process == True:
        Items_Connected_Items_df, Items_For_Connected_Items_df = NAV_OData_API.Get_Items_Connected_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, Connection_Type_list=["Free of Charge", "Distribution"])
        Items_Connected_Items_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Connected_Items_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_Connected_Items_df----------")
        print(Items_Connected_Items_df)
        Items_For_Connected_Items_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_For_Connected_Items_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_For_Connected_Items_df----------")
        print(Items_For_Connected_Items_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass
    
    # Concat Items
    if Can_Process == True:
        Items_df = pandas.DataFrame(data=pandas.concat(objs=[Items_df, Items_For_BOM_df, Items_For_Substitution_df, Items_For_Connected_Items_df]))
        # Update Item List for all Items
        Items_list = Items_df["No"].tolist()
        Items_list = list(set(Items_list))

        # Delete duplicate rows from Items_df
        Items_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_df.reset_index(drop=True, inplace=True)

        print("\n----------Items_list -> Concatenate----------")
        print(Items_list)
        print("\n----------Items_df -> All----------")
        print(Items_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Items_Price_Detail_List
    if Can_Process == True:
        Active_Price_Lists_df, BEU_Price_list = NAV_OData_API.Get_Items_Price_Lists_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Active_Price_Lists_df----------")
        print(Active_Price_Lists_df)
        Items_Price_List_Detail_df = NAV_OData_API.Get_Items_Price_List_detail_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, BEU_Price_list=BEU_Price_list, Amount_Type_List=["Price", "Price & Discount"])
        # Drop Duplicate rows
        Items_Price_List_Detail_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Price_List_Detail_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_Price_List_Detail_df----------")
        print(Items_Price_List_Detail_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Items_Tracking_Codes
    if Can_Process == True:
        Items_Tracking_df = NAV_OData_API.Get_Items_Tracking_Codes_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Item_Tracking_Code_list=Item_Tracking_Code_list)
        Items_Tracking_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Tracking_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_Tracking_df----------")
        print(Items_Tracking_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Items_UoM
    if Can_Process == True:
        Items_UoM_df = NAV_OData_API.Get_Items_UoM_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list)
        Items_UoM_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_UoM_df.reset_index(drop=True, inplace=True)
        print("\n----------Items_UoM_df----------")
        print(Items_UoM_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Plans
    if Can_Process == True:
        Plants_df = NAV_OData_API.Get_Plants_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        Plants_df.drop_duplicates(inplace=True, ignore_index=True)
        Plants_df.reset_index(drop=True, inplace=True)
        print("\n----------Plants_df----------")
        print(Plants_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Shipment_Method
    if Can_Process == True:
        Shipment_Method_list = NAV_OData_API.Get_Shipment_Method_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Shipment_Method_list----------")
        print(Shipment_Method_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Shipping_Agent
    if Can_Process == True:
        Shipping_Agent_list = NAV_OData_API.Get_Shipping_Agent_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Shipping_Agent_list----------")
        print(Shipping_Agent_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Tariff_Numbers
    if Can_Process == True:
        Tariff_Number_list = NAV_OData_API.Get_Tariff_Number_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Tariff_Number_list----------")
        print(Tariff_Number_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

     # HQ_Testing_Company_Information
    if Can_Process == True:
        Company_Information_df = NAV_OData_API.Get_Company_Information_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        Company_Information_df.drop_duplicates(inplace=True, ignore_index=True)
        Company_Information_df.reset_index(drop=True, inplace=True)
        print("\n----------Company_Information_df----------")
        print(Company_Information_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Country_Regions
    if Can_Process == True:
        Country_ISO_Code_list = NAV_OData_API.Get_Country_ISO_Code_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Country_ISO_Code_list----------")
        print(Country_ISO_Code_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_HQ_CPDI_Levels
    if Can_Process == True:
        CPDI_Level_list = NAV_OData_API.Get_CPDI_Level_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------CPDI_Level_list----------")
        print(CPDI_Level_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # CPDI_Status_list
    if Can_Process == True:
        CPDI_Status_list = NAV_OData_API.Get_CPDI_Status_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------CPDI_Status_list----------")
        print(CPDI_Status_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_UoM
    if Can_Process == True:
        UoM_df =  NAV_OData_API.Get_UoM_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        UoM_df.drop_duplicates(inplace=True, ignore_index=True)
        UoM_df.reset_index(drop=True, inplace=True)
        print("\n----------UoM_df----------")
        print(UoM_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    if Can_Process == True:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1)
        Prepare_Files.Process_Purchase_Orders(
            Settings=Settings,
            Can_Process=Can_Process, 
            Purchase_Headers_df=Purchase_Headers_df, 
            Purchase_Lines_df=Purchase_Lines_df, 
            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
            Company_Information_df=Company_Information_df, 
            Country_ISO_Code_list=Country_ISO_Code_list, 
            CPDI_Level_list=CPDI_Level_list, 
            CPDI_Status_list=CPDI_Status_list, 
            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, 
            Items_df=Items_df, 
            Items_BOMs_df=Items_BOMs_df, 
            Items_Substitutions_df=Items_Substitutions_df, 
            Items_Connected_Items_df=Items_Connected_Items_df, 
            Items_Price_List_Detail_df=Items_Price_List_Detail_df, 
            Items_Tracking_df=Items_Tracking_df, 
            Items_UoM_df=Items_UoM_df, 
            NVR_FS_Connect_df=NVR_FS_Connect_df, 
            Plants_df=Plants_df, 
            Shipment_Method_list=Shipment_Method_list, 
            Shipping_Agent_list=Shipping_Agent_list, 
            Tariff_Number_list=Tariff_Number_list, 
            UoM_df=UoM_df)
    else:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=0)
    
    return Can_Process


def Download_Data_BackBoneBilling(Settings: dict, 
                                  Configuration: dict, 
                                  window: CTk, 
                                  Progress_Bar: CTkProgressBar,
                                  NUS_version: str, 
                                  NOC: str,
                                  Environment: str, 
                                  Company: str, 
                                  Buy_from_Vendor_No: str) -> bool:
    Company = Data_Functions.Company_Name_prepare(Company=Company)

    Progress_Bar.configure(determinate_speed = round(number=50 / 6, ndigits=3), progress_color="#517A31")
    Can_Process = True

    HQ_Communication_Setup_df = DataFrame()
    NVR_FS_Connect_df = DataFrame()
    Vendor_Service_Function_df = DataFrame()
    Plants_df = DataFrame()
    Country_ISO_Code_list = []
    Tariff_Number_list = []

    # Headers for all pages
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    print("\n----------HQ_Communication_Setup_df----------")
    print(HQ_Communication_Setup_df)
    if HQ_Communication_Setup_df.empty:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        Can_Process = False
    else:
        # Drop Duplicate rows amd reset index
        HQ_Communication_Setup_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_Communication_Setup_df.reset_index(drop=True, inplace=True)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)

    # HQ_Testing_NVR_FS_Connect
    if Can_Process == True:
        NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list)
        print("\n----------NVR_FS_Connect_df----------")
        print(NVR_FS_Connect_df)
        if NVR_FS_Connect_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            NVR_FS_Connect_df.drop_duplicates(inplace=True, ignore_index=True)
            NVR_FS_Connect_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # Vendor_Service_Function_df
    if Can_Process == True:
        Vendor_Service_Function_df = NAV_OData_API.Get_Vendor_Service_Functions_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No=Buy_from_Vendor_No)
        print("\n----------Vendor_Service_Function_df----------")
        print(Vendor_Service_Function_df)
        if Vendor_Service_Function_df.empty:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"It was not possible to download any Vendor Service Functions detail so program cannot build Invoice.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Vendor_Service_Function_df.drop_duplicates(inplace=True, ignore_index=True)
            Vendor_Service_Function_df.reset_index(drop=True, inplace=True)
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Plans
    if Can_Process == True:
        Plants_df = NAV_OData_API.Get_Plants_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        Plants_df.drop_duplicates(inplace=True, ignore_index=True)
        Plants_df.reset_index(drop=True, inplace=True)
        print("\n----------Plants_df----------")
        print(Plants_df)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Country_Regions
    if Can_Process == True:
        Country_ISO_Code_list = NAV_OData_API.Get_Country_ISO_Code_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Country_ISO_Code_list----------")
        print(Country_ISO_Code_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    # HQ_Testing_Tariff_Numbers
    if Can_Process == True:
        Tariff_Number_list = NAV_OData_API.Get_Tariff_Number_list(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
        print("\n----------Tariff_Number_list----------")
        print(Tariff_Number_list)
        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
    else:
        pass

    if Can_Process == True:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1)
        Prepare_Files.Process_BackBoneBilling(
            Settings=Settings,
            Can_Process=Can_Process, 
            Buy_from_Vendor_No=Buy_from_Vendor_No,
            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
            NVR_FS_Connect_df=NVR_FS_Connect_df, 
            Vendor_Service_Function_df=Vendor_Service_Function_df,
            Plants_df=Plants_df,
            Country_ISO_Code_list=Country_ISO_Code_list,  
            Tariff_Number_list=Tariff_Number_list)
    else:
        Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=0)

    return Can_Process
        

def Download_Data_Return_Order(Settings: dict, Configuration: dict, window: CTk, Progress_Bar: CTkProgressBar, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Return_Orders_List: list) -> bool:
    Company = Data_Functions.Company_Name_prepare(Company=Company)

    Progress_Bar.configure(determinate_speed = round(number=50 / 6, ndigits=3), progress_color="#517A31")
    Can_Process = True

    # Headers for all pages
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}
    
    # TODO - Completaly finish

    return Can_Process