# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, BooleanVar

import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_CheckBox, WidgetRow_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Date_Picker

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #--------------------------------------------------- Tabs--------------------------------------------------------------------------#
def DEL_Count(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    DEL_Count_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Method"]
    DEL_Count_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Methods_List"])
    Random_Max_count = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["Random_Max_count"]
    Fixed_Count = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Fixed_Options"]["Count"]
    DEL_Count_Method_Variable = StringVar(master=Frame, value=DEL_Count_Method, name="DEL_Count_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Count_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Delivery Count", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definition how many Deliveries will be created.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    DEL_Count_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Count_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed count", Value=Fixed_Count, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Counts", "Fixed_Options", "Count"], Validation="Integer")

    Del_Count_Random_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_Count_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Random Count", Label_Size="Field_Label", Font_Size="Section_Separator")
    DEL_Random_Max_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Count_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Maximal count", Value=Random_Max_count, placeholder_text="Maximal delivery Count.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Counts", "Random_Options", "Random_Max_count"], Validation="Integer")
    
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Prompt"], Freeze_fields=[[],[DEL_Count_FIX_Row],[DEL_Count_FIX_Row]])
    DEL_Count_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Count_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=DEL_Count_Method_Variable, Values=DEL_Count_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Counts", "Method"], Field_list=[DEL_Random_Max_Row, DEL_Count_FIX_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_Count_Widget.Add_row(Rows=[DEL_Count_Row, DEL_Count_FIX_Row, Del_Count_Random_Section_Row, DEL_Random_Max_Row])

    return Del_Count_Widget

def DEL_Number(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Fixed_Options"]["Number"]
    DEL_Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="DEL_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Number_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Delivery Number.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    NUM_CON_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=Fixed_Number, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Number", "Fixed_Options", "Number"])

    Del_Auto_Num_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_Number_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=Automatic_Prefix, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Number", "Automatic_Options", "Prefix"])

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic", "Prompt"], Freeze_fields=[[AUT_Prefix_Row],[NUM_CON_FIX_Row],[AUT_Prefix_Row, NUM_CON_FIX_Row]])
    DEL_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=DEL_Numbers_Method_Variable, Values=Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Number", "Method"], Field_list=[AUT_Prefix_Row, NUM_CON_FIX_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_Number_Widget.Add_row(Rows=[DEL_Number_Row, NUM_CON_FIX_Row, Del_Auto_Num_Section_Row, AUT_Prefix_Row])

    return Del_Number_Widget

def Item_Delivery_Assignment(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    DEL_Assignment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["Method"]
    DEL_Assignment_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["Methods_List"])
    DEL_FOCH_with_Main = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["FreeOfCharge_with_Main"]
    DEL_Assignment_Method_Variable = StringVar(master=Frame, value=DEL_Assignment_Method, name="DEL_Assignment_Method_Variable")
    DEL_FOCH_with_Main_Variable = BooleanVar(master=Frame, value=DEL_FOCH_with_Main, name="DEL_FOCH_with_Main_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Items_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Item Assignment to Delivery", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="How program will select Items and Qty to the Delivery.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    DEL_Assignment_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Items_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=DEL_Assignment_Method_Variable, Values=DEL_Assignment_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Item_Delivery_Assignment", "Method"], GUI_Level_ID=GUI_Level_ID) 
    DEL_FOCH_with_Main_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Del_Items_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="FOCHs with Machine", Variable=DEL_FOCH_with_Main_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Item_Delivery_Assignment", "FreeOfCharge_with_Main"])

    # Add Fields to Widget Body
    Del_Items_Widget.Add_row(Rows=[DEL_Assignment_Row, DEL_FOCH_with_Main_Row])

    return Del_Items_Widget

def Delivery_Date(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Delivery_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Method"]
    Delivery_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Methods_List"])
    DEL_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Fixed_Options"]["Fix_Date"]
    DEL_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Random_Options"]["From"]
    DEL_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Random_Options"]["To"]
    Delivery_Dates_Method_Variable = StringVar(master=Frame, value=Delivery_Dates_Method, name="Delivery_Dates_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Dates_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Delivery Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    DEL_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Del_Dates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=DEL_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)

    Interval_Date_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_Dates_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Interval Date", Label_Size="Field_Label", Font_Size="Section_Separator")
    DEL_Random_From_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Dates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - From CD +", Value=DEL_Rand_From_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Random_Options", "From"], Validation="Integer")
    DEL_Random_To_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Dates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - To CD +", Value=DEL_Rand_To_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Random_Options", "To"], Validation="Integer")

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Prompt"], Freeze_fields=[[DEL_Random_From_Row, DEL_Random_To_Row],[DEL_Fixed_Date_Row],[DEL_Fixed_Date_Row, DEL_Random_From_Row, DEL_Random_To_Row]])
    Delivery_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Dates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Delivery_Dates_Method_Variable, Values=Delivery_Dates_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Method"], Field_list=[DEL_Fixed_Date_Row, DEL_Random_From_Row, DEL_Random_To_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_Dates_Widget.Add_row(Rows=[Delivery_Date_Method_Row, DEL_Fixed_Date_Row, Interval_Date_Section_Row, DEL_Random_From_Row, DEL_Random_To_Row])

    return Del_Dates_Widget

