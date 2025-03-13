# Import libraries
from pandas import DataFrame
import requests
import json

import Libs.GUI.Elements as Elements
import Libs.Pandas_Functions as Pandas_Functions

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Get_Params(fields_list_string: str, filters_list_string: str) -> dict:
    if (fields_list_string == "") and (filters_list_string == ""):
        params = {}
    elif (fields_list_string != "") and (filters_list_string == ""):
        params = {
            "$select": fields_list_string,
            "$schemaversion" : "2.1"}
    elif (fields_list_string == "") and (filters_list_string != ""):
        params = {
            "$filter": filters_list_string,
            "$schemaversion" : "2.1"}
    elif (fields_list_string != "") and (filters_list_string != ""):
        params = {
            "$select": fields_list_string,
            "$filter": filters_list_string,
            "$schemaversion" : "2.1"}
    else:
        params = {
            "$schemaversion" : "2.1"}
    return params
    
def Get_Field_List_string(fields_list: list, Join_sign: str) -> str:
    sub_fields_list_string = f"{Join_sign}".join(fields_list)
    return sub_fields_list_string

def Get_Rid_od_OData_Tag(My_dictionary: dict, Key: str) -> dict:
    My_dictionary.pop(Key)
    return My_dictionary

def Request_Endpoint(Configuration: dict, headers: dict, params: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Table: str):
    response_values_List = []
    list_len = 0 

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/{Table}"
    response = requests.get(url=url, headers=headers, params=params)
    if (response.status_code >= 200) and (response.status_code < 300):
        response_values_List = response.json()["value"]
        list_len =len(response_values_List)
    else:
        Error_dict = json.loads(response.text)
        Error_Code = Error_dict["error"]["code"]
        Error_Detail = Error_dict["error"]["message"]
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"{Error_Code}: {Error_Detail}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    return response_values_List, list_len

# ---------------------------------------------------------- Main Functions ---------------------------------------------------------- #
# ------------------- Company List ------------------- #
def Get_Companies(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str) -> list:    
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/api/v2.0/companies"
    response = requests.get(url=url, headers=headers)
    Companies_list = []

    if (response.status_code >= 200) and (response.status_code < 300):
        response_values_List = response.json()["value"]
        list_len =len(response_values_List)

        for index in range(0, list_len):
            Companies_list.append(response_values_List[index]["name"])
    else:
        Error_dict = json.loads(response.text)
        Error_Code = Error_dict["error"]["code"]
        Error_Detail = Error_dict["error"]["message"]
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"{Error_Code}: {Error_Detail}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    return Companies_list

# ------------------- HQ_Testing_Logistic_Process ------------------- #
def Get_HQ_Testing_Logistic_Process_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["Process_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Logistic_Process")

    # Prepare DataFrame
    Process_Code_List = []
    for index in range(0, list_len):
        Process_Code_List.append(response_values_List[index]["Process_Code"])

    return Process_Code_List

