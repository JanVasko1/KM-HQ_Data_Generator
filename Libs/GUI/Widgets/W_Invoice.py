# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, BooleanVar

import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Date_Picker, WidgetRow_CheckBox


# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #--------------------------------------------------- Tabs--------------------------------------------------------------------------#
# --------------------------------------------------------------------------- Purchase Orders ---------------------------------------------------------------------------#
def PO_INV_Number(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]

    Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PO_INV_Number_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Invoice Number.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    NUM_INV_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=Fixed_Number, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Fixed_Options", "Number"])

    Section_Row = Widget_Section_Row(Configuration=Configuration, master=PO_INV_Number_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    PO_AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=Automatic_Prefix, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Automatic_Options", "Prefix"])

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic", "Prompt"], Freeze_fields=[[PO_AUT_Prefix_Row],[NUM_INV_FIX_Row],[NUM_INV_FIX_Row, PO_AUT_Prefix_Row]])
    PO_INV_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Numbers_Method_Variable, Values=Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Method"], Field_list=[NUM_INV_FIX_Row, PO_AUT_Prefix_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PO_INV_Number_Widget.Add_row(Rows=[PO_INV_Number_Row, NUM_INV_FIX_Row, Section_Row, PO_AUT_Prefix_Row])

    return PO_INV_Number_Widget


def PO_Price_Currency(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Method"]
    Currency_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Methods_List"])
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Method"]
    Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Methods_List"])
    Price_Method_Variable = StringVar(master=Frame, value=Price_Method, name="Price_Method_Variable")
    Currency_Method_Variable = StringVar(master=Frame, value=Currency_Method, name="Currency_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PO_INV_Price_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Invoice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Prices_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Price", Variable=Price_Method_Variable, Values=Price_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Prices", "Method"], GUI_Level_ID=GUI_Level_ID) 
    Fixed_Currency_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Currency", Value=Fixed_Currency, placeholder_text="Manual Currency.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Currency", "Fixed_Options", "Fix_Currency"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Purchase Order", "From Confirmation"], Freeze_fields=[[],[Fixed_Currency_Row],[Fixed_Currency_Row]])
    Currency_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Currency", Variable=Currency_Method_Variable, Values=Currency_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Currency", "Method"], Field_list=[Fixed_Currency_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PO_INV_Price_Widget.Add_row(Rows=[Prices_Method_Row, Currency_Method_Row, Fixed_Currency_Row])

    return PO_INV_Price_Widget

def PO_Invoice_Date(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Method"]
    Posting_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Methods_List"])
    INV_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]
    INV_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Random_Options"]["From"]
    INV_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Random_Options"]["To"]
    Posting_Date_Method_Variable = StringVar(master=Frame, value=Posting_Date_Method, name="Posting_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PO_INV_Date_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Invoice Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Vendor Invoice Date.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    INV_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=PO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=INV_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)

    Section_Row = Widget_Section_Row(Configuration=Configuration, master=PO_INV_Date_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Random Date interval", Label_Size="Field_Label", Font_Size="Section_Separator")
    INV_Random_From_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - From CD +", Value=INV_Rand_From_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Random_Options", "From"], Validation="Integer")
    INV_Random_To_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - To CD +", Value=INV_Rand_To_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Random_Options", "To"], Validation="Integer")

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Today", "Prompt"], Freeze_fields=[[INV_Random_From_Row, INV_Random_To_Row],[INV_Fixed_Date_Row],[INV_Fixed_Date_Row, INV_Random_From_Row, INV_Random_To_Row],[INV_Fixed_Date_Row, INV_Random_From_Row, INV_Random_To_Row]])
    Invoice_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Posting_Date_Method_Variable, Values=Posting_Date_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Method"], Field_list=[INV_Fixed_Date_Row, INV_Random_From_Row, INV_Random_To_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PO_INV_Date_Widget.Add_row(Rows=[Invoice_Date_Method_Row, INV_Fixed_Date_Row, Section_Row, INV_Random_From_Row, INV_Random_To_Row])

    return PO_INV_Date_Widget

