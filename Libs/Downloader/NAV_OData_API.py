from pandas import DataFrame
import requests

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Get_Params(fields_list_string: str, filters_list_string: str) -> dict:
    if (fields_list_string == "") and (filters_list_string == ""):
        params = {}
    elif (fields_list_string != "") and (filters_list_string == ""):
        params = {
            "$select": fields_list_string}
    elif (fields_list_string == "") and (filters_list_string != ""):
        params = {
            "$filter": filters_list_string}
    elif (fields_list_string != "") and (filters_list_string != ""):
        params = {
            "$select": fields_list_string,
            "$filter": filters_list_string}
    else:
        params = {}
    return params
    
def Get_Field_List_string(fields_list: list, Join_sign: str) -> str:
    sub_fields_list_string = f"{Join_sign}".join(fields_list)
    return sub_fields_list_string

def Get_Rid_od_OData_Tag(My_dictionary: dict, Key: str) -> dict:
    My_dictionary.pop(Key)
    return My_dictionary

# ---------------------------------------------------------- Main Functions ---------------------------------------------------------- #
# ------------------- Company List ------------------- #
def Get_Companies(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str) -> list:    
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/api/v2.0/companies"
    response = requests.get(url=url, headers=headers)
    Companies_list = response.json()['value']

    return Companies_list