# ------------------- HQ_Testing_Purchase_Headers ------------------- #
def Get_Purchase_Headers_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Document_Type: str, HQ_Vendors_list: list, Logistic_Process_Filter: str):
    # Fields
    fields_list = ["No"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    Order_status_List = ["Exported", "Partially Confirmed", "Confirmed", "Partially PreAdviced", "PreAdviced", "Partially Dispatched", "Dispatched", "Partially Invoiced", "Partially Posted", "Partially Delivered"]
    filters_Order_status = Get_Field_List_string(fields_list=Order_status_List, Join_sign="','")
    filters_Vendors = Get_Field_List_string(fields_list=HQ_Vendors_list, Join_sign="','")
    if (Logistic_Process_Filter == " ") or (Logistic_Process_Filter == ""):
        filters_list_string = f"""Document_Type eq '{Document_Type}' and Buy_from_Vendor_No in ('{filters_Vendors}') and HQ_Order_Status_NUS in ('{filters_Order_status}')"""
    else:
        filters_list_string = f"""Document_Type eq '{Document_Type}' and Buy_from_Vendor_No in ('{filters_Vendors}') and LogisticProcessFieldNUS eq '{Logistic_Process_Filter}' and HQ_Order_Status_NUS in ('{filters_Order_status}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    if Document_Type == "Order":
        response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Purchase_Headers")
    elif Document_Type == "Return Order":
        response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Purch_Ret_Header")

    # Prepare DataFrame
    Purchase_Header_No_list = []
    for index in range(0, list_len):
        Purchase_Header_No_list.append(response_values_List[index]["No"])
    
    return Purchase_Header_No_list


def Get_Purchase_Headers_info_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Purchase_Order_list: list, HQ_Vendors_list: list):
    # Fields
    fields_list = ["No", "Buy_from_Vendor_No", "HQ_Identification_No_NUS", "ShippingConditionFieldNUS", "CompleteDeliveryFieldNUS", "PDICenterFieldNUS", "HQCPDILevelRequestedFieldNUS", "Expected_Receipt_Date", "Promised_Receipt_Date", "Requested_Receipt_Date", "Order_Date", "Currency_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Prepare DataFrame
    Purchase_Order_No_list = []
    Buy_from_Vendor_No_list = []
    HQ_Identification_No_NUS_list = []
    ShippingConditionFieldNUS_list = []
    CompleteDeliveryFieldNUS_list = []
    PDICenterFieldNUS_list = []
    HQCPDILevelRequestedFieldNUS_list = []
    Expected_Receipt_Date_list = []
    Promised_Receipt_Date_list = []
    Requested_Receipt_Date_list = []
    Order_Date_list = []
    Currency_Code_list = []

    Non_HQ_Orders = []
    Non_HQ_Vendors = []

    for Purchase_Order in Purchase_Order_list:
        # Filters
        filters_list_string = f"""Document_Type eq 'Order' and No eq '{Purchase_Order}'"""

        # Params
        params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

        # Request
        response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_PO_Header_Detail")

        for index in range(0, list_len):
            if response_values_List[index]["Buy_from_Vendor_No"] in HQ_Vendors_list:
                Purchase_Order_No_list.append(response_values_List[index]["No"])
                Buy_from_Vendor_No_list.append(response_values_List[index]["Buy_from_Vendor_No"])
                HQ_Identification_No_NUS_list.append(response_values_List[index]["HQ_Identification_No_NUS"])
                ShippingConditionFieldNUS_list.append(response_values_List[index]["ShippingConditionFieldNUS"])
                CompleteDeliveryFieldNUS_list.append(response_values_List[index]["CompleteDeliveryFieldNUS"])
                PDICenterFieldNUS_list.append(response_values_List[index]["PDICenterFieldNUS"])
                HQCPDILevelRequestedFieldNUS_list.append(response_values_List[index]["HQCPDILevelRequestedFieldNUS"])
                Expected_Receipt_Date_list.append(response_values_List[index]["Expected_Receipt_Date"])
                Promised_Receipt_Date_list.append(response_values_List[index]["Promised_Receipt_Date"])
                Requested_Receipt_Date_list.append(response_values_List[index]["Requested_Receipt_Date"])
                Order_Date_list.append(response_values_List[index]["Order_Date"])
                Currency_Code_list.append(response_values_List[index]["Currency_Code"])
            else:
                Non_HQ_Orders.append(response_values_List[index]["No"])
                Non_HQ_Vendors.append(response_values_List[index]["Buy_from_Vendor_No"])

    response_values_dict = {
        "No": Purchase_Order_No_list,
        "Buy_from_Vendor_No": Buy_from_Vendor_No_list,
        "HQ_Identification_No_NUS": HQ_Identification_No_NUS_list,
        "ShippingConditionFieldNUS": ShippingConditionFieldNUS_list,
        "CompleteDeliveryFieldNUS": CompleteDeliveryFieldNUS_list,
        "PDICenterFieldNUS": PDICenterFieldNUS_list,
        "HQCPDILevelRequestedFieldNUS": HQCPDILevelRequestedFieldNUS_list,
        "Expected_Receipt_Date": Expected_Receipt_Date_list,
        "Promised_Receipt_Date": Promised_Receipt_Date_list,
        "Requested_Receipt_Date": Requested_Receipt_Date_list,
        "Order_Date": Order_Date_list,
        "Currency_Code": Currency_Code_list}

    if len(response_values_dict) == 1:
        Purchase_Headers_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Purchase_Headers_df = DataFrame(data=response_values_dict, columns=fields_list)
    Purchase_Headers_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Purchase_Headers_df, Columns_list=["No"], Accenting_list=[True]) 

    # Non-HQ Purchase Orders Message
    if len(Non_HQ_Orders) > 0:
        Non_HQ_Orders = list(set(Non_HQ_Orders))
        Non_HQ_Orders = Get_Field_List_string(fields_list=Non_HQ_Orders, Join_sign=", ")
        Non_HQ_Vendors = list(set(Non_HQ_Vendors))
        Non_HQ_Vendors = Get_Field_List_string(fields_list=Non_HQ_Vendors, Join_sign=", ")
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Program will not process these Purchase Orders: {Non_HQ_Orders} \n as this/these Vendors: {Non_HQ_Vendors}\n are not part of HQ Communication.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        pass

    Purchase_Order_No_list = list(set(Purchase_Order_No_list))
    return Purchase_Headers_df, Purchase_Order_No_list

# ------------------- HQ_Testing_Purchase_Lines ------------------- #
def Get_Purchase_Lines_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Purchase_Order_list: list):
    # Fields
    fields_list = ["Document_No", "Type", "Line_No", "No", "Description", "Quantity", "Unit_of_Measure_Code", "Direct_Unit_Cost"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Purchase_Order = Get_Field_List_string(fields_list=Purchase_Order_list, Join_sign="','")
    filters_list_string = f"""Document_Type eq 'Order' and Type eq 'Item' and Document_No in ('{filters_Purchase_Order}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Purchase_Lines")

    # Prepare DataFrame
    Purchase_Order_No_list = []
    Type_list = []
    Line_No_list = []
    No_list = []
    Description_list = []
    Quantity_list = []
    Unit_of_Measure_Code_list = []
    Direct_Unit_Cost_list = []

    for index in range(0, list_len):
        Purchase_Order_No_list.append(response_values_List[index]["Document_No"])
        Type_list.append(response_values_List[index]["Type"])
        Line_No_list.append(response_values_List[index]["Line_No"])
        No_list.append(response_values_List[index]["No"])
        Description_list.append(response_values_List[index]["Description"])
        Quantity_list.append(response_values_List[index]["Quantity"])
        Unit_of_Measure_Code_list.append(response_values_List[index]["Unit_of_Measure_Code"])
        Direct_Unit_Cost_list.append(response_values_List[index]["Direct_Unit_Cost"])

    response_values_dict = {
        "Document_No": Purchase_Order_No_list,
        "Type": Type_list,
        "Line_No": Line_No_list,
        "No": No_list,
        "Description": Description_list,
        "Quantity": Quantity_list,
        "Unit_of_Measure_Code": Unit_of_Measure_Code_list,
        "Direct_Unit_Cost": Direct_Unit_Cost_list}
    
    if list_len == 1:
        Purchase_Lines_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Purchase_Lines_df = DataFrame(data=response_values_dict, columns=fields_list)
    Purchase_Lines_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Purchase_Lines_df, Columns_list=["Document_No", "Line_No"], Accenting_list=[True, True]) 

    Items_list = list(set(No_list))
    return Purchase_Lines_df, Items_list

# ------------------- HQ_Testing_HQ_Communication ------------------- #
def Get_HQ_Communication_Setup_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["HQ_Vendor_Type", "HQ_Vendor_No", "HQ_Identification_No", "Zero_Date", "HQ_Confirm_File_Path", "HQ_PreAdvice_File_Path", "HQ_CPDI_Import_Path", "HQ_Delivery_File_Path", "HQ_Invoice_File_Path", "HQ_PDF_File_Path", "HQ_R_O_Confirm_File_Path", "HQ_R_O_Cr_Memo_File_Path", "File_Connector_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_HQ_Communication")

    # Prepare DataFrame
    HQ_Vendor_Type_list = []
    HQ_Vendor_No_list = []
    HQ_Identification_No_list = []
    Zero_Date_list = []
    HQ_Confirm_File_Path_list = []
    HQ_PreAdvice_File_Path_list = []
    HQ_CPDI_Import_Path_list = []
    HQ_Delivery_File_Path_list = []
    HQ_Invoice_File_Path_list = []
    HQ_PDF_File_Path_list = []
    HQ_R_O_Confirm_File_Path_list = []
    HQ_R_O_Cr_Memo_File_Path_list = []
    File_Connector_Code_list = []

    for index in range(0, list_len):
        HQ_Vendor_Type_list.append(response_values_List[index]["HQ_Vendor_Type"])
        HQ_Vendor_No_list.append(response_values_List[index]["HQ_Vendor_No"])
        HQ_Identification_No_list.append(response_values_List[index]["HQ_Identification_No"])
        Zero_Date_list.append(response_values_List[index]["Zero_Date"])
        HQ_Confirm_File_Path_list.append(response_values_List[index]["HQ_Confirm_File_Path"])
        HQ_PreAdvice_File_Path_list.append(response_values_List[index]["HQ_PreAdvice_File_Path"])
        HQ_CPDI_Import_Path_list.append(response_values_List[index]["HQ_CPDI_Import_Path"])
        HQ_Delivery_File_Path_list.append(response_values_List[index]["HQ_Delivery_File_Path"])
        HQ_Invoice_File_Path_list.append(response_values_List[index]["HQ_Invoice_File_Path"])
        HQ_PDF_File_Path_list.append(response_values_List[index]["HQ_PDF_File_Path"])
        HQ_R_O_Confirm_File_Path_list.append(response_values_List[index]["HQ_R_O_Confirm_File_Path"])
        HQ_R_O_Cr_Memo_File_Path_list.append(response_values_List[index]["HQ_R_O_Cr_Memo_File_Path"])
        File_Connector_Code_list.append(response_values_List[index]["File_Connector_Code"])

    response_values_dict = {
        "HQ_Vendor_Type": HQ_Vendor_Type_list,
        "HQ_Vendor_No": HQ_Vendor_No_list,
        "HQ_Identification_No": HQ_Identification_No_list,
        "Zero_Date": Zero_Date_list,
        "HQ_Confirm_File_Path": HQ_Confirm_File_Path_list,
        "HQ_PreAdvice_File_Path": HQ_PreAdvice_File_Path_list,
        "HQ_CPDI_Import_Path": HQ_CPDI_Import_Path_list,
        "HQ_Delivery_File_Path": HQ_Delivery_File_Path_list,
        "HQ_Invoice_File_Path": HQ_Invoice_File_Path_list,
        "HQ_PDF_File_Path": HQ_PDF_File_Path_list,
        "HQ_R_O_Confirm_File_Path": HQ_R_O_Confirm_File_Path_list,
        "HQ_R_O_Cr_Memo_File_Path": HQ_R_O_Cr_Memo_File_Path_list,
        "File_Connector_Code": File_Connector_Code_list}
    
    if list_len == 1:
        HQ_Communication_Setup_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        HQ_Communication_Setup_df = DataFrame(data=response_values_dict, columns=fields_list)

    File_Connector_Code_list = list(set(File_Connector_Code_list))
    HQ_Vendor_No_list = list(set(HQ_Vendor_No_list))

    return HQ_Communication_Setup_df, File_Connector_Code_list, HQ_Vendor_No_list

# ------------------- HQ_Testing_Company_Information ------------------- #
def Get_Company_Information_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["English_Name_NUS", "English_Address_NUS", "English_Post_Code_NUS", "English_City_NUS", "English_Country_Reg_Code_NUS"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Company_Information")
    response_values_dict = Get_Rid_od_OData_Tag(My_dictionary=response_values_List[0], Key="@odata.etag")
    
    Company_Information_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    return Company_Information_df

# ------------------- HQ_Testing_Country_Regions ------------------- #
def Get_Country_ISO_Code_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["ISO_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Country_Regions")

    # Prepare DataFrame
    Country_ISO_Code_list = []
    for index in range(0, list_len):
        Country_ISO_Code_list.append(response_values_List[index]["ISO_Code"])

    return Country_ISO_Code_list

# ------------------- HQ_Testing_HQ_CPDI_Levels ------------------- #
def Get_CPDI_Level_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["Level"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_HQ_CPDI_Levels")

    # Prepare DataFrame
    CPDI_Level_list = []
    for index in range(0, list_len):
        CPDI_Level_list.append(response_values_List[index]["Level"])

    return CPDI_Level_list

# ------------------- HQ_Testing_HQ_CPDI_Status ------------------- #
def Get_CPDI_Status_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["Status_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_HQ_CPDI_Status")

    # Prepare DataFrame
    CPDI_Status_list = []
    for index in range(0, list_len):
        CPDI_Status_list.append(response_values_List[index]["Status_Code"])

    return CPDI_Status_list

# ------------------- HQ_Testing_HQ_Item_Transport_Register ------------------- #
def Get_HQ_Item_Transport_Register_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Purchase_Order_list: list, Document_Type: str, Vendor_Document_Type: list) -> DataFrame:
    # Fields
    fields_list = ["Register_No", "Document_Type", "Document_No", "Document_Line_No", "Exported_Line_No", "Vendor_Document_Type", "Line_Type", "Item_No", "Quantity", "Unit_of_Measure", "Currency_Code", "Order_Date"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Purchase_Order = Get_Field_List_string(fields_list=Purchase_Order_list, Join_sign="','")
    filters_Vendor_Document_Type = Get_Field_List_string(fields_list=Vendor_Document_Type, Join_sign="','")
    filters_list_string = f"""Document_Type eq '{Document_Type}' and Document_No in ('{filters_Purchase_Order}') and Vendor_Document_Type in ('{filters_Vendor_Document_Type}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_HQ_Item_Transport_Register")

    # Prepare DataFrame
    Register_No_list = []
    Document_Type_list = []
    Document_No_list = []
    Document_Line_No_list = []
    Exported_Line_No_list = []
    Vendor_Document_Type_list = []
    Line_Type_list = []
    Item_No_list = []
    Quantity_list = []
    Unit_of_Measure_list = []
    Currency_Code_list = []
    Order_Date_list = []

    for index in range(0, list_len):
        Register_No_list.append(response_values_List[index]["Register_No"])
        Document_Type_list.append(response_values_List[index]["Document_Type"])
        Document_No_list.append(response_values_List[index]["Document_No"])
        Document_Line_No_list.append(response_values_List[index]["Document_Line_No"])
        Exported_Line_No_list.append(response_values_List[index]["Exported_Line_No"])
        Vendor_Document_Type_list.append(response_values_List[index]["Vendor_Document_Type"])
        Line_Type_list.append(response_values_List[index]["Line_Type"])
        Item_No_list.append(response_values_List[index]["Item_No"])
        Quantity_list.append(response_values_List[index]["Quantity"])
        Unit_of_Measure_list.append(response_values_List[index]["Unit_of_Measure"])
        Currency_Code_list.append(response_values_List[index]["Currency_Code"])
        Order_Date_list.append(response_values_List[index]["Order_Date"])

    response_values_dict = {
        "Register_No": Register_No_list,
        "Document_Type": Document_Type_list,
        "Document_No": Document_No_list,
        "Document_Line_No": Document_Line_No_list,
        "Exported_Line_No": Exported_Line_No_list,
        "Vendor_Document_Type": Vendor_Document_Type_list,
        "Line_Type": Line_Type_list,
        "Item_No": Item_No_list,
        "Quantity": Quantity_list,
        "Unit_of_Measure": Unit_of_Measure_list,
        "Currency_Code": Currency_Code_list,
        "Order_Date": Order_Date_list}
    
    if list_len == 1:
        HQ_Item_Transport_Register_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        HQ_Item_Transport_Register_df = DataFrame(data=response_values_dict, columns=fields_list)
    HQ_Item_Transport_Register_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=HQ_Item_Transport_Register_df, Columns_list=["Register_No"], Accenting_list=[True]) 

    # Final check non downloaded Purchase Orders list --> not exported
    Non_Exported_Purchase_Orders = []
    for Request_Order in Purchase_Order_list:
        if Request_Order in Document_No_list:
            pass
        else:
            Non_Exported_Purchase_Orders.append(Request_Order)
    if len(Non_Exported_Purchase_Orders) > 1:
        Non_Exported_Purchase_Orders = Get_Field_List_string(fields_list=Non_Exported_Purchase_Orders, Join_sign=", ")
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Program will not process these Purchase Orders: {Non_Exported_Purchase_Orders}, because they were not Exported.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        pass
        
    return HQ_Item_Transport_Register_df

# ------------------- HQ_Testing_Items ------------------- #
def Get_Items_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Items_list: list):
    # Fields
    fields_list = ["No", "Description", "Vendor_No", "Vendor_Item_No", "Item_Tracking_Code", "Substitutes_Exist_NUS", "AssemblyBOM", "BEU_Set_NUS", "BEU_End_of_Life_NUS", "Material_Group_NUS", "Unit_Price", "Distribution_Status_NUS"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Items = Get_Field_List_string(fields_list=Items_list, Join_sign="','")
    filters_list_string = f"""No in ('{filters_Items}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items")

    # Prepare DataFrame
    No_list = []
    Description_list = []
    Vendor_No_list = []
    Vendor_Item_No_list = []
    Item_Tracking_Code_list = []
    Substitutes_Exist_NUS_list = []
    AssemblyBOM_list = []
    BEU_Set_NUS_list = []
    Material_Group_NUS_list = []
    BEU_End_of_Life_NUS_list = []
    Unit_Price_List = []
    Distribution_Status_NUS_List = []
    for index in range(0, list_len):
        No_list.append(response_values_List[index]["No"])
        Description_list.append(response_values_List[index]["Description"])
        Vendor_No_list.append(response_values_List[index]["Vendor_No"])
        Vendor_Item_No_list.append(response_values_List[index]["Vendor_Item_No"])
        Item_Tracking_Code_list.append(response_values_List[index]["Item_Tracking_Code"])
        Substitutes_Exist_NUS_list.append(response_values_List[index]["Substitutes_Exist_NUS"])
        AssemblyBOM_list.append(response_values_List[index]["AssemblyBOM"])
        BEU_Set_NUS_list.append(response_values_List[index]["BEU_Set_NUS"])
        BEU_End_of_Life_NUS_list.append(response_values_List[index]["BEU_End_of_Life_NUS"])
        Material_Group_NUS_list.append(response_values_List[index]["Material_Group_NUS"])
        Unit_Price_List.append(response_values_List[index]["Unit_Price"])
        Distribution_Status_NUS_List.append(response_values_List[index]["Distribution_Status_NUS"])

    response_values_dict = {
        "No": No_list,
        "Description": Description_list,
        "Vendor_No": Vendor_No_list,
        "Vendor_Item_No": Vendor_Item_No_list,
        "Item_Tracking_Code": Item_Tracking_Code_list,
        "Substitutes_Exist_NUS": Substitutes_Exist_NUS_list,
        "AssemblyBOM": AssemblyBOM_list,
        "BEU_Set_NUS": BEU_Set_NUS_list,
        "BEU_End_of_Life_NUS": BEU_End_of_Life_NUS_list,
        "Material_Group_NUS": Material_Group_NUS_list,
        "Unit_Price": Unit_Price_List,
        "Distribution_Status_NUS": Distribution_Status_NUS_List}
    
    if list_len == 1:
        Items_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_df, Columns_list=["No"], Accenting_list=[True]) 

    # Substitutions list
    mask_substitution = Items_df["Substitutes_Exist_NUS"] == True
    Substitution_df = Items_df[mask_substitution]
    Substitution_Item_list = Substitution_df["No"].to_list()
    Substitution_Item_list = list(set(Substitution_Item_list))

    # BOL Items list
    mask_BOM = Items_df["AssemblyBOM"] == True
    BOM_df = Items_df[mask_BOM]
    BOM_Item_list = BOM_df["No"].to_list()
    BOM_Item_list = list(set(BOM_Item_list))

    # BEU Set Item List
    mask_BEU_Set = Items_df["BEU_Set_NUS"] == True
    BEU_Set_df = Items_df[mask_BEU_Set]
    BEU_Set_Item_list = BEU_Set_df["No"].to_list()
    BEU_Set_Item_list = list(set(BEU_Set_Item_list))

    # Item Tracking Codes
    Item_Tracking_Code_list = list(set(Item_Tracking_Code_list))

    return Items_df, Substitution_Item_list, BOM_Item_list, BEU_Set_Item_list, Item_Tracking_Code_list

# ------------------- HQ_Testing_Items_BOM ------------------- #
def Get_Items_BOM_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Items_list: list):
    # Fields
    fields_list = ["Parent_Item_No_NUS", "Line_No", "Type", "No", "Quantity_per", "Unit_of_Measure_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Items = Get_Field_List_string(fields_list=Items_list, Join_sign="','")
    filters_list_string = f"""Type eq 'Item' and Parent_Item_No_NUS in ('{filters_Items}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_BOM")

    # Prepare DataFrame
    Parent_Item_No_NUS_list = []
    Line_No_list = []
    Type_list = []
    No_list = []
    Quantity_per_list = []
    Unit_of_Measure_Code_list = []
    for index in range(0, list_len):
        Parent_Item_No_NUS_list.append(response_values_List[index]["Parent_Item_No_NUS"])
        Line_No_list.append(response_values_List[index]["Line_No"])
        Type_list.append(response_values_List[index]["Type"])
        No_list.append(response_values_List[index]["No"])
        Quantity_per_list.append(response_values_List[index]["Quantity_per"])
        Unit_of_Measure_Code_list.append(response_values_List[index]["Unit_of_Measure_Code"])

    response_values_dict = {
        "Parent_Item_No_NUS": Parent_Item_No_NUS_list,
        "Line_No": Line_No_list,
        "Type": Type_list,
        "No": No_list,
        "Quantity_per": Quantity_per_list,
        "Unit_of_Measure_Code": Unit_of_Measure_Code_list}
    
    if list_len == 1:
        Items_BOMs_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_BOMs_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_BOMs_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_BOMs_df, Columns_list=["Parent_Item_No_NUS", "Line_No"], Accenting_list=[True, True]) 
    
    # Update Item list for new Items + Gent Items 
    No_list = list(set(No_list))
    if len(No_list) > 0:
        Items_return_list = Get_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=No_list)
        Items_For_BOM_df = Items_return_list[0]
    else:
        Items_For_BOM_df = DataFrame()

    return Items_BOMs_df, Items_For_BOM_df


# ------------------- HQ_Testing_Items_Substitution ------------------- #
def Get_Items_Substitutions_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Items_list: list):
    # Fields
    fields_list = ["No", "Substitute_Type", "Substitute_No"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Items = Get_Field_List_string(fields_list=Items_list, Join_sign="','")
    filters_list_string = f"""Type eq 'Item' and Substitute_Type eq 'Item' and No in ('{filters_Items}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_Substitution")

    # Prepare DataFrame
    No_list = []
    Substitute_Type_list = []
    Substitute_No_list = []
    for index in range(0, list_len):
        No_list.append(response_values_List[index]["No"])
        Substitute_Type_list.append(response_values_List[index]["Substitute_Type"])
        Substitute_No_list.append(response_values_List[index]["Substitute_No"])

    response_values_dict = {
        "No": No_list,
        "Substitute_Type": Substitute_Type_list,
        "Substitute_No": Substitute_No_list}
    
    if list_len == 1:
        Items_Substitutions_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_Substitutions_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_Substitutions_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_Substitutions_df, Columns_list=["No"], Accenting_list=[True]) 
    
    # Update Item list for new Items + Gent Items 
    Substitute_No_list = list(set(Substitute_No_list))
    if len(Substitute_No_list) > 0:
        Items_return_list = Get_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=Substitute_No_list)
        Items_For_Substitution_df = Items_return_list[0]
    else:
        Items_For_Substitution_df = DataFrame()

    return Items_Substitutions_df, Items_For_Substitution_df

# ------------------- HQ_Testing_Items_Connected_Items ------------------- #
def Get_Items_Connected_Items_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Items_list: list, Connection_Type_list: list):
    # Fields
    fields_list = ["Main_Item_No", "No", "Connection_Type", "Quantity"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Because of filters must be done Item per Item
    response_values_List = []
    for Item in Items_list:
        # Filters
        filters_Connections_Types = Get_Field_List_string(fields_list=Connection_Type_list, Join_sign="','")
        filters_list_string = f"""Main_Item_Connection_Type eq 'Item' and Main_Item_No eq '{Item}' and Connection_Type in ('{filters_Connections_Types}')"""

        # Params
        params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

        # Request
        sub_response_values_List, sub_list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_Connected_Items")
        for sub_list in sub_response_values_List:
            response_values_List.append(sub_list)

    # Prepare DataFrame
    list_len =len(response_values_List)
    Main_Item_No_list = []
    No_list = []
    Connection_Type_list = []
    Quantity_list = []
    for index in range(0, list_len):
        Main_Item_No_list.append(response_values_List[index]["Main_Item_No"])
        No_list.append(response_values_List[index]["No"])
        Connection_Type_list.append(response_values_List[index]["Connection_Type"])
        Quantity_list.append(response_values_List[index]["Quantity"])

    response_values_dict = {
        "Main_Item_No": Main_Item_No_list,
        "No": No_list,
        "Connection_Type": Connection_Type_list,
        "Quantity": Quantity_list}
    
    if list_len == 1:
        Items_Connected_Items_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_Connected_Items_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_Connected_Items_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_Connected_Items_df, Columns_list=["Main_Item_No", "No"], Accenting_list=[True, True]) 
    
    # Update Item list for new Items + Gent Items 
    No_list = list(set(No_list))
    if len(No_list) > 0:
        Items_return_list = Get_Items_df(Configuration=Configuration, headers=headers, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Items_list=No_list)
        Items_For_Connected_Items_df = Items_return_list[0]
    else:
        Items_For_Connected_Items_df = DataFrame()

    return Items_Connected_Items_df, Items_For_Connected_Items_df

# ------------------- HQ_Testing_Items_Price_List ------------------- #
def Get_Items_Price_Lists_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["Code", "Status"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = f"""Status eq 'Active'"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_Prices_List")

    # Prepare DataFrame
    Code_list = []
    Status_list = []
    for index in range(0, list_len):
        Code_list.append(response_values_List[index]["Code"])
        Status_list.append(response_values_List[index]["Status"])

    response_values_dict = {
        "Code": Code_list,
        "Status": Status_list}
    
    if list_len == 1:
        Active_Price_Lists_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Active_Price_Lists_df = DataFrame(data=response_values_dict, columns=fields_list)
    Active_Price_Lists_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Active_Price_Lists_df, Columns_list=["Code"], Accenting_list=[True]) 
    
    # BEU Price List Code
    BEU_Price_list = []
    for Price_List_Code in Code_list:
        index = Price_List_Code.find("BEU")
        if index > -1:
            BEU_Price_list.append(Price_List_Code)
        else:
            pass

    return Active_Price_Lists_df, BEU_Price_list

# ------------------- HQ_Testing_Items_Price_Detail_List ------------------- #
def Get_Items_Price_List_detail_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Items_list: list, BEU_Price_list: str, Amount_Type_List: list) -> DataFrame:
    # Fields
    fields_list = ["Price_List_Code", "SourceType", "SourceNo", "Asset_Type", "Asset_No", "Unit_of_Measure_Code", "StartingDate", "EndingDate", "DirectUnitCost"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Items = Get_Field_List_string(fields_list=Items_list, Join_sign="','")
    filters_Price_Lists = Get_Field_List_string(fields_list=BEU_Price_list, Join_sign="','")
    filters_Amount_type = Get_Field_List_string(fields_list=Amount_Type_List, Join_sign="','")
    filters_list_string = f"""Price_List_Code in ('{filters_Price_Lists}') and Asset_Type eq 'Item' and Asset_No in ('{filters_Items}') and Amount_Type in ('{filters_Amount_type}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_Price_Detail_List")

    # Prepare DataFrame
    Price_List_Code = []
    SourceType = []
    SourceNo = []
    Asset_Type = []
    Asset_No = []
    Unit_of_Measure_Code = []
    StartingDate = []
    EndingDate = []
    DirectUnitCost = []
    for index in range(0, list_len):
        Price_List_Code.append(response_values_List[index]["Price_List_Code"])
        SourceType.append(response_values_List[index]["SourceType"])
        SourceNo.append(response_values_List[index]["SourceNo"])
        Asset_Type.append(response_values_List[index]["Asset_Type"])
        Asset_No.append(response_values_List[index]["Asset_No"])
        Unit_of_Measure_Code.append(response_values_List[index]["Unit_of_Measure_Code"])
        StartingDate.append(response_values_List[index]["StartingDate"])
        EndingDate.append(response_values_List[index]["EndingDate"])
        DirectUnitCost.append(response_values_List[index]["DirectUnitCost"])

    response_values_dict = {
        "Price_List_Code": Price_List_Code,
        "SourceType": SourceType,
        "SourceNo": SourceNo,
        "Asset_Type": Asset_Type,
        "Asset_No": Asset_No,
        "Unit_of_Measure_Code": Unit_of_Measure_Code,
        "StartingDate": StartingDate,
        "EndingDate": EndingDate,
        "DirectUnitCost": DirectUnitCost}
    
    if list_len == 1:
        Items_Price_List_Detail_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_Price_List_Detail_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_Price_List_Detail_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_Price_List_Detail_df, Columns_list=["Price_List_Code", "Asset_No"], Accenting_list=[True, True]) 

    return Items_Price_List_Detail_df 

# ------------------- HQ_Testing_Items_Tracking_Codes ------------------- #
def Get_Items_Tracking_Codes_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Item_Tracking_Code_list: list) -> DataFrame:
    # Fields
    fields_list = ["Code", "SN_Purchase_Inbound_Tracking"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Tracking_Codes = Get_Field_List_string(fields_list=Item_Tracking_Code_list, Join_sign="','")
    filters_list_string = f"""Code in ('{filters_Tracking_Codes}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_Tracking_Codes")

    # Prepare DataFrame
    Tracking_code_list = []
    SN_Purchase_Inbound_Tracking_list = []
    for index in range(0, list_len):
        Tracking_code_list.append(response_values_List[index]["Code"])
        SN_Purchase_Inbound_Tracking_list.append(response_values_List[index]["SN_Purchase_Inbound_Tracking"])

    response_values_dict = {
        "Code": Tracking_code_list,
        "SN_Purchase_Inbound_Tracking": SN_Purchase_Inbound_Tracking_list}
    
    if list_len == 1:
        Items_Tracking_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_Tracking_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_Tracking_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_Tracking_df, Columns_list=["Code"], Accenting_list=[True]) 

    return Items_Tracking_df

# ------------------- HQ_Testing_Items_UoM ------------------- #
def Get_Items_UoM_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Items_list: list) -> DataFrame:
    # Fields
    fields_list = ["Item_No", "Code", "Qty_per_Unit_of_Measure", "Weight"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Items = Get_Field_List_string(fields_list=Items_list, Join_sign="','")
    filters_list_string = f"""Item_No in ('{filters_Items}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Items_UoM")

    # Prepare DataFrame
    Item_No_list = []
    Code_list = []
    Qty_per_Unit_of_Measure_list = []
    Weight_List = []
    for index in range(0, list_len):
        Item_No_list.append(response_values_List[index]["Item_No"])
        Code_list.append(response_values_List[index]["Code"])
        Qty_per_Unit_of_Measure_list.append(response_values_List[index]["Qty_per_Unit_of_Measure"])
        Weight_List.append(response_values_List[index]["Weight"])

    response_values_dict = {
        "Item_No": Item_No_list, 
        "Code": Code_list,
        "Qty_per_Unit_of_Measure": Qty_per_Unit_of_Measure_list,
        "Weight": Weight_List}
    
    if list_len == 1:
        Items_UoM_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_UoM_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_UoM_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_UoM_df, Columns_list=["Item_No", "Code"], Accenting_list=[True, True]) 

    return Items_UoM_df


# ------------------- HQ_Testing_Items_UoM ------------------- #
def Get_Items_Distr_Status_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Distribution_Status", "Blocked_for_Purchase"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_BEU_Dist_Status")

    # Prepare DataFrame
    Distribution_Status_list = []
    Blocked_for_Purchase_list = []
    for index in range(0, list_len):
        Distribution_Status_list.append(response_values_List[index]["Distribution_Status"])
        Blocked_for_Purchase_list.append(response_values_List[index]["Blocked_for_Purchase"])

    response_values_dict = {
        "Distribution_Status": Distribution_Status_list, 
        "Blocked_for_Purchase": Blocked_for_Purchase_list}
    
    if list_len == 1:
        Items_Distr_Status_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Items_Distr_Status_df = DataFrame(data=response_values_dict, columns=fields_list)
    Items_Distr_Status_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Items_Distr_Status_df, Columns_list=["Distribution_Status"], Accenting_list=[True]) 

    return Items_Distr_Status_df