def PO_Plant(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Method"]
    Inv_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Methods_List"])
    Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Plants_List"])
    Inv_Plant_Method_Variable = StringVar(master=Frame, value=Inv_Plant_Method, name="Inv_Plant_Method_Variable")
    Inv_Fixed_Plant_Variable = StringVar(master=Frame, value=Inv_Fixed_Plant, name="Inv_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PO_INV_Plant_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    PO_INV_Plant_Fixed_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Plant", Variable=Inv_Fixed_Plant_Variable, Values=Inv_Fixed_Plants_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Plants", "Fixed_Options", "Fixed_Plant"], GUI_Level_ID=GUI_Level_ID) 
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "From Delivery", "Empty", "Prompt"], Freeze_fields=[[],[PO_INV_Plant_Fixed_Row],[PO_INV_Plant_Fixed_Row],[PO_INV_Plant_Fixed_Row],[PO_INV_Plant_Fixed_Row]])
    PO_INV_Plant_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Inv_Plant_Method_Variable, Values=Inv_Plant_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Plants", "Method"], Field_list=[PO_INV_Plant_Fixed_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PO_INV_Plant_Widget.Add_row(Rows=[PO_INV_Plant_Method_Row, PO_INV_Plant_Fixed_Row])

    return PO_INV_Plant_Widget

def PO_CountryOrigin(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Method"]
    Count_Origin_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Methods_List"])
    Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]
    Count_Origin_Method_Variable = StringVar(master=Frame, value=Count_Origin_Method, name="Count_Origin_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PO_INV_Origin_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Country of Origin", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Country Codes in Invoice. \n Always takes 4 major codes + 5 random from Business Central.", GUI_Level_ID=GUI_Level_ID)

    # Fields 
    Fixed_Count_Origin_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Origin_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Country Code", Value=Fixed_Count_Origin, placeholder_text="Manual Country Code.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Country_Of_Origin", "Fixed_Options", "Fix_Country_Of_Origin"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[Fixed_Count_Origin_Row],[Fixed_Count_Origin_Row],[Fixed_Count_Origin_Row]])
    PO_INV_Plant_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Origin_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Count_Origin_Method_Variable, Values=Count_Origin_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Country_Of_Origin", "Method"], Field_list=[Fixed_Count_Origin_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PO_INV_Origin_Widget.Add_row(Rows=[PO_INV_Plant_Method_Row, Fixed_Count_Origin_Row])

    return PO_INV_Origin_Widget

def PO_Tariff(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Method"]
    Tariff_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Methods_List"])
    Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]
    Tariff_Method_Variable = StringVar(master=Frame, value=Tariff_Method, name="Tariff_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PO_INV_Tariff_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Tariffs", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define tariffs numbers in Invoice. \n Always takes only random 10 tariffs from Business Central.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Fixed_Tariff_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PO_INV_Tariff_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Tariff code", Value=Fixed_Tariff, placeholder_text="Manual Tariff Code.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Tariff", "Fixed_Options", "Fix_Tariff"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[Fixed_Tariff_Row],[Fixed_Tariff_Row],[Fixed_Tariff_Row]])
    Tariff_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PO_INV_Tariff_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Tariff_Method_Variable, Values=Tariff_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Tariff", "Method"], Field_list=[Fixed_Tariff_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PO_INV_Tariff_Widget.Add_row(Rows=[Tariff_Method_Row, Fixed_Tariff_Row])

    return PO_INV_Tariff_Widget

# --------------------------------------------------------------------------- BackBone Billing Invoices ---------------------------------------------------------------------------#
def BB_INV_Number(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Method"]
    BB_Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Methods_List"])
    BB_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Automatic_Options"]["Prefix"]
    BB_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Fixed_Options"]["Number"]
    BB_Numbers_Method_Variable = StringVar(master=Frame, value=BB_Numbers_Method, name="BB_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Number_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Invoice Number.", GUI_Level_ID=GUI_Level_ID)

    # Fields 
    BB_NUM_INV_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=BB_Fixed_Number, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Number", "Fixed_Options", "Number"])

    Section_Row = Widget_Section_Row(Configuration=Configuration, master=BB_INV_Number_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    BB_AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=BB_Automatic_Prefix, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Number", "Automatic_Options", "Prefix"])

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic", "Prompt"], Freeze_fields=[[BB_AUT_Prefix_Row],[BB_NUM_INV_FIX_Row],[BB_NUM_INV_FIX_Row, BB_AUT_Prefix_Row]])
    BB_INV_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Numbers_Method_Variable, Values=BB_Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Number", "Method"], Field_list=[BB_NUM_INV_FIX_Row, BB_AUT_Prefix_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Number_Widget.Add_row(Rows=[BB_INV_Number_Row, BB_NUM_INV_FIX_Row, Section_Row, BB_AUT_Prefix_Row])

    return BB_INV_Number_Widget

def BB_Items(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    BB_Items_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Method"]
    BB_Items_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Methods_List"])
    BB_Fixed_Items = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Fixed_Options"]["Fix_Item"]
    BB_Items_Method_Variable = StringVar(master=Frame, value=BB_Items_Method, name="BB_Items_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Items_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Vendor Service Functions", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Service Functions in Invoice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_Fixed_Items_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Items_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Service ID", Value=BB_Fixed_Items, placeholder_text="Manual Service ID.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Items", "Fixed_Options", "Fix_Item"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "All", "Prompt"], Freeze_fields=[[],[BB_Fixed_Items_Row],[BB_Fixed_Items_Row]])
    BB_Items_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Items_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Items", Variable=BB_Items_Method_Variable, Values=BB_Items_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Items", "Method"], Field_list=[BB_Fixed_Items_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Items_Widget.Add_row(Rows=[BB_Items_Method_Row, BB_Fixed_Items_Row])

    return BB_INV_Items_Widget

def BB_Quantity(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    BB_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Quantity"]["Method"]
    BB_Quantity_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Quantity"]["Methods_List"])

    BB_Quantity_Method_Variable = StringVar(master=Frame, value=BB_Quantity_Method, name="BB_Quantity_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Qty_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Quantity", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Quantity in Invoice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_Quantity_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Qty_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Items", Variable=BB_Quantity_Method_Variable, Values=BB_Quantity_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Quantity", "Method"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Qty_Widget.Add_row(Rows=[BB_Quantity_Method_Row])

    return BB_INV_Qty_Widget

def BB_Price_Currency(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Method"]
    BB_Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Methods_List"])
    BB_Fixed_Price = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Fixed_Options"]["Fix_Price"]
    BB_Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Currency"]["Fix_Currency"]
    BB_Price_Method_Variable = StringVar(master=Frame, value=BB_Price_Method, name="BB_Price_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Price_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Invoice.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_Fixed_Price_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Price", Value=BB_Fixed_Price, placeholder_text="Manual Price.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Prices", "Fixed_Options", "Fix_Price"], Validation="Float")
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Prompt"], Freeze_fields=[[],[BB_Fixed_Price_Row]])
    BB_Prices_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Price", Variable=BB_Price_Method_Variable, Values=BB_Price_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Prices", "Method"], Field_list=[BB_Fixed_Price_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 
    BB_Fixed_Currency_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Currency", Value=BB_Fixed_Currency, placeholder_text="Manual Currency.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Currency", "Fix_Currency"])
    
    # Add Fields to Widget Body
    BB_INV_Price_Widget.Add_row(Rows=[BB_Prices_Method_Row, BB_Fixed_Price_Row, BB_Fixed_Currency_Row])

    return BB_INV_Price_Widget

def BB_Posting_Date(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    BB_Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Method"]
    BB_Posting_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Methods_List"])
    BB_PD_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]
    BB_Posting_Date_Method_Variable = StringVar(master=Frame, value=BB_Posting_Date_Method, name="BB_Posting_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Date_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Invoice Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Vendor Invoice Date.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_PD_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=BB_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=BB_PD_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Invoice_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Today", "Prompt"], Freeze_fields=[[],[BB_PD_Fixed_Date_Row],[BB_PD_Fixed_Date_Row]])
    BB_Invoice_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Posting_Date_Method_Variable, Values=BB_Posting_Date_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Invoice_Date", "Method"], Field_list=[BB_PD_Fixed_Date_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Date_Widget.Add_row(Rows=[BB_Invoice_Date_Method_Row, BB_PD_Fixed_Date_Row])

    return BB_INV_Date_Widget

def BB_Order_reference(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    BB_Order_id_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Method"]
    BB_Order_id_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Methods_List"])
    BB_Fixed_Order_id = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Fixed_Options"]["Fixed_Order_ID"]
    BB_Order_date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Method"]
    BB_Order_date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Methods_List"])
    BB_OD_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Fixed_Options"]["Fixed_Order_Date"]
    BB_Order_id_Method_Variable = StringVar(master=Frame, value=BB_Order_id_Method, name="BB_Order_id_Method_Variable")
    BB_Order_date_Method_Variable = StringVar(master=Frame, value=BB_Order_date_Method, name="BB_Order_date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Reference_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Order Reference", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Order Reference like fictive Confirmation Id and Vendor creation date.", GUI_Level_ID=GUI_Level_ID)

    # Fields 
    Order_ID_Section_Row = Widget_Section_Row(Configuration=Configuration, master=BB_INV_Reference_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Order ID", Label_Size="Field_Label", Font_Size="Section_Separator")
    BB_Fixed_Order_id_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Reference_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Order id", Value=BB_Fixed_Order_id, placeholder_text="Manual Order Id.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_id", "Fixed_Options", "Fixed_Order_ID"])
    Order_ID_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Previous Month"], Freeze_fields=[[],[BB_Fixed_Order_id_Row]])
    BB_Order_id_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Reference_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Order_id_Method_Variable, Values=BB_Order_id_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_id", "Method"], Field_list=[BB_Fixed_Order_id_Row], Field_Blocking_dict=Order_ID_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Order_Date_Section_Row = Widget_Section_Row(Configuration=Configuration, master=BB_INV_Reference_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Order Date", Label_Size="Field_Label", Font_Size="Section_Separator")
    BB_OD_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=BB_INV_Reference_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=BB_OD_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_date", "Fixed_Options", "Fixed_Order_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
    Order_Date_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Invoice date"], Freeze_fields=[[],[BB_OD_Fixed_Date_Row]])
    BB_Order_date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Reference_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Order_date_Method_Variable, Values=BB_Order_date_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_date", "Method"], Field_list=[BB_OD_Fixed_Date_Row], Field_Blocking_dict=Order_Date_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Reference_Widget.Add_row(Rows=[Order_ID_Section_Row, BB_Order_id_Method_Row, BB_Fixed_Order_id_Row, Order_Date_Section_Row, BB_Order_date_Method_Row, BB_OD_Fixed_Date_Row])

    return BB_INV_Reference_Widget

def BB_Plant(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Method"]
    BB_Inv_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Methods_List"])
    BB_Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    BB_Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Fixed_Options"]["Plants_List"])
    BB_Inv_Plant_Method_Variable = StringVar(master=Frame, value=BB_Inv_Plant_Method, name="BB_Inv_Plant_Method_Variable")
    BB_Inv_Fixed_Plant_Variable = StringVar(master=Frame, value=BB_Inv_Fixed_Plant, name="BB_Inv_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Plant_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_Inv_Plant_Fixed_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Plant", Variable=BB_Inv_Fixed_Plant_Variable, Values=BB_Inv_Fixed_Plants_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Plants", "Fixed_Options", "Fixed_Plant"], GUI_Level_ID=GUI_Level_ID) 
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[BB_Inv_Plant_Fixed_Row],[BB_Inv_Plant_Fixed_Row],[BB_Inv_Plant_Fixed_Row]])
    BB_Inv_Plant_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Inv_Plant_Method_Variable, Values=BB_Inv_Plant_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Plants", "Method"], Field_list=[BB_Inv_Plant_Fixed_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Plant_Widget.Add_row(Rows=[BB_Inv_Plant_Method_Row, BB_Inv_Plant_Fixed_Row])

    return BB_INV_Plant_Widget

def BB_CountryOrigin(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Method"]
    BB_Count_Origin_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Methods_List"])
    BB_Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    BB_Count_Origin_Method_Variable = StringVar(master=Frame, value=BB_Count_Origin_Method, name="BB_Count_Origin_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Origin_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Country of Origin", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Country Codes in Invoice. \n Always takes 4 major codes + 5 random from Business Central.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_Fixed_Count_Origin_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Origin_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Country code", Value=BB_Fixed_Count_Origin, placeholder_text="Manual Country Code.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Country_Of_Origin", "Fixed_Options", "Fix_Country_Of_Origin"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[BB_Fixed_Count_Origin_Row],[BB_Fixed_Count_Origin_Row],[BB_Fixed_Count_Origin_Row]])
    BB_Count_Origin_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Origin_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Count_Origin_Method_Variable, Values=BB_Count_Origin_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Country_Of_Origin", "Method"], Field_list=[BB_Fixed_Count_Origin_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Origin_Widget.Add_row(Rows=[BB_Count_Origin_Method_Row, BB_Fixed_Count_Origin_Row])

    return BB_INV_Origin_Widget

def BB_Tariff(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Method"]
    BB_Tariff_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Methods_List"])
    BB_Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    BB_Tariff_Method_Variable = StringVar(master=Frame, value=BB_Tariff_Method, name="BB_Tariff_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BB_INV_Tariff_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Tariffs", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define tariffs numbers in Invoice. \n Always takes only random 10 tariffs from Business Central.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BB_Fixed_Tariff_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BB_INV_Tariff_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Tariff", Value=BB_Fixed_Tariff, placeholder_text="Manual Tariff Code.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Tariff", "Fixed_Options", "Fix_Tariff"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[BB_Fixed_Tariff_Row],[BB_Fixed_Tariff_Row],[BB_Fixed_Tariff_Row]])
    BB_Tariff_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BB_INV_Tariff_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=BB_Tariff_Method_Variable, Values=BB_Tariff_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Tariff", "Method"], Field_list=[BB_Fixed_Tariff_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    BB_INV_Tariff_Widget.Add_row(Rows=[BB_Tariff_Method_Row, BB_Fixed_Tariff_Row])

    return BB_INV_Tariff_Widget

# --------------------------------------------------------------------------- Purchase Return Order ---------------------------------------------------------------------------#
def PRO_INV_Number(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    PRO_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Method"]
    PRO_Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Methods_List"])
    PRO_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Automatic_Options"]["Prefix"]
    PRO_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Fixed_Options"]["Number"]

    PRO_Numbers_Method_Variable = StringVar(master=Frame, value=PRO_Numbers_Method, name="PRO_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PRO_INV_Number_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Credit Memo Number.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    PRO_NUM_INV_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=PRO_Fixed_Number, placeholder_text="Manual Number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Number", "Fixed_Options", "Number"])

    Section_Row = Widget_Section_Row(Configuration=Configuration, master=PRO_INV_Number_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    PRO_AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=PRO_Automatic_Prefix, placeholder_text="Prefix for unique number.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Number", "Automatic_Options", "Prefix"])

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Automatic", "Prompt"], Freeze_fields=[[PRO_AUT_Prefix_Row],[PRO_NUM_INV_FIX_Row],[PRO_NUM_INV_FIX_Row, PRO_AUT_Prefix_Row]])
    PRO_INV_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=PRO_Numbers_Method_Variable, Values=PRO_Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Number", "Method"], Field_list=[PRO_NUM_INV_FIX_Row, PRO_AUT_Prefix_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PRO_INV_Number_Widget.Add_row(Rows=[PRO_INV_Number_Row, PRO_NUM_INV_FIX_Row, Section_Row, PRO_AUT_Prefix_Row])

    return PRO_INV_Number_Widget

def PRO_Price_Currency(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    PRO_Currency_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Currency"]["Method"]
    PRO_Currency_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Currency"]["Methods_List"])
    PRO_Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    PRO_Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Prices"]["Method"]
    PRO_Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Prices"]["Methods_List"])
    PRO_Price_Method_Variable = StringVar(master=Frame, value=PRO_Price_Method, name="PRO_Price_Method_Variable")
    PRO_Currency_Method_Variable = StringVar(master=Frame, value=PRO_Currency_Method, name="PRO_Currency_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PRO_INV_Price_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Credit Memo.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    PRO_Prices_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Price", Variable=PRO_Price_Method_Variable, Values=PRO_Price_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Prices", "Method"], GUI_Level_ID=GUI_Level_ID) 
    PRO_Fixed_Currency_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Currency", Value=PRO_Fixed_Currency, placeholder_text="Manual Currency.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Currency", "Fixed_Options", "Fix_Currency"])
    PRO_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Purchase Return Order", "From Confirmation"], Freeze_fields=[[],[PRO_Fixed_Currency_Row],[PRO_Fixed_Currency_Row]])
    PRO_Currency_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Currency", Variable=PRO_Currency_Method_Variable, Values=PRO_Currency_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Currency", "Method"], Field_list=[PRO_Fixed_Currency_Row], Field_Blocking_dict=PRO_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PRO_INV_Price_Widget.Add_row(Rows=[PRO_Prices_Method_Row, PRO_Currency_Method_Row, PRO_Fixed_Currency_Row])

    return PRO_INV_Price_Widget

def PRO_Invoice_Date(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    PRO_Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Method"]
    PRO_Posting_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Methods_List"])
    PRO_INV_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]
    PRO_INV_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Random_Options"]["From"]
    PRO_INV_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Random_Options"]["To"]
    PRO_Posting_Date_Method_Variable = StringVar(master=Frame, value=PRO_Posting_Date_Method, name="PRO_Posting_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PRO_INV_Date_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Invoice Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Vendor Invoice Date.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    PRO_INV_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=PRO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=PRO_INV_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Invoice_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)

    Section_Row = Widget_Section_Row(Configuration=Configuration, master=PRO_INV_Date_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Random Date interval", Label_Size="Field_Label", Font_Size="Section_Separator")
    PRO_INV_Random_From_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - From CD +", Value=PRO_INV_Rand_From_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Invoice_Date", "Random_Options", "From"], Validation="Integer")
    PRO_INV_Random_To_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - To CD +", Value=PRO_INV_Rand_To_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Invoice_Date", "Random_Options", "To"], Validation="Integer")

    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Today", "Prompt"], Freeze_fields=[[PRO_INV_Random_From_Row, PRO_INV_Random_To_Row],[PRO_INV_Fixed_Date_Row],[PRO_INV_Fixed_Date_Row, PRO_INV_Random_From_Row, PRO_INV_Random_To_Row],[PRO_INV_Fixed_Date_Row, PRO_INV_Random_From_Row, PRO_INV_Random_To_Row]])
    PRO_Invoice_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=PRO_Posting_Date_Method_Variable, Values=PRO_Posting_Date_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Invoice_Date", "Method"], Field_list=[PRO_INV_Fixed_Date_Row, PRO_INV_Random_From_Row, PRO_INV_Random_To_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PRO_INV_Date_Widget.Add_row(Rows=[PRO_Invoice_Date_Method_Row, PRO_INV_Fixed_Date_Row, Section_Row, PRO_INV_Random_From_Row, PRO_INV_Random_To_Row])

    return PRO_INV_Date_Widget

def PRO_Plant(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    PRO_Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Method"]
    PRO_Inv_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Methods_List"])
    PRO_Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    PRO_Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Plants"]["Fixed_Options"]["Plants_List"])
    PRO_Inv_Plant_Method_Variable = StringVar(master=Frame, value=PRO_Inv_Plant_Method, name="PRO_Inv_Plant_Method_Variable")
    PRO_Inv_Fixed_Plant_Variable = StringVar(master=Frame, value=PRO_Inv_Fixed_Plant, name="PRO_Inv_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PRO_INV_Plant_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    PRO_INV_Plant_Fixed_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Plant", Variable=PRO_Inv_Fixed_Plant_Variable, Values=PRO_Inv_Fixed_Plants_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Plants", "Fixed_Options", "Fixed_Plant"], GUI_Level_ID=GUI_Level_ID) 
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[PRO_INV_Plant_Fixed_Row],[PRO_INV_Plant_Fixed_Row],[PRO_INV_Plant_Fixed_Row]])
    PRO_INV_Plant_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Plant_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=PRO_Inv_Plant_Method_Variable, Values=PRO_Inv_Plant_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Plants", "Method"], Field_list=[PRO_INV_Plant_Fixed_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PRO_INV_Plant_Widget.Add_row(Rows=[PRO_INV_Plant_Method_Row, PRO_INV_Plant_Fixed_Row])

    return PRO_INV_Plant_Widget

def PRO_CountryOrigin(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    PRO_Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Country_Of_Origin"]["Method"]
    PRO_Count_Origin_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Country_Of_Origin"]["Methods_List"])
    PRO_Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]
    PRO_Count_Origin_Method_Variable = StringVar(master=Frame, value=PRO_Count_Origin_Method, name="PRO_Count_Origin_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PRO_INV_Origin_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Country of Origin", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Country Codes in Credit Memo. \n Always takes 4 major codes + 5 random from Business Central.", GUI_Level_ID=GUI_Level_ID)

    # Fields 
    PRO_Fixed_Count_Origin_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Origin_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Country Code", Value=PRO_Fixed_Count_Origin, placeholder_text="Manual Country Code.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Country_Of_Origin", "Fixed_Options", "Fix_Country_Of_Origin"])
    Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[PRO_Fixed_Count_Origin_Row],[PRO_Fixed_Count_Origin_Row],[PRO_Fixed_Count_Origin_Row]])
    PRO_INV_Plant_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Origin_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=PRO_Count_Origin_Method_Variable, Values=PRO_Count_Origin_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Country_Of_Origin", "Method"], Field_list=[PRO_Fixed_Count_Origin_Row], Field_Blocking_dict=Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PRO_INV_Origin_Widget.Add_row(Rows=[PRO_INV_Plant_Method_Row, PRO_Fixed_Count_Origin_Row])

    return PRO_INV_Origin_Widget

def PRO_Tariff(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    PRO_Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Tariff"]["Method"]
    PRO_Tariff_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Tariff"]["Methods_List"])
    PRO_Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]
    PRO_Tariff_Method_Variable = StringVar(master=Frame, value=PRO_Tariff_Method, name="PRO_Tariff_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PRO_INV_Tariff_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Tariffs", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define tariffs numbers in Credit Memo. \n Always takes only random 10 tariffs from Business Central.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    PRO_Fixed_Tariff_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PRO_INV_Tariff_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Tariff code", Value=PRO_Fixed_Tariff, placeholder_text="Manual Tariff Code.", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Tariff", "Fixed_Options", "Fix_Tariff"])
    PRO_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Random", "Empty", "Prompt"], Freeze_fields=[[],[PRO_Fixed_Tariff_Row],[PRO_Fixed_Tariff_Row],[PRO_Fixed_Tariff_Row]])
    PRO_Tariff_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PRO_INV_Tariff_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=PRO_Tariff_Method_Variable, Values=PRO_Tariff_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Tariff", "Method"], Field_list=[PRO_Fixed_Tariff_Row], Field_Blocking_dict=PRO_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PRO_INV_Tariff_Widget.Add_row(Rows=[PRO_Tariff_Method_Row, PRO_Fixed_Tariff_Row])

    return PRO_INV_Tariff_Widget

def BHN_Exchange_Rates(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    BHN_Exchange_Use = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Use"]
    BHN_Exchange_Currency_From = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Currency"]["Currency_From"]
    BHN_Exchange_Currency_To = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Currency"]["Currency_To"]
    BHN_Exchange_Currency_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Currency"]["Currency_List"])
    
    BHN_Exchange_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Valid_Date"]["Method"]
    BHN_Exchange_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Valid_Date"]["Methods_List"])
    BHN_Exchange_Date_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Valid_Date"]["Fixed_Options"]["Fix_Date"]

    BHN_Exchange_Exchange_Rate = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Exchange_Rate"]

    BHN_Exchange_Use_Variable = BooleanVar(master=Frame, value=BHN_Exchange_Use, name="BHN_Exchange_Use_Variable")
    BHN_Exchange_Currency_From_Variable = StringVar(master=Frame, value=BHN_Exchange_Currency_From, name="BHN_Exchange_Currency_From_Variable")
    BHN_Exchange_Currency_To_Variable = StringVar(master=Frame, value=BHN_Exchange_Currency_To, name="BHN_Exchange_Currency_To_Variable")
    BHN_Exchange_Date_Method_Variable = StringVar(master=Frame, value=BHN_Exchange_Date_Method, name="BHN_Exchange_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    BHN_Exchange_Rates_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="BHN Exchange Rates", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="These settings if enabled will add 4 Remarks into Invoice related to Exchange Rate. This happen only when Delivery is done from Plant=1004.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    BHN_Exchange_Currency_From_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BHN_Exchange_Rates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Currency From", Variable=BHN_Exchange_Currency_From_Variable, Values=BHN_Exchange_Currency_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Local_Development", "BHN", "Exchange_Rate", "Currency", "Currency_From"], GUI_Level_ID=GUI_Level_ID) 
    BHN_Exchange_Currency_To_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BHN_Exchange_Rates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Currency To", Variable=BHN_Exchange_Currency_To_Variable, Values=BHN_Exchange_Currency_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Local_Development", "BHN", "Exchange_Rate", "Currency", "Currency_To"], GUI_Level_ID=GUI_Level_ID) 

    BHN_Exchange_Date_Fix_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=BHN_Exchange_Rates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=BHN_Exchange_Date_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Local_Development", "BHN", "Exchange_Rate", "Valid_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
    BHN_Exchange_Date_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Today", "Prompt"], Freeze_fields=[[],[BHN_Exchange_Date_Fix_Date_Row],[BHN_Exchange_Date_Fix_Date_Row]])
    BHN_Exchange_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=BHN_Exchange_Rates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Valid Date Method", Variable=BHN_Exchange_Date_Method_Variable, Values=BHN_Exchange_Date_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Local_Development", "BHN", "Exchange_Rate", "Valid_Date", "Method"], Field_list=[BHN_Exchange_Date_Fix_Date_Row], Field_Blocking_dict=BHN_Exchange_Date_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    BHN_Exchange_Exchange_Rate_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=BHN_Exchange_Rates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Exchange Rate", Value=BHN_Exchange_Exchange_Rate, placeholder_text="Exchange Rate", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Local_Development", "BHN", "Exchange_Rate", "Exchange_Rate"], Validation="Float")

    Use_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=[True, False], Freeze_fields=[[],[BHN_Exchange_Currency_From_Row, BHN_Exchange_Currency_To_Row, BHN_Exchange_Date_Fix_Date_Row, BHN_Exchange_Date_Method_Row, BHN_Exchange_Exchange_Rate_Row]])
    Use_BHN_Exchange_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=BHN_Exchange_Rates_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=BHN_Exchange_Use_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Local_Development", "BHN", "Exchange_Rate", "Use"], Field_list=[BHN_Exchange_Currency_From_Row, BHN_Exchange_Currency_To_Row, BHN_Exchange_Date_Fix_Date_Row, BHN_Exchange_Date_Method_Row, BHN_Exchange_Exchange_Rate_Row], Field_Blocking_dict=Use_Fields_Blocking_dict)


    # Add Fields to Widget Body
    BHN_Exchange_Rates_Widget.Add_row(Rows=[Use_BHN_Exchange_Row, BHN_Exchange_Currency_From_Row, BHN_Exchange_Currency_To_Row, BHN_Exchange_Date_Method_Row, BHN_Exchange_Date_Fix_Date_Row, BHN_Exchange_Exchange_Rate_Row])

    return BHN_Exchange_Rates_Widget