# ------------------- HQ_Testing_Purchase_Headers ------------------- #
def Get_Purchase_Headers_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Purchase_Order_list: list):
    # Fields
    fields_list = ["No", "Buy_from_Vendor_No", "HQ_Identification_No_NUS", "ShippingConditionFieldNUS", "CompleteDeliveryFieldNUS", "PDICenterFieldNUS", "HQCPDILevelRequestedFieldNUS", "Expected_Receipt_Date", "Promised_Receipt_Date", "Requested_Receipt_Date", "Order_Date"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Purchase_Order = Get_Field_List_string(fields_list=Purchase_Order_list, Join_sign="','")
    filters_list_string = f"""Document_Type eq 'Order' and No in ('{filters_Purchase_Order}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)
    params["$schemaversion"] = "2.1"

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Purchase_Headers"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
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

    for index in range(0, list_len):
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
        "Order_Date": Order_Date_list}
    
    if list_len == 1:
        Purchase_Headers_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Purchase_Headers_df = DataFrame(data=response_values_dict, columns=fields_list)

    Buy_from_Vendor_No_list = list(set(Buy_from_Vendor_No_list))
    return Purchase_Headers_df, Buy_from_Vendor_No_list

# ------------------- HQ_Testing_Purchase_Lines ------------------- #
def Get_Purchase_Lines_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Purchase_Order_list: list):
    # Fields
    fields_list = ["Document_No", "Type", "No", "Description", "Quantity", "Unit_of_Measure_Code", "Direct_Unit_Cost"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Purchase_Order = Get_Field_List_string(fields_list=Purchase_Order_list, Join_sign="','")
    filters_list_string = f"""Document_Type eq 'Order' and Document_No in ('{filters_Purchase_Order}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)
    params["$schemaversion"] = "2.1"

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Purchase_Lines"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    Purchase_Order_No_list = []
    Type_list = []
    No_list = []
    Description_list = []
    Quantity_list = []
    Unit_of_Measure_Code_list = []
    Direct_Unit_Cost_list = []

    for index in range(0, list_len):
        Purchase_Order_No_list.append(response_values_List[index]["Document_No"])
        Type_list.append(response_values_List[index]["Type"])
        No_list.append(response_values_List[index]["No"])
        Description_list.append(response_values_List[index]["Description"])
        Quantity_list.append(response_values_List[index]["Quantity"])
        Unit_of_Measure_Code_list.append(response_values_List[index]["Unit_of_Measure_Code"])
        Direct_Unit_Cost_list.append(response_values_List[index]["Direct_Unit_Cost"])

    response_values_dict = {
        "Document_No": Purchase_Order_No_list,
        "Type": Type_list,
        "No": No_list,
        "Description": Description_list,
        "Quantity": Quantity_list,
        "Unit_of_Measure_Code": Unit_of_Measure_Code_list,
        "Direct_Unit_Cost": Direct_Unit_Cost_list}
    
    if list_len == 1:
        Purchase_Lines_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Purchase_Lines_df = DataFrame(data=response_values_dict, columns=fields_list)

    Items_list = list(set(No_list))
    return Purchase_Lines_df, Items_list

# ------------------- HQ_Testing_HQ_Communication ------------------- #
def Get_HQ_Communication_Setup_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Buy_from_Vendor_No_list: list):
    # Fields
    fields_list = ["HQ_Vendor_Type", "HQ_Vendor_No", "HQ_Identification_No", "Zero_Date", "HQ_Confirm_File_Path", "HQ_PreAdvice_File_Path", "HQ_CPDI_Import_Path", "HQ_Delivery_File_Path", "HQ_Invoice_File_Path", "HQ_PDF_File_Path", "HQ_R_O_Confirm_File_Path", "HQ_R_O_Cr_Memo_File_Path", "File_Connector_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Vendors = Get_Field_List_string(fields_list=Buy_from_Vendor_No_list, Join_sign="','")
    filters_list_string = f"""HQ_Vendor_No in ('{filters_Vendors}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)
    params["$schemaversion"] = "2.1"

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_HQ_Communication"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
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
    return HQ_Communication_Setup_df, File_Connector_Code_list

# ------------------- HQ_Testing_Company_Information ------------------- #
def Get_Company_Information_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Name", "Address", "Post_Code", "City", "Country_Region_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Company_Information"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]
    response_values_dict = Get_Rid_od_OData_Tag(My_dictionary=response_values_List[0], Key="@odata.etag")
    
    Company_Information_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    return Company_Information_df

# ------------------- HQ_Testing_Country_Regions ------------------- #
def Get_Country_Regions_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Code", "ISO_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Country_Regions"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    Code_list = []
    ISO_Code_list = []
    for index in range(0, list_len):
        Code_list.append(response_values_List[index]["Code"])
        ISO_Code_list.append(response_values_List[index]["ISO_Code"])

    response_values_dict = {
        "Code": Code_list,
        "ISO_Code": ISO_Code_list}
    
    if list_len == 1:
        Country_Regions_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Country_Regions_df = DataFrame(data=response_values_dict, columns=fields_list)
    return Country_Regions_df

# ------------------- HQ_Testing_HQ_CPDI_Levels ------------------- #
def Get_HQ_CPDI_Levels_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Level"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_HQ_CPDI_Levels"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    CPDI_Level_list = []
    for index in range(0, list_len):
        CPDI_Level_list.append(response_values_List[index]["Level"])

    response_values_dict = {
        "Level": CPDI_Level_list}
    
    if list_len == 1:
        HQ_CPDI_Levels_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        HQ_CPDI_Levels_df = DataFrame(data=response_values_dict, columns=fields_list)
    return HQ_CPDI_Levels_df


# ------------------- HQ_Testing_HQ_CPDI_Status ------------------- #
def Get_HQ_CPDI_Status_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Status_Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_HQ_CPDI_Status"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    CPDI_Status_list = []
    for index in range(0, list_len):
        CPDI_Status_list.append(response_values_List[index]["Status_Code"])

    response_values_dict = {
        "Status_Code": CPDI_Status_list}
    
    if list_len == 1:
        HQ_CPDI_Status_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        HQ_CPDI_Status_df = DataFrame(data=response_values_dict, columns=fields_list)
    return HQ_CPDI_Status_df

# ------------------- HQ_Testing_HQ_Item_Transport_Register ------------------- #

# ------------------- HQ_Testing_Items ------------------- #

# ------------------- HQ_Testing_Items_BOM ------------------- #

# ------------------- HQ_Testing_Items_Substitution ------------------- #

# ------------------- HQ_Testing_Items_Tracking_Codes ------------------- #
def Get_Tracking_Codes_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Code", "SN_Purchase_Inbound_Tracking"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Items_Tracking_Codes"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    Tracking_code_list = []
    SN_Purchase_Inbound_Tracking_list = []
    for index in range(0, list_len):
        Tracking_code_list.append(response_values_List[index]["Code"])
        SN_Purchase_Inbound_Tracking_list.append(response_values_List[index]["SN_Purchase_Inbound_Tracking"])

    response_values_dict = {
        "Code": Tracking_code_list,
        "SN_Purchase_Inbound_Tracking": SN_Purchase_Inbound_Tracking_list}
    
    if list_len == 1:
        Item_Tracking_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Item_Tracking_df = DataFrame(data=response_values_dict, columns=fields_list)
    return Item_Tracking_df


# ------------------- HQ_Testing_Items_UoM ------------------- #

# ------------------- HQ_Testing_NVR_FS_Connect ------------------- #
def Get_NVR_FS_Connect_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, File_Connector_Code_list: list) -> DataFrame:
    # Fields
    fields_list = ["Code", "Root_Path_NUS"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Purchase_Order = Get_Field_List_string(fields_list=File_Connector_Code_list, Join_sign="','")
    filters_list_string = f"""Code in ('{filters_Purchase_Order}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)
    params["$schemaversion"] = "2.1"

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_NVR_FS_Connect"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    NVR_FS_Connect_Code_list = []
    NVR_FS_Connect_Path_list = []
    for index in range(0, list_len):
        NVR_FS_Connect_Code_list.append(response_values_List[index]["Code"])
        NVR_FS_Connect_Path_list.append(response_values_List[index]["Root_Path_NUS"])

    response_values_dict = {
        "Code": NVR_FS_Connect_Code_list,
        "Root_Path_NUS": NVR_FS_Connect_Path_list}
    
    if list_len == 1:
        NVR_FS_Connect_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        NVR_FS_Connect_df = DataFrame(data=response_values_dict, columns=fields_list)
    return NVR_FS_Connect_df

# ------------------- HQ_Testing_Plans ------------------- #
def Get_Plants_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Code", "VAT"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Plans"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
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
    return Plants_df

# ------------------- HQ_Testing_Shipment_Method ------------------- #
def Get_Shipment_Method_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["Code"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Shipment_Method"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    Shipment_Method_list = []
    for index in range(0, list_len):
        Shipment_Method_list.append(response_values_List[index]["Code"])

    response_values_dict = {
        "Code": Shipment_Method_list}
    
    if list_len == 1:
        Shipment_Method_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Shipment_Method_df = DataFrame(data=response_values_dict, columns=fields_list)
    return Shipment_Method_df

# ------------------- HQ_Testing_Shipping_Agent ------------------- #
def Get_Shipping_Agent_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["BEU_Carrier_ID_NUS"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = """BEU_Carrier_ID_NUS ne ''"""
    
    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Shipping_Agent"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    Shipping_Agent_list = []
    for index in range(0, list_len):
        Shipping_Agent_list.append(response_values_List[index]["BEU_Carrier_ID_NUS"])

    response_values_dict = {
        "BEU_Carrier_ID_NUS": Shipping_Agent_list}
    
    if list_len == 1:
        Shipping_Agent_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Shipping_Agent_df = DataFrame(data=response_values_dict, columns=fields_list)
    return Shipping_Agent_df


# ------------------- HQ_Testing_Tariff_Numbers ------------------- #
def Get_Tariff_Numbers_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str) -> DataFrame:
    # Fields
    fields_list = ["No"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_list_string = ""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Tarif_Numbers"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
    Tariff_Number_list = []
    for index in range(0, list_len):
        Tariff_Number_list.append(response_values_List[index]["No"])

    response_values_dict = {
        "No": Tariff_Number_list}
    
    if list_len == 1:
        Tariff_Numbers_df = DataFrame(data=response_values_dict, columns=fields_list, index=[0])
    else:
        Tariff_Numbers_df = DataFrame(data=response_values_dict, columns=fields_list)
    return Tariff_Numbers_df

# ------------------- HQ_Testing_UoM ------------------- #

# ------------------- HQ_Testing_Vendor_Service_Functions ------------------- #
def Get_Vendor_Service_Functions_df(headers: dict, tenant_id: str, NUS_version: str, NOC: str,  Environment: str, Company: str, Buy_from_Vendor_No_list: list) -> DataFrame:
    # Fields
    fields_list = ["Vendor_No", "Vendor_Service_ID", "Vendor_Service_Name"]
    fields_list_string = Get_Field_List_string(fields_list=fields_list, Join_sign=",")

    # Filters
    filters_Vendors = Get_Field_List_string(fields_list=Buy_from_Vendor_No_list, Join_sign="','")
    filters_list_string = f"""Vendor_No in ('{filters_Vendors}')"""

    # Params
    params = Get_Params(fields_list_string=fields_list_string, filters_list_string=filters_list_string)
    params["$schemaversion"] = "2.1"

    # Request
    url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/NUS_{NUS_version}_{NOC}_{Environment}/ODataV4/Company('{Company}')/HQ_Testing_Vendor_Service_Functions"
    response = requests.get(url=url, headers=headers, params=params)
    response_values_List = response.json()["value"]

    # Prepare DataFrame
    list_len =len(response_values_List)
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
    return Vendor_Service_Functions_df