def Get_Lines(pandas, pyodbc):
    def update_string(inset_value):
        try:
            inset_value = str(inset_value).replace(" ", "_")
            return inset_value
        except:
            return inset_value

    def test_float(inset_value):
        while True:
            try:
                number = float(inset_value)
                number = round(number, 2)
                return number
            except ValueError:
                inset_value = input(f"The {inset_value} is not float number, test again: ")

    # Data downloaded from DB
    NUS2_NOC_list = ["NAV2009", "BBG", "BBL", "BCZ", "BFI", "BGR", "BHN", "BNO", "BPT", "BRO", "BSK", "BSW", "BTR", "BUR"]
    NUS3_NOC_list = ["COREQA", "BDK", "BPL", "BHR", "BSL", "BIH", "BRS", "BR"]

    NUS_Version = ""
    while NUS_Version != "NUS2" and NUS_Version != "NUS3":
        NUS_Version = update_string(input("Which NUS Version you want to select as data source? [NUS2/NUS3]: "))
    Data_System = ""
    while Data_System != "QA" and Data_System != "PRD":
        Data_System = update_string(input("Which DB you want to select as data source? [QA/PRD]: "))
    if NUS_Version == "NUS2":
        Data_NOC = ""
        while Data_NOC not in NUS2_NOC_list:
            Data_NOC = update_string(input(f"Which NOC you want to select? {NUS2_NOC_list} [Code]: "))
        if Data_System == "QA" and Data_NOC == "BSW":
            Data_System = "QA1"
        if Data_System == "QA" and Data_NOC == "BCZ":
            Data_System = "QA2"
    elif NUS_Version == "NUS3":
        Data_NOC = ""
        while Data_NOC not in NUS3_NOC_list:
            Data_NOC = update_string(input(f"Which NOC you want to select? {NUS3_NOC_list} [Code]: "))
    else:
        pass

    # Database connection preparation
    if NUS_Version == "NUS2":
        if Data_System == "QA" or Data_System == "QA1" or Data_System == "QA2":
            server = 'kmnus2qadbs01.erp.kme.intern'
        else:
            server = 'kmnus2prddbs01.erp.kme.intern'
    elif NUS_Version == "NUS3":
        if Data_System == "QA":
            server = 'kmnavqdbs02.bs.kme.intern'
        else:
            server = 'kmnavpdbs02.bs.kme.intern'
    else:
        print("No NUS Version selectd")
        exit

    # Database connection
    database = update_string(Data_NOC+Data_System)
    dabase_schama = "dbo"
    Connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    cnxn = pyodbc.connect(Connection_string, autocommit=True)
    cursor = cnxn.cursor()

    # Company Selection
    company_list = []
    cursor.execute(f'SELECT [Name] FROM [{database}].[{dabase_schama}].[Company]')
    for row in cursor.fetchall():
        company_list.append(row[0])
    Company = ""
    while Company not in company_list:
        Company = str(input(f"Select Company you want {company_list}: "))

    # Purchase Order selection
    Purchase_Order = update_string(input("Write Purchae Order Number from which you want to download lines? [Code]: "))

    # Data Download
    Item_List = []
    Line_Type_list = []
    Item_Line_Quantity_list = []
    Item_Unit_of_Measure_list = []
    Item_Unit_Price_list = []
    Main_BOM_Item_list = []
    Item_Connected_to_BOM_list = []
    BOM_Item_Relation_list = []
    Item_Free_Of_Charge_list = []
    Item_Free_Of_Charge_Relation_list = []
    Item_SN_Tracking_list = []
    HQ_Confirmation_Line_Flag_Use_list = []
    HQ_Confirmation_Line_Flag_list = []
    HQ_SUB_New_Item_list = []

    Downloaded_PO_Lines = []
    Downloaded_Item_NOs = []
    Downloaded_Items_Tracking_Codes = []

    Downloaded_Tracking_Code_list = []
    Downloaded_Tracking_Value_list = []

    # Purchase Line
    cursor.execute(f"SELECT [No_],[Line No_],[Quantity],[Unit Cost (LCY)],[Unit of Measure Code]  FROM [{database}].[{dabase_schama}].[{Company}$Purchase Line] WHERE [Document No_] = '{Purchase_Order}' AND [Document Type] = 1 AND [Type] = 2")
    for row in cursor.fetchall():
        Downloaded_PO_Lines.append(row)

    # Item Tracking Codes - Checker from all Items
    for Item in Downloaded_PO_Lines:
        Current_Item = Item[0]
        cursor.execute(f"SELECT [Item Tracking Code] FROM [{database}].[{dabase_schama}].[{Company}$Item] WHERE [No_] = '{Current_Item}'")
        for row in cursor.fetchall():
            Downloaded_Item_NOs.append(Current_Item)
            Downloaded_Items_Tracking_Codes.append(row[0])
    Unique_Tracking_Codes = list(set(Downloaded_Items_Tracking_Codes))

    # Tracking Code mapping from Code to Track/NonTracked on Purchase
    for Tracking in Unique_Tracking_Codes:
        cursor.execute(f"SELECT [SN Purchase Inbound Tracking] FROM [{database}].[{dabase_schama}].[{Company}$Item Tracking Code] WHERE [Code] = '{Tracking}'")
        for row in cursor.fetchall():
            Downloaded_Tracking_Code_list.append(str(Tracking))
            Downloaded_Tracking_Value_list.append(str(row[0]))

    cnxn.commit()
    cursor.close()

    # Item - Tracking Code df
    Item_Tracking_Dict = {
        "Item_No": Downloaded_Item_NOs,
        "Tracking_Code":Downloaded_Items_Tracking_Codes}
    Item_Tracking_df = pandas.DataFrame(data=Item_Tracking_Dict, columns=Item_Tracking_Dict.keys())
    Item_Tracking_df.Name = "Item_Tracking_df"

    # Tracking Code - Tracking df
    Tracking_Dict = {
        "Tracking_Code": Downloaded_Tracking_Code_list,
        "Tracking_Value":Downloaded_Tracking_Value_list}
    Tracking_df = pandas.DataFrame(data=Tracking_Dict, columns=Tracking_Dict.keys())
    Tracking_df.Name = "Tracking_df"


    # Item definition
    for line in Downloaded_PO_Lines:
        # Tracking definition for current Item
        Current_Item = str(line[0])
        Current_Tracking_Code = Item_Tracking_df[(Item_Tracking_df["Item_No"] == str(Current_Item))]
        Current_Tracking_Value = Tracking_df[(Tracking_df["Tracking_Code"] == str(Current_Tracking_Code.iloc[0]["Tracking_Code"]))]
        if str(Current_Tracking_Value.iloc[0]["Tracking_Value"]) == "0":
            Current_Tracking_Value_text = "N"
        elif str(Current_Tracking_Value.iloc[0]["Tracking_Value"]) == "1":
            Current_Tracking_Value_text = "Y"
        else:
            Current_Tracking_Value_text = "N"
        # List appends
        Item_List.append(str(line[0]))
        Line_Type_list.append(str("ITEM"))
        Item_Line_Quantity_list.append(str(int(line[2])))
        Item_Unit_of_Measure_list.append(str(line[4]))
        Item_Unit_Price_list.append(str(test_float(line[3])))
        Main_BOM_Item_list.append(str("N"))
        Item_Connected_to_BOM_list.append(str("N"))
        BOM_Item_Relation_list.append(str(""))
        Item_Free_Of_Charge_list.append(str("N"))
        Item_Free_Of_Charge_Relation_list.append(str(""))
        Item_SN_Tracking_list.append(Current_Tracking_Value_text)
        HQ_Confirmation_Line_Flag_Use_list.append(str("N"))
        HQ_Confirmation_Line_Flag_list.append(str(""))
        HQ_SUB_New_Item_list.append(str(""))


    Items_Dict = {
        "Item_No": list(Item_List),
        "Line_Type": list(Line_Type_list),
        "Item_Line_Quantity": list(Item_Line_Quantity_list),
        "Item_Unit_of_Measure": list(Item_Unit_of_Measure_list),
        "Item_Unit_Price": list(Item_Unit_Price_list),
        "Main_BOM_Item": list(Main_BOM_Item_list),
        "Item_Connected_to_BOM": list(Item_Connected_to_BOM_list),
        "BOM_Item_Relation": list(BOM_Item_Relation_list),
        "Item_Free_Of_Charge": list(Item_Free_Of_Charge_list),
        "Item_Free_Of_Charge_Relation": list(Item_Free_Of_Charge_Relation_list),
        "Item_SN_Tracking": list(Item_SN_Tracking_list),
        "HQ_Confirmation_Line_Flag_Use": list(HQ_Confirmation_Line_Flag_Use_list),
        "HQ_Confirmation_Line_Flag": list(HQ_Confirmation_Line_Flag_list),
        "HQ_SUB_New_Item": list(HQ_SUB_New_Item_list)}
    return Items_Dict