# Import Libraries
import pandas
from pandas import DataFrame
from fastapi import HTTPException

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions
import Libs.Azure.Authorization as Authorization
import Libs.Downloader.NAV_OData_API as NAV_OData_API
import Libs.Process.Prepare_Files as Prepare_Files

from customtkinter import CTkProgressBar, CTk, CTkFrame, StringVar
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

# ---------------------------------------------------------- Local Function ---------------------------------------------------------- #
def Progress_Bar_step(window: CTk|None, Progress_Bar: CTkProgressBar|None) -> None:
    Progress_Bar.step()
    window.update_idletasks()

def Progress_Bar_set(window: CTk|None, Progress_Bar: CTkProgressBar|None, value: int) -> None:
    Progress_Bar.set(value=value)
    window.update_idletasks()


# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Get_Companies_List(Configuration: dict|None, window: CTk|None, NUS_version: str, NOC: str, Environment: str, Companies_Frame_Var: CTkScrollableDropdown) -> list:
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Companies_list = []
    # To clean before new list applied
    Companies_Frame_Var.configure(values=Companies_list)

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    Companies_list = NAV_OData_API.Get_Companies(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment)

    if len(Companies_list) > 0:
        # Update Option List
        Companies_Frame_Var.configure(values=Companies_list)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Companies downloaded.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
    else:
        pass

def Select_Company_Process(Configuration: dict|None, window: CTk|None, Documents: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Log_Proc_Used_Variable: StringVar, PO_MUL_LOG_PROC_Frame: CTkFrame, BB_Vendor_Used_Variable: StringVar, BB_Vendor_Used_Frame: CTkFrame) -> None:
    Get_Logistic_Process_List(Configuration=Configuration, window=window, Documents=Documents, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Log_Proc_Used_Variable=Log_Proc_Used_Variable, PO_MUL_LOG_PROC_Frame=PO_MUL_LOG_PROC_Frame)
    Get_HQ_Vendors_List(Configuration=Configuration, window=window, Documents=Documents, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, BB_Vendor_Used_Variable=BB_Vendor_Used_Variable, BB_Vendor_Used_Frame=BB_Vendor_Used_Frame)

def Get_Logistic_Process_List(Configuration: dict|None, window: CTk|None, Documents: dict, NUS_version: str, NOC: str, Environment: str, Company: str, Log_Proc_Used_Variable: StringVar, PO_MUL_LOG_PROC_Frame: CTkFrame) -> None:
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Company = Data_Functions.Company_Name_prepare(Company=Company)
    Log_Process_List = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    Log_Process_List = NAV_OData_API.Get_HQ_Testing_Logistic_Process_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    
    if len(Log_Process_List) > 0:
        # Add empty value for all
        Log_Process_List.append(" ")    # space because of OptionMenu full row list
        
        # Update Option List
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Process_List"], Information=Log_Process_List)
        PO_MUL_LOG_PROC_Frame_Var = PO_MUL_LOG_PROC_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
        PO_MUL_LOG_PROC_Frame_Var.configure(values=Log_Process_List)
        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=PO_MUL_LOG_PROC_Frame_Var, values=Log_Process_List, command=lambda PO_MUL_LOG_PROC_Frame_Var: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=Log_Proc_Used_Variable, File_Name="Documents", JSON_path=["Logistic_Process", "Used"], Information=PO_MUL_LOG_PROC_Frame_Var), GUI_Level_ID=3)
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It was not possible to download Logistic Process or Table is empty, will not be possible to use filter for Multiple POs.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Get_HQ_Vendors_List(Configuration: dict|None, window: CTk|None, Documents: dict, NUS_version: str, NOC: str, Environment: str, Company: str, BB_Vendor_Used_Variable: StringVar, BB_Vendor_Used_Frame: CTkFrame) -> None:
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Company = Data_Functions.Company_Name_prepare(Company=Company)
    HQ_Vendors_list = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    HQ_Vendors_list = list(set(HQ_Vendors_list))

    if len(HQ_Vendors_list) > 0:
        # Update Option List
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Vendors_List"], Information=HQ_Vendors_list)
        BB_Vendor_Used_Frame_Var = BB_Vendor_Used_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
        BB_Vendor_Used_Frame_Var.configure(values=HQ_Vendors_list)
        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Vendor_Used_Frame_Var, values=HQ_Vendors_list, command=lambda BB_Vendor_Used_Frame_Var: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=BB_Vendor_Used_Variable, File_Name="Documents", JSON_path=["BackBone_Billing", "Used"], Information=BB_Vendor_Used_Frame_Var), GUI_Level_ID=3)
        # Last step to confirm that company is selected and all data downloaded
        response = Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Company Selected, you can continue.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It was not possible to download Vendors or HQ Communication Setup table is empty, will not be possible to use filter for Multiple POs.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)