def Serial_Numbers(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    SN_Machines = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Generate"]["Machines"]
    SN_Tracked_Items = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Generate"]["Tracked"]
    SN_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Prefix"]
    SN_Middle_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Method"]
    SN_Middle_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Methods_List"])
    SN_Middle_Manual = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Fixed"]
    SN_Suffix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Suffix"]
    SN_Machines_Variable = BooleanVar(master=Frame, value=SN_Machines, name="SN_Machines_Variable")
    SN_Tracked_Items_Variable = BooleanVar(master=Frame, value=SN_Tracked_Items, name="SN_Tracked_Items_Variable")
    SN_Middle_Method_Variable = StringVar(master=Frame, value=SN_Middle_Method, name="Serial_Number_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_SN_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Serial Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Serial Numbers creation options.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    SN_Machines_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Del_SN_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Generate for all Machines", Variable=SN_Machines_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Generate", "Machines"])
    SN_Tracked_Items_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Del_SN_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Generate for tracked Items", Variable=SN_Tracked_Items_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Generate", "Tracked"])

    Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_SN_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="SN Number Creation", Label_Size="Field_Label", Font_Size="Section_Separator")
    SN_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_SN_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=SN_Prefix, placeholder_text="Prefix.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Prefix"])
    SN_Middle_Man_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_SN_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed middle", Value=SN_Middle_Manual, placeholder_text="Manual Middle part.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Middle", "Fixed"])
    SN_Suffix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_SN_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Suffix", Value=SN_Suffix, placeholder_text_color="#949A9F")
    
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Item No", "DateTime stamp"], Freeze_fields=[[SN_Suffix_Row],[SN_Middle_Man_Row, SN_Suffix_Row],[SN_Middle_Man_Row, SN_Suffix_Row]])
    SN_Middle_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_SN_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Middle Method", Variable=SN_Middle_Method_Variable, Values=SN_Middle_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Middle", "Method"], Field_list=[SN_Middle_Man_Row, SN_Suffix_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_SN_Widget.Add_row(Rows=[SN_Machines_Row, SN_Tracked_Items_Row, Section_Row, SN_Prefix_Row, SN_Middle_Method_Row, SN_Middle_Man_Row, SN_Suffix_Row])

    return Del_SN_Widget

def Carrier_ID(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Carrier_ID_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Method"]
    Carrier_ID_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Methods_List"])
    Carrier_ID_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Fixed_Options"]["Fix_Carrier"]
    Carrier_ID_Method_Variable = StringVar(master=Frame, value=Carrier_ID_Method, name="Carrier_ID_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Carrier_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Carrier", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Carrier_ID_Fixed_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Carrier_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Carrier", Value=Carrier_ID_Fixed, placeholder_text="Carrier from Shipping Agent.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Carrier_ID", "Fixed_Options", "Fix_Carrier"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty"], Freeze_fields=[[],[Carrier_ID_Fixed_Row],[Carrier_ID_Fixed_Row]])
    Carrier_ID_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Carrier_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Carrier_ID_Method_Variable, Values=Carrier_ID_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Carrier_ID", "Method"], Field_list=[Carrier_ID_Fixed_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_Carrier_Widget.Add_row(Rows=[Carrier_ID_Method_Row, Carrier_ID_Fixed_Row])

    return Del_Carrier_Widget

def Shipment_Method(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Shipment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Method"]
    Shipment_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Methods_List"])
    Shipment_Method_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Fixed_Options"]["Fixed_Shipment_Method"]
    Shipment_Method_Variable = StringVar(master=Frame, value=Shipment_Method, name="Shipment_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Ship_Method_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Shipment Method", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Ship_Method_Fixed_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Ship_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Shp. Method", Value=Shipment_Method_Fixed, placeholder_text="Fixed Shipment Method.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Shipment_Method", "Fixed_Options", "Fixed_Shipment_Method"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty"], Freeze_fields=[[],[Ship_Method_Fixed_Row],[Ship_Method_Fixed_Row]])
    Shipment_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Ship_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Shipment_Method_Variable, Values=Shipment_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Shipment_Method", "Method"], Field_list=[Ship_Method_Fixed_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_Ship_Method_Widget.Add_row(Rows=[Shipment_Method_Row, Ship_Method_Fixed_Row])
 
    return Del_Ship_Method_Widget

def BillOfLanding(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    BOL_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Method"]
    BOL_Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Methods_List"])
    BOL_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Automatic_Options"]["Prefix"]
    BOL_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Fixed_Options"]["Fixed_BOL"]
    BOL_Numbers_Method_Variable = StringVar(master=Frame, value=BOL_Numbers_Method, name="BOL_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_Bill_Land_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Bill of Landing", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Bill of Landing number logic assignment.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    NUM_BOL_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Bill_Land_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=BOL_Fixed_Number, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "BillOfLanding", "Number", "Fixed_Options", "Fixed_BOL"])
    
    Aut_BOL_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_Bill_Land_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_Bill_Land_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=BOL_Automatic_Prefix, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "BillOfLanding", "Number", "Automatic_Options", "Prefix"])

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic", "Empty"], Freeze_fields=[[AUT_Prefix_Row],[NUM_BOL_FIX_Row],[NUM_BOL_FIX_Row, AUT_Prefix_Row]])
    BOL_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_Bill_Land_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BOL_Numbers_Method_Variable, Values=BOL_Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "BillOfLanding", "Number", "Method"], Field_list=[NUM_BOL_FIX_Row, AUT_Prefix_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_Bill_Land_Widget.Add_row(Rows=[BOL_Number_Row, NUM_BOL_FIX_Row, Aut_BOL_Section_Row, AUT_Prefix_Row])
 
    return Del_Bill_Land_Widget

def Packages_Numbers(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Pack_Number_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Method"]
    Pack_Number_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Methods_List"])
    Pack_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Automatic_Options"]["Prefix"]
    Pack_Max_Records = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Automatic_Options"]["Max_Packages_Records"]
    Pack_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Fixed_Options"]["Fixed_Package_No"]
    Pack_Number_Method_Variable = StringVar(master=Frame, value=Pack_Number_Method, name="Pack_Number_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_PACK_Num_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Package Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Package numbers creation logic.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    DEL_PACK_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_Num_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=Pack_Fixed_Number, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Fixed_Options", "Fixed_Package_No"])

    Aut_PACK_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_PACK_Num_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    DEL_Pack_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_Num_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=Pack_Prefix, placeholder_text="Prefix.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Automatic_Options", "Prefix"])
    DEL_Pack_MAX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_Num_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Maximal Package Count", Value=Pack_Max_Records, placeholder_text="Fill maximal Package count per Delivery.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Automatic_Options", "Max_Packages_Records"], Validation="Integer")

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic"], Freeze_fields=[[DEL_Pack_Prefix_Row, DEL_Pack_MAX_Row],[DEL_PACK_FIX_Row]])
    Pack_Number_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_Num_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Pack_Number_Method_Variable, Values=Pack_Number_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Method"], Field_list=[DEL_PACK_FIX_Row, DEL_Pack_Prefix_Row, DEL_Pack_MAX_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_PACK_Num_Widget.Add_row(Rows=[Pack_Number_Method_Row, DEL_PACK_FIX_Row, Aut_PACK_Section_Row, DEL_Pack_Prefix_Row, DEL_Pack_MAX_Row])
 
    return Del_PACK_Num_Widget

def Packages_Plants(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Pack_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Method"]
    Pack_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Methods_List"])
    Pack_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Pack_Fixed_Plant_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Plant_List"])
    Pack_Plant_Method_Variable = StringVar(master=Frame, value=Pack_Plant_Method, name="Pack_Plant_Method_Variable")
    Pack_Fixed_Plant_Variable = StringVar(master=Frame, value=Pack_Fixed_Plant, name="Pack_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_PACK_Plant_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Pack_Plant_Fixed_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Plant", Variable=Pack_Fixed_Plant_Variable, Values=Pack_Fixed_Plant_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Plants", "Fixed_Options", "Fixed_Plant"], GUI_Level_ID=GUI_Level_ID) 
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[Pack_Plant_Fixed_Row],[Pack_Plant_Fixed_Row],[Pack_Plant_Fixed_Row]])
    Pack_Number_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Pack_Plant_Method_Variable, Values=Pack_Plant_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Plants", "Method"], Field_list=[Pack_Plant_Fixed_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_PACK_Plant_Widget.Add_row(Rows=[Pack_Number_Method_Row, Pack_Plant_Fixed_Row])
 
    return Del_PACK_Plant_Widget

def Packages_UOM(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Pack_Weight_UoM_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Weight"]["Method"]
    Pack_Weight_UoM_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Weight"]["Methods_List"])
    Pack_Weight_UoM_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Weight"]["Fixed_Options"]["Fixed_Weight_UoM"]
    Pack_Volume_UoM_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Volume"]["Method"]
    Pack_Volume_UoM_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Volume"]["Methods_List"])
    Pack_Volume_UoM_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Unit_Of_Measure"]["Volume"]["Fixed_Options"]["Fixed_Volume_UoM"]
    Pack_Weight_UoM_Method_Variable = StringVar(master=Frame, value=Pack_Weight_UoM_Method, name="Pack_Weight_UoM_Method_Variable")
    Pack_Volume_UoM_Method_Variable = StringVar(master=Frame, value=Pack_Volume_UoM_Method, name="Pack_Volume_UoM_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_PACK_UoM_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Unit of Measure", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Packages unit of measure for measurements.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Weight_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_PACK_UoM_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Weight", Label_Size="Field_Label", Font_Size="Section_Separator")
    Pack_Weight_UoM_Fixed_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_UoM_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Weight UoM", Value=Pack_Weight_UoM_Fixed, placeholder_text="Fixed weight UoM.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Weight", "Fixed_Options", "Fixed_Weight_UoM"])
    Weight_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty"], Freeze_fields=[[],[Pack_Weight_UoM_Fixed_Row],[Pack_Weight_UoM_Fixed_Row]])
    Pack_Weight_UoM_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_UoM_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Pack_Weight_UoM_Method_Variable, Values=Pack_Weight_UoM_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Weight", "Method"], Field_list=[Pack_Weight_UoM_Fixed_Row], Field_Blocking_dict=Weight_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Volume_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_PACK_UoM_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Volume", Label_Size="Field_Label", Font_Size="Section_Separator")
    Pack_Volume_UoM_Fixed_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_UoM_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Volume UoM", Value=Pack_Volume_UoM_Fixed, placeholder_text="Fixed volume UoM.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Volume", "Fixed_Options", "Fixed_Volume_UoM"])
    Volume_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty"], Freeze_fields=[[],[Pack_Volume_UoM_Fixed_Row],[Pack_Volume_UoM_Fixed_Row]])
    Pack_Volume_UoM_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_UoM_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Pack_Volume_UoM_Method_Variable, Values=Pack_Volume_UoM_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Volume", "Method"], Field_list=[Pack_Volume_UoM_Fixed_Row], Field_Blocking_dict=Volume_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_PACK_UoM_Widget.Add_row(Rows=[Weight_Section_Row, Pack_Weight_UoM_Method_Row, Pack_Weight_UoM_Fixed_Row, Volume_Section_Row, Pack_Volume_UoM_Method_Row, Pack_Volume_UoM_Fixed_Row])

    return Del_PACK_UoM_Widget

def EXIDV2(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    EXIDV2_Assign_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Method"]
    EXIDV2_Assign_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Methods_List"])
    EXIDV2_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Method"]
    EXIDV2_Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Methods_List"])
    EXIDV2_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Automatic_Options"]["Prefix"]
    EXIDV2_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["EXIDV2"]["Number"]["Fixed_Options"]["Fixed_EXIDV2"]
    EXIDV2_Assign_Method_Variable = StringVar(master=Frame, value=EXIDV2_Assign_Method, name="EXIDV2_Assign_Method_Variable")
    EXIDV2_Numbers_Method_Variable = StringVar(master=Frame, value=EXIDV2_Numbers_Method, name="EXIDV2_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Del_PACK_EXIDV_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="EXIDV2", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="EXIDV2 Number logic assignment.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    NUM_EXIDV2_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_EXIDV_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=EXIDV2_Fixed_Number, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Number", "Fixed_Options", "Fixed_EXIDV2"])
    
    Automatic_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_PACK_EXIDV_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Del_PACK_EXIDV_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=EXIDV2_Automatic_Prefix, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Number", "Automatic_Options", "Prefix"])
    EXIDV2_Number_Menu_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic", "Empty"], Freeze_fields=[[AUT_Prefix_Row],[NUM_EXIDV2_FIX_Row],[NUM_EXIDV2_FIX_Row, AUT_Prefix_Row]])
    EXIDV2_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_EXIDV_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=EXIDV2_Numbers_Method_Variable, Values=EXIDV2_Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Number", "Method"], Field_list=[NUM_EXIDV2_FIX_Row, AUT_Prefix_Row], Field_Blocking_dict=EXIDV2_Number_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Assign_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Del_PACK_EXIDV_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Package Assign Method", Label_Size="Field_Label", Font_Size="Section_Separator")
    EXIDV2_Assign_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Del_PACK_EXIDV_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Assign method", Variable=EXIDV2_Assign_Method_Variable, Values=EXIDV2_Assign_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Method"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Del_PACK_EXIDV_Widget.Add_row(Rows=[EXIDV2_Number_Row, NUM_EXIDV2_FIX_Row, Automatic_Section_Row, AUT_Prefix_Row, Assign_Section_Row, EXIDV2_Assign_Row])

    return Del_PACK_EXIDV_Widget