# ------------------- HQ_Testing_NVR_FS_Connect ------------------- #
def Get_NVR_FS_Connect_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, File_Connector_Code_list: list) -> DataFrame:
    # Fields
    fields_list = ["Code", "Root_Path_NUS", "Root_Path_Suffix_NUS"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Purchase_Order = Get_Field_List_string(fields_list=File_Connector_Code_list, Join_sign="','")
    filters_list_string = f"""Code in ('{filters_Purchase_Order}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_NVR_FS_Connect")

    # Prepare DataFrame
    NVR_FS_Connect_Code_list = []
    NVR_FS_Connect_Path_list = []
    Root_Path_Suffix_NUS_list = []
    for index in range(0, list_len):
        NVR_FS_Connect_Code_list.append(response_values_List[index]["Code"])
        NVR_FS_Connect_Path_list.append(response_values_List[index]["Root_Path_NUS"])
        Root_Path_Suffix_NUS_list.append(response_values_List[index]["Root_Path_Suffix_NUS"])

    response_values_dict = {
        "Code": NVR_FS_Connect_Code_list,
        "Root_Path_NUS": NVR_FS_Connect_Path_list,
        "Root_Path_Suffix_NUS": Root_Path_Suffix_NUS_list}
    
    if list_len == 1:
        NVR_FS_Connect_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        NVR_FS_Connect_df = DataFrame(data=response_values_dict, columns=fields_list)
    return NVR_FS_Connect_df

# ------------------- HQ_Testing_Plans ------------------- #
def Get_Plants_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Code", "VAT"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Plans")

    # Prepare DataFrame
    Plants_Code_list = []
    Plants_VAT_list = []
    for index in range(0, list_len):
        Plants_Code_list.append(response_values_List[index]["Code"])
        Plants_VAT_list.append(response_values_List[index]["VAT"])

    response_values_dict = {
        "Code": Plants_Code_list,
        "VAT": Plants_VAT_list}
    
    if list_len == 1:
        Plants_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Plants_df = DataFrame(data=response_values_dict, columns=fields_list)
    Plants_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Plants_df, Columns_list=["Code"], Accenting_list=[True]) 

    return Plants_df

# ------------------- HQ_Testing_Shipment_Method ------------------- #
def Get_Shipment_Method_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Shipment_Method")

    # Prepare DataFrame
    Shipment_Method_list = []
    for index in range(0, list_len):
        Shipment_Method_list.append(response_values_List[index]["Code"])

    return Shipment_Method_list

# ------------------- HQ_Testing_Shipping_Agent ------------------- #
def Get_Shipping_Agent_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["BEU_Carrier_ID_NUS"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = """BEU_Carrier_ID_NUS ne ''"""
    
    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Shipping_Agent")

    # Prepare DataFrame
    Shipping_Agent_list = []
    for index in range(0, list_len):
        Shipping_Agent_list.append(response_values_List[index]["BEU_Carrier_ID_NUS"])

    return Shipping_Agent_list


# ------------------- HQ_Testing_Tariff_Numbers ------------------- #
def Get_Tariff_Number_list(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str):
    # Fields
    fields_list = ["No"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Tariff_Numbers")

    # Prepare DataFrame
    Tariff_Number_list = []
    for index in range(0, list_len):
        Tariff_Number_list.append(response_values_List[index]["No"])

    return Tariff_Number_list

# ------------------- HQ_Testing_UoM ------------------- #
def Get_UoM_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Code", "International_Standard_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_UoM")

    # Prepare DataFrame
    Code_list = []
    International_Standard_Code_list = []
    for index in range(0, list_len):
        Code_list.append(response_values_List[index]["Code"])
        International_Standard_Code_list.append(response_values_List[index]["International_Standard_Code"])

    response_values_dict = {
        "Code": Code_list, 
        "International_Standard_Code": International_Standard_Code_list}
    
    if list_len == 1:
        UoM_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        UoM_df = DataFrame(data=response_values_dict, columns=fields_list)
    UoM_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=UoM_df, Columns_list=["Code"], Accenting_list=[True]) 

    return UoM_df

# ------------------- HQ_Testing_Vendor_Service_Functions ------------------- #
def Get_Vendor_Service_Functions_df(Configuration: dict, headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Buy_from_Vendor_No: str) -> DataFrame:
    # Fields
    fields_list = ["Vendor_No", "Vendor_Service_ID", "Vendor_Service_Name"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = f"""Vendor_No eq '{Buy_from_Vendor_No}'"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    response_values_List, list_len = Request_Endpoint(Configuration=Configuration, headers=headers, params=params, tenant_id=tenant_id, NUS_version=NUS_version, NOC=NOC, Environment=Environment, Company=Company, Table="HQ_Testing_Vendor_Service_Functions")

    # Prepare DataFrame
    Vendor_No_list = []
    Vendor_Service_ID_list = []
    Vendor_Service_Name_list = []
    for index in range(0, list_len):
        Vendor_No_list.append(response_values_List[index]["Vendor_No"])
        Vendor_Service_ID_list.append(response_values_List[index]["Vendor_Service_ID"])
        Vendor_Service_Name_list.append(response_values_List[index]["Vendor_Service_Name"])

    response_values_dict = {
        "Vendor_No": Vendor_No_list,
        "Vendor_Service_ID": Vendor_Service_ID_list,
        "Vendor_Service_Name": Vendor_Service_Name_list}
    
    if list_len == 1:
        Vendor_Service_Functions_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Vendor_Service_Functions_df = DataFrame(data=response_values_dict, columns=fields_list)
    Vendor_Service_Functions_df = Pandas_Functions.Dataframe_sort(Sort_Dataframe=Vendor_Service_Functions_df, Columns_list=["Vendor_No"], Accenting_list=[True]) 

    return Vendor_Service_Functions_df