def Get_Orders_List(Configuration: dict|None, window: CTk|None, NUS_version: str, NOC: str, Environment: str, Company: str, Document_Type: str, Logistic_Process_Filter: str) -> list:
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Company = Data_Functions.Company_Name_prepare(Company=Company)
    Can_Process = True
    Purchase_Header_list = []

    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company)
    if HQ_Communication_Setup_df.empty:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        Can_Process = False
    else:
        pass

    # HQ_Testing_Purchase_Headers
    if Can_Process == True:
        Purchase_Header_list = NAV_OData_API.Get_Purchase_Headers_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Document_Type=Document_Type, HQ_Vendors_list=HQ_Vendors_list, Logistic_Process_Filter=Logistic_Process_Filter)
        if len(Purchase_Header_list) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no purchase header for {Document_Type} downloaded that is why program cannot continue. Please check", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass
    else:
        pass

    return Purchase_Header_list


def Download_Data_Purchase_Orders(Settings: dict, Configuration: dict|None, window: CTk|None, Progress_Bar: CTkProgressBar|None, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Order_list: list, client_id: str|None=None, client_secret: str|None=None, tenant_id: str|None=None, GUI: bool=True) -> None:
    Company = Data_Functions.Company_Name_prepare(Company=Company)

    if GUI == True:
        Progress_Bar.configure(determinate_speed = round(number=50 / 23, ndigits=3), progress_color="#517A31")
    else:
        pass
    Can_Process = True

    Purchase_Headers_df = DataFrame()
    Purchase_Lines_df = DataFrame()
    HQ_Communication_Setup_df = DataFrame()
    Company_Information_df = DataFrame()
    Country_ISO_Code_list = []
    HQ_CPDI_Level_df = DataFrame()
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
    Shipment_Method_list = []
    Shipping_Agent_list = []
    Tariff_Number_list = []
    UoM_df = DataFrame()

    # Headers for all pages
    if GUI == True:
        Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    else:
        pass
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id, GUI=GUI)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
    if HQ_Communication_Setup_df.empty:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail="HQ Communication Setup is empty, canceling download and process. Please check.")
        Can_Process = False
    else:
        # Drop Duplicate rows amd reset index
        HQ_Communication_Setup_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_Communication_Setup_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass

    # HQ_Testing_NVR_FS_Connect
    if Can_Process == True:
        NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list, GUI=GUI)
        if NVR_FS_Connect_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            NVR_FS_Connect_df.drop_duplicates(inplace=True, ignore_index=True)
            NVR_FS_Connect_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Purchase_Headers
    if Can_Process == True:
        Purchase_Headers_df, Purchase_Order_list = NAV_OData_API.Get_Purchase_Headers_info_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, HQ_Vendors_list=HQ_Vendors_list, GUI=GUI)
        if Purchase_Headers_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no purchase header downloaded that is why program cannot continue. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="There is no purchase header downloaded that is why program cannot continue. Please check.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Purchase_Headers_df.drop_duplicates(inplace=True, ignore_index=True)
            Purchase_Headers_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Purchase_Lines
    if Can_Process == True:
        Purchase_Lines_df, Items_list = NAV_OData_API.Get_Purchase_Lines_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, GUI=GUI)
        if Purchase_Lines_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no purchase lines downloaded, that is why program cannot continue. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="There is no purchase lines downloaded, that is why program cannot continue. Please check.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Purchase_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
            Purchase_Lines_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_HQ_Item_Transport_Register
    if Can_Process == True:
        HQ_Item_Transport_Register_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Order_list, Document_Type="Order", Vendor_Document_Type="Export", GUI=GUI)
        if HQ_Item_Transport_Register_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"All Order/s you select were not exported by HQ, canceling download. Please Export them first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="All Order/s you select were not exported by HQ, canceling download. Please Export them first.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            HQ_Item_Transport_Register_df.drop_duplicates(inplace=True, ignore_index=True)
            HQ_Item_Transport_Register_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Items
    if Can_Process == True:
        Items_df, Substitution_Item_list, BOM_Item_list, BEU_Set_Item_list, Item_Tracking_Code_list = NAV_OData_API.Get_Items_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, GUI=GUI)
        if Items_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It was not possible to download any Item detail information from Item Cards.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="It was not possible to download any Item detail information from Item Cards.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Items_df.drop_duplicates(inplace=True, ignore_index=True)
            Items_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Items_BOM
    if Can_Process == True:
        Items_BOMs_df, Items_For_BOM_df = NAV_OData_API.Get_Items_BOM_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=BOM_Item_list, GUI=GUI)
        Items_BOMs_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_BOMs_df.reset_index(drop=True, inplace=True)

        Items_For_BOM_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_For_BOM_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Items_Substitutions
    if Can_Process == True:
        Items_Substitutions_df, Items_For_Substitution_df = NAV_OData_API.Get_Items_Substitutions_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Substitution_Item_list, GUI=GUI)
        Items_Substitutions_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Substitutions_df.reset_index(drop=True, inplace=True)

        Items_For_Substitution_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_For_Substitution_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Items_Connected_Items
    if Can_Process == True:
        Items_Connected_Items_df, Items_For_Connected_Items_df = NAV_OData_API.Get_Items_Connected_Items_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, Connection_Type_list=["Free of Charge", "Distribution"], GUI=GUI)
        Items_Connected_Items_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Connected_Items_df.reset_index(drop=True, inplace=True)

        Items_For_Connected_Items_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_For_Connected_Items_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
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
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Items_Price_Detail_List
    if Can_Process == True:
        Active_Price_Lists_df, BEU_Price_list = NAV_OData_API.Get_Items_Price_Lists_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Items_Price_List_Detail_df = NAV_OData_API.Get_Items_Price_List_detail_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, BEU_Price_list=BEU_Price_list, Amount_Type_List=["Price", "Price & Discount"], GUI=GUI)
        # Drop Duplicate rows
        Items_Price_List_Detail_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Price_List_Detail_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Items_Tracking_Codes
    if Can_Process == True:
        Items_Tracking_df = NAV_OData_API.Get_Items_Tracking_Codes_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Item_Tracking_Code_list=Item_Tracking_Code_list, GUI=GUI)
        Items_Tracking_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Tracking_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Items_UoM
    if Can_Process == True:
        Items_UoM_df = NAV_OData_API.Get_Items_UoM_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, GUI=GUI)
        Items_UoM_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_UoM_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_BEU_Dist_Status
    if Can_Process == True:
        Items_Distr_Status_df = NAV_OData_API.Get_Items_Distr_Status_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Items_Distr_Status_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Distr_Status_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Plans
    if Can_Process == True:
        Plants_df = NAV_OData_API.Get_Plants_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Plants_df.drop_duplicates(inplace=True, ignore_index=True)
        Plants_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Shipment_Method
    if Can_Process == True:
        Shipment_Method_list = NAV_OData_API.Get_Shipment_Method_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Shipping_Agent
    if Can_Process == True:
        Shipping_Agent_list = NAV_OData_API.Get_Shipping_Agent_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Tariff_Numbers
    if Can_Process == True:
        Tariff_Number_list = NAV_OData_API.Get_Tariff_Number_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Company_Information
    if Can_Process == True:
        Company_Information_df = NAV_OData_API.Get_Company_Information_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Company_Information_df.drop_duplicates(inplace=True, ignore_index=True)
        Company_Information_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Country_Regions
    if Can_Process == True:
        Country_ISO_Code_list = NAV_OData_API.Get_Country_ISO_Code_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_HQ_CPDI_Level_df
    if Can_Process == True:
        HQ_CPDI_Level_df = NAV_OData_API.Get_CPDI_Level_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        HQ_CPDI_Level_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_CPDI_Level_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_HQ_CPDI_Status_df
    if Can_Process == True:
        HQ_CPDI_Status_df = NAV_OData_API.Get_CPDI_Status_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        HQ_CPDI_Status_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_CPDI_Status_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_UoM
    if Can_Process == True:
        UoM_df =  NAV_OData_API.Get_UoM_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        UoM_df.drop_duplicates(inplace=True, ignore_index=True)
        UoM_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    if Can_Process == True:
        if GUI == True:
            Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1)
        else:
            pass
        Prepare_Files.Process_Purchase_Orders(
            Settings=Settings,
            Configuration=Configuration,
            window=window,
            headers=headers, 
            tenant_id=tenant_id, 
            NUS_version=NUS_version, 
            NOC=NOC, 
            Environment=Environment, 
            Company=Company,
            Can_Process=Can_Process, 
            Purchase_Headers_df=Purchase_Headers_df, 
            Purchase_Lines_df=Purchase_Lines_df, 
            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
            Company_Information_df=Company_Information_df, 
            Country_ISO_Code_list=Country_ISO_Code_list, 
            HQ_CPDI_Level_df=HQ_CPDI_Level_df, 
            HQ_CPDI_Status_df=HQ_CPDI_Status_df, 
            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, 
            Items_df=Items_df, 
            Items_BOMs_df=Items_BOMs_df, 
            Items_Substitutions_df=Items_Substitutions_df, 
            Items_Connected_Items_df=Items_Connected_Items_df, 
            Items_Price_List_Detail_df=Items_Price_List_Detail_df, 
            Items_Tracking_df=Items_Tracking_df, 
            Items_UoM_df=Items_UoM_df, 
            Items_Distr_Status_df=Items_Distr_Status_df,
            NVR_FS_Connect_df=NVR_FS_Connect_df, 
            Plants_df=Plants_df, 
            Shipment_Method_list=Shipment_Method_list, 
            Shipping_Agent_list=Shipping_Agent_list, 
            Tariff_Number_list=Tariff_Number_list, 
            UoM_df=UoM_df,
            GUI=GUI)
        
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Selected files for selected Purchase Order/s successfully created.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=200, detail="Selected files for selected Purchase Order/s successfully created.")
    else:
        if GUI == True:
            Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=0)
        else:
            pass

def Download_Data_BackBoneBilling(Settings: dict, Configuration: dict|None, window: CTk|None, Progress_Bar: CTkProgressBar|None, NUS_version: str, NOC: str, Environment: str, Company: str, Buy_from_Vendor_No: str, client_id: str|None=None, client_secret: str|None=None, tenant_id: str|None=None, GUI: bool=True) -> None:
    Company = Data_Functions.Company_Name_prepare(Company=Company)

    if GUI == True:
        Progress_Bar.configure(determinate_speed = round(number=50 / 6, ndigits=3), progress_color="#517A31")
    else:
        pass
    Can_Process = True

    HQ_Communication_Setup_df = DataFrame()
    NVR_FS_Connect_df = DataFrame()
    Vendor_Service_Function_df = DataFrame()
    Plants_df = DataFrame()
    Country_ISO_Code_list = []
    Tariff_Number_list = []

    # Headers for all pages
    if GUI == True:
        Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    else:
        pass
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id, GUI=GUI)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}

    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
    if HQ_Communication_Setup_df.empty:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail="HQ Communication Setup is empty, canceling download and process. Please check.")
        Can_Process = False
    else:
        # Drop Duplicate rows amd reset index
        HQ_Communication_Setup_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_Communication_Setup_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass

    # HQ_Testing_NVR_FS_Connect
    if Can_Process == True:
        NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list, GUI=GUI)
        if NVR_FS_Connect_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            NVR_FS_Connect_df.drop_duplicates(inplace=True, ignore_index=True)
            NVR_FS_Connect_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # Vendor_Service_Function_df
    if Can_Process == True:
        Vendor_Service_Function_df = NAV_OData_API.Get_Vendor_Service_Functions_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Buy_from_Vendor_No=Buy_from_Vendor_No, GUI=GUI)
        if Vendor_Service_Function_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It was not possible to download any Vendor Service Functions detail so program cannot build Invoice.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="It was not possible to download any Vendor Service Functions detail so program cannot build Invoice.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Vendor_Service_Function_df.drop_duplicates(inplace=True, ignore_index=True)
            Vendor_Service_Function_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Company_Information
    if Can_Process == True:
        Company_Information_df = NAV_OData_API.Get_Company_Information_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Company_Information_df.drop_duplicates(inplace=True, ignore_index=True)
        Company_Information_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Plans
    if Can_Process == True:
        Plants_df = NAV_OData_API.Get_Plants_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Plants_df.drop_duplicates(inplace=True, ignore_index=True)
        Plants_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Country_Regions
    if Can_Process == True:
        Country_ISO_Code_list = NAV_OData_API.Get_Country_ISO_Code_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Tariff_Numbers
    if Can_Process == True:
        Tariff_Number_list = NAV_OData_API.Get_Tariff_Number_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    if Can_Process == True:
        if GUI == True:
            Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1)
        else:
            pass
        Prepare_Files.Process_BackBoneBilling(
            Settings=Settings,
            Configuration=Configuration,
            window=window,
            Can_Process=Can_Process, 
            Buy_from_Vendor_No=Buy_from_Vendor_No,
            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
            NVR_FS_Connect_df=NVR_FS_Connect_df, 
            Vendor_Service_Function_df=Vendor_Service_Function_df,
            Company_Information_df=Company_Information_df,
            Plants_df=Plants_df,
            Country_ISO_Code_list=Country_ISO_Code_list,  
            Tariff_Number_list=Tariff_Number_list,
            GUI=GUI)
        
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Selected files for selected BackBone Billing Invoice/s successfully created.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=200, detail="Selected files for selected BackBone Billing Invoice/s successfully created.")
    else:
        if GUI == True:
            Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=0)
        else:
            pass

def Download_Data_Return_Order(Settings: dict, Configuration: dict|None, window: CTk|None, Progress_Bar: CTkProgressBar|None, NUS_version: str, NOC: str, Environment: str, Company: str, Purchase_Return_Orders_List: list, client_id: str|None=None, client_secret: str|None=None, tenant_id: str|None=None, GUI: bool=True) -> None:
    Company = Data_Functions.Company_Name_prepare(Company=Company)

    if GUI == True:
        Progress_Bar.configure(determinate_speed = round(number=50 / 11, ndigits=3), progress_color="#517A31")
    else:
        pass
    Can_Process = True

    Purchase_Return_Headers_df = DataFrame()
    Purchase_Return_Lines_df = DataFrame()
    HQ_Communication_Setup_df = DataFrame()
    Company_Information_df = DataFrame()
    Country_ISO_Code_list = []
    HQ_Item_Transport_Register_df = DataFrame()
    Items_df = DataFrame()
    Items_Price_List_Detail_df = DataFrame()
    NVR_FS_Connect_df = DataFrame()
    Tariff_Number_list = []
    UoM_df = DataFrame()

    # Headers for all pages
    if GUI == True:
        Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    else:
        pass
    access_token = Authorization.Azure_OAuth(Configuration=Configuration, window=window, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id, GUI=GUI)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'}
    
    # HQ_Testing_HQ_Communication
    HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendors_list = NAV_OData_API.Get_HQ_Communication_Setup_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
    if HQ_Communication_Setup_df.empty:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"HQ Communication Setup is empty, canceling download and process. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail="HQ Communication Setup is empty, canceling download and process. Please check.")
        Can_Process = False
    else:
        # Drop Duplicate rows amd reset index
        HQ_Communication_Setup_df.drop_duplicates(inplace=True, ignore_index=True)
        HQ_Communication_Setup_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass

    # HQ_Testing_NVR_FS_Connect
    if Can_Process == True:
        NVR_FS_Connect_df = NAV_OData_API.Get_NVR_FS_Connect_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, File_Connector_Code_list=File_Connector_Code_list, GUI=GUI)
        if NVR_FS_Connect_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="NVR File Connector is empty, this means that there is not know path for file exports. Canceling downloads.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            NVR_FS_Connect_df.drop_duplicates(inplace=True, ignore_index=True)
            NVR_FS_Connect_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Purchase_Headers
    if Can_Process == True:
        Purchase_Return_Headers_df, Purchase_Return_Orders_List = NAV_OData_API.Get_Purchase_Return_Headers_info_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Return_Orders_List=Purchase_Return_Orders_List, HQ_Vendors_list=HQ_Vendors_list, GUI=GUI)
        if Purchase_Return_Headers_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no purchase return header downloaded that is why program cannot continue. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="There is no purchase return header downloaded that is why program cannot continue. Please check.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Purchase_Return_Headers_df.drop_duplicates(inplace=True, ignore_index=True)
            Purchase_Return_Headers_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Purchase_Lines
    if Can_Process == True:
        Purchase_Return_Lines_df, Items_list = NAV_OData_API.Get_Purchase_Return_Lines_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Return_Orders_List=Purchase_Return_Orders_List, GUI=GUI)
        if Purchase_Return_Lines_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no purchase return lines downloaded, that is why program cannot continue. Please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="There is no purchase return lines downloaded, that is why program cannot continue. Please check.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Purchase_Return_Lines_df.drop_duplicates(inplace=True, ignore_index=True)
            Purchase_Return_Lines_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_HQ_Item_Transport_Register
    if Can_Process == True:
        HQ_Item_Transport_Register_df = NAV_OData_API.Get_HQ_Item_Transport_Register_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Purchase_Order_list=Purchase_Return_Orders_List, Document_Type="Return Order", Vendor_Document_Type="Export", GUI=GUI)
        if HQ_Item_Transport_Register_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"All Order/s you select were not exported by HQ, canceling download. Please Export them first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="All Order/s you select were not exported by HQ, canceling download. Please Export them first.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            HQ_Item_Transport_Register_df.drop_duplicates(inplace=True, ignore_index=True)
            HQ_Item_Transport_Register_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Items
    if Can_Process == True:
        Items_df, Substitution_Item_list, BOM_Item_list, BEU_Set_Item_list, Item_Tracking_Code_list = NAV_OData_API.Get_Items_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, GUI=GUI)
        if Items_df.empty:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"It was not possible to download any Item detail information from Item Cards.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail="It was not possible to download any Item detail information from Item Cards.")
            Can_Process = False
        else:
            # Drop Duplicate rows amd reset index
            Items_df.drop_duplicates(inplace=True, ignore_index=True)
            Items_df.reset_index(drop=True, inplace=True)
            if GUI == True:
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
            else:
                pass
    else:
        pass

    # HQ_Testing_Items_Price_Detail_List
    if Can_Process == True:
        Active_Price_Lists_df, BEU_Price_list = NAV_OData_API.Get_Items_Price_Lists_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Items_Price_List_Detail_df = NAV_OData_API.Get_Items_Price_List_detail_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Items_list, BEU_Price_list=BEU_Price_list, Amount_Type_List=["Price", "Price & Discount"], GUI=GUI)
        # Drop Duplicate rows
        Items_Price_List_Detail_df.drop_duplicates(inplace=True, ignore_index=True)
        Items_Price_List_Detail_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Country_Regions
    if Can_Process == True:
        Country_ISO_Code_list = NAV_OData_API.Get_Country_ISO_Code_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Tariff_Numbers
    if Can_Process == True:
        Tariff_Number_list = NAV_OData_API.Get_Tariff_Number_list(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_Company_Information
    if Can_Process == True:
        Company_Information_df = NAV_OData_API.Get_Company_Information_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        Company_Information_df.drop_duplicates(inplace=True, ignore_index=True)
        Company_Information_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    # HQ_Testing_UoM
    if Can_Process == True:
        UoM_df =  NAV_OData_API.Get_UoM_df(Configuration=Configuration, window=window, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, GUI=GUI)
        UoM_df.drop_duplicates(inplace=True, ignore_index=True)
        UoM_df.reset_index(drop=True, inplace=True)
        if GUI == True:
            Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
        else:
            pass
    else:
        pass

    if Can_Process == True:
        if GUI == True:
            Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1)
        else:
            pass
        Prepare_Files.Process_Purchase_Return_Orders(
            Settings=Settings,
            Configuration=Configuration,
            window=window,
            headers=headers, 
            tenant_id=tenant_id, 
            NUS_version=NUS_version, 
            NOC=NOC, 
            Environment=Environment, 
            Company=Company,
            Can_Process=Can_Process, 
            HQ_Vendors_list=HQ_Vendors_list,
            Purchase_Return_Headers_df=Purchase_Return_Headers_df, 
            Purchase_Return_Lines_df=Purchase_Return_Lines_df, 
            HQ_Communication_Setup_df=HQ_Communication_Setup_df, 
            Company_Information_df=Company_Information_df, 
            Country_ISO_Code_list=Country_ISO_Code_list, 
            HQ_Item_Transport_Register_df=HQ_Item_Transport_Register_df, 
            Items_df=Items_df, 
            Items_Price_List_Detail_df=Items_Price_List_Detail_df, 
            NVR_FS_Connect_df=NVR_FS_Connect_df, 
            UoM_df=UoM_df,
            Tariff_Number_list=Tariff_Number_list, 
            GUI=GUI)
        
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Selected files for selected Return Purchase Order/s successfully created.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=200, detail="Selected files for selected Return Purchase Order/s successfully created.")
    else:
        if GUI == True:
            Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=0)
        else:
            pass