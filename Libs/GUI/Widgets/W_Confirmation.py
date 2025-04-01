# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, BooleanVar

import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_CheckBox, WidgetRow_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Date_Picker

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #--------------------------------------------------- Tabs--------------------------------------------------------------------------#
def PO_CON_Number(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]
    Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Number_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Confirmation Number.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    NUM_CON_FIX_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Number", Value=Fixed_Number, placeholder_text="Manual Number", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Fixed_Options", "Number"])
    Section_Row = Widget_Section_Row(Configuration=Configuration, master=Con_Number_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Automatic Setup", Label_Size="Field_Label", Font_Size="Section_Separator")
    AUT_Prefix_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Prefix", Value=Automatic_Prefix, placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Automatic_Options", "Prefix"])
    Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["Fixed", "Automatic", "Prompt"], Freeze_fields=[[AUT_Prefix_Row],[NUM_CON_FIX_Row],[AUT_Prefix_Row,NUM_CON_FIX_Row]])
    CON_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_Number_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Numbers_Method_Variable, Values=Numbers_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Method"], Field_list=[NUM_CON_FIX_Row, AUT_Prefix_Row], Field_Blocking_dict=Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Con_Number_Widget.Add_row(Rows=[CON_Number_Row, NUM_CON_FIX_Row, Section_Row, AUT_Prefix_Row])

    return Con_Number_Widget

def PO_Generation_Date(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Generation_Date_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Method"]
    Generation_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Methods_List"])
    Gen_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Fixed_Options"]["Fix_Date"]
    Generation_Date_Method_Variable = StringVar(master=Frame, value=Generation_Date_Method, name="Generation_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Gen_Date_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Generation Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Date of generation Confirmation.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Gen_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Con_Gen_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=Gen_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Generation_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
    Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["Fixed", "Today", "Prompt"], Freeze_fields=[[],[Gen_Fixed_Date_Row],[Gen_Fixed_Date_Row]])
    CON_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_Gen_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Generation_Date_Method_Variable, Values=Generation_Date_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Generation_Date", "Method"], Field_list=[Gen_Fixed_Date_Row], Field_Blocking_dict=Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Con_Gen_Date_Widget.Add_row(Rows=[CON_Date_Method_Row, Gen_Fixed_Date_Row])

    return Con_Gen_Date_Widget

def PO_Unit_of_Measure(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    UoM_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Method"]
    UoM_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Methods_List"])
    Fixed_UoM = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Fixed_Options"]["Fix_UoM"]
    UoM_Method_Variable = StringVar(master=Frame, value=UoM_Method, name="UoM_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_UoM_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Unit of Measure", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Unit of Measure in Confirmation.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Fixed_UoM_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_UoM_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Unit of Measure", Value=Fixed_UoM, placeholder_text="Manual Unit of Measure", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Unit_of_Measure", "Fixed_Options", "Fix_UoM"])
    Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["Fixed", "Purchase Line", "HQ Item Transport Export", "Prompt"], Freeze_fields=[[],[Fixed_UoM_Row],[Fixed_UoM_Row],[Fixed_UoM_Row]])
    UoM_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_UoM_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Unit of Measure", Variable=UoM_Method_Variable, Values=UoM_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Unit_of_Measure", "Method"], Field_list=[Fixed_UoM_Row], Field_Blocking_dict=Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Con_UoM_Widget.Add_row(Rows=[UoM_Method_Row, Fixed_UoM_Row])

    return Con_UoM_Widget

def PO_Price_Currency(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Method"]
    Currency_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Methods_List"])
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    Price_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Prices"]["Method"]
    Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Prices"]["Methods_List"])
    Price_Method_Variable = StringVar(master=Frame, value=Price_Method, name="Price_Method_Variable")
    Currency_Method_Variable = StringVar(master=Frame, value=Currency_Method, name="Currency_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Price_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Confirmation.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Fixed_Currency_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Currency", Value=Fixed_Currency, placeholder_text="Manual Currency", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Currency", "Fixed_Options", "Fix_Currency"])
    Prices_Method_Frame = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Price", Variable=Price_Method_Variable, Values=Price_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Prices", "Method"], GUI_Level_ID=GUI_Level_ID) 
    Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["Fixed", "Purchase Order"], Freeze_fields=[[],[Fixed_Currency_Row]])
    Currency_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_Price_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Currency", Variable=Currency_Method_Variable, Values=Currency_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Currency", "Method"], Field_list=[Fixed_Currency_Row], Field_Blocking_dict=Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Con_Price_Widget.Add_row(Rows=[Prices_Method_Frame, Currency_Method_Row, Fixed_Currency_Row])

    return Con_Price_Widget

def PO_Line_Flags(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Line_Flags_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Use"]
    Line_Flag_Label_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Labels_always"]
    Line_Flag_Item_EOL_Finished = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Item_EOL_Finish"]
    Line_Flag_Always_Substitute = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Always_Substitute"]
    Line_Flags_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Method"]
    Line_Flags_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Methods_List"])
    Line_Flags_Enabled_Variable = BooleanVar(master=Frame, value=Line_Flags_Enabled, name="Line_Flags_Enabled_Variable")
    Line_Flag_Label_Enabled_Variable = BooleanVar(master=Frame, value=Line_Flag_Label_Enabled, name="Line_Flag_Label_Enabled_Variable")
    Line_Flag_Item_EOL_Finished_Variable = BooleanVar(master=Frame, value=Line_Flag_Item_EOL_Finished, name="Line_Flag_Item_EOL_Finished_Variable")
    Line_Flag_Always_Substitute_Variable = BooleanVar(master=Frame, value=Line_Flag_Always_Substitute, name="Line_Flag_Always_Substitute_Variable")
    Line_Flags_Method_Variable = StringVar(master=Frame, value=Line_Flags_Method, name="Line_Flags_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Line_Flags_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Line Flags", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will treat Line Flags.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Line_Flags_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Con_Line_Flags_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=Line_Flags_Enabled_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Use"])
    Line_Flags_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_Line_Flags_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Line_Flags_Method_Variable, Values=Line_Flags_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Method"], GUI_Level_ID=GUI_Level_ID) 
    Section_Row = Widget_Section_Row(Configuration=Configuration, master=Con_Line_Flags_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Global Flags", Label_Size="Field_Label", Font_Size="Section_Separator")
    Use_Line_Flag_Label_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Con_Line_Flags_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Label always", Variable=Line_Flag_Label_Enabled_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Labels_always"])
    Finished_EOL_Item_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Con_Line_Flags_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Finish EOL Item", Variable=Line_Flag_Item_EOL_Finished_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Item_EOL_Finish"])
    Always_Substitute_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Con_Line_Flags_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Always Substitute", Variable=Line_Flag_Always_Substitute_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Always_Substitute"])

    # Add Fields to Widget Body
    Con_Line_Flags_Widget.Add_row(Rows=[Use_Line_Flags_Row, Line_Flags_Method_Row, Section_Row, Use_Line_Flag_Label_Row, Finished_EOL_Item_Row, Always_Substitute_Row])

    return Con_Line_Flags_Widget

def PO_ATP_General(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Use"]
    ATP_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Method"]
    ATP_Quantity_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Methods_List"])

    ATP_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Method"]
    ATP_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Methods_List"])

    ATP_Enabled_Variable = BooleanVar(master=Frame, value=ATP_Enabled, name="ATP_Enabled_Variable")
    ATP_Quantity_Method_Variable = StringVar(master=Frame, value=ATP_Quantity_Method, name="ATP_Quantity_Method_Variable")
    ATP_Dates_Method_Variable = StringVar(master=Frame, value=ATP_Dates_Method, name="ATP_Dates_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_ATP_Gen_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="ATP", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will work on ATP for each line.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Use_Line_Flags_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Con_ATP_Gen_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Use", Variable=ATP_Enabled_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Use"])
    ATP_QTY_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_ATP_Gen_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Quantity Method", Variable=ATP_Quantity_Method_Variable, Values=ATP_Quantity_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Method"], GUI_Level_ID=GUI_Level_ID) 
    ATP_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_ATP_Gen_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Date Method", Variable=ATP_Dates_Method_Variable, Values=ATP_Dates_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Method"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Con_ATP_Gen_Widget.Add_row(Rows=[Use_Line_Flags_Row, ATP_QTY_Method_Row, ATP_Date_Method_Row])

    return Con_ATP_Gen_Widget

def PO_ATP_Quantity_Distribution(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    ONH_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["ONH"]
    ONB_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["ONB"]
    BACK_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["BACK"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_ATP_Qty_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Quantity distribution", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to Ratio between each state.\nGood to distribute values as percentage up to 100.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    ONH_Ratio_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Qty_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="ONH Ratio", Value=ONH_Ratio, placeholder_text="OnHand Ratio", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Ratio", "ONH"], Validation="Integer")
    ONB_Ratio_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Qty_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="ONB Ratio", Value=ONB_Ratio, placeholder_text="OnBoard Ratio", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Ratio", "ONB"], Validation="Integer")
    BACK_Ratio_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Qty_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="BACK Ratio", Value=BACK_Ratio, placeholder_text="BackOrder Ratio", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Ratio", "BACK"], Validation="Integer")

    # Add Fields to Widget Body
    Con_ATP_Qty_Widget.Add_row(Rows=[ONH_Ratio_Row, ONB_Ratio_Row, BACK_Ratio_Row])

    return Con_ATP_Qty_Widget


def PO_ATP_Fixed_Dates(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_ONH_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Fixed_Dates"]["ONH"]
    ATP_ONB_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Fixed_Dates"]["ONB"]
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_ATP_Date_Fix_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Fixed Dates", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will delivery Fixed Dates.", GUI_Level_ID=GUI_Level_ID)

    # Fields 
    Man_ONH_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Con_ATP_Date_Fix_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="ONH Date", Date_format=Date_Format, Value=ATP_ONH_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Fixed_Dates", "ONH"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
    Man_ONB_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=Con_ATP_Date_Fix_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="ONB Date", Date_format=Date_Format, Value=ATP_ONB_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Fixed_Dates", "ONB"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)

    # Add Fields to Widget Body
    Con_ATP_Date_Fix_Widget.Add_row(Rows=[Man_ONH_Date_Row, Man_ONB_Date_Row])

    return Con_ATP_Date_Fix_Widget

def PO_ATP_Interval_Dates(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_Interval_ONH_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["From"]
    ATP_Interval_ONH_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["To"]
    ATP_Interval_ONB_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["From"]
    ATP_Interval_ONB_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["To"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_ATP_Date_Interval_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Interval Dates", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will delivery Interval Dates.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    ATP_Interval_ONH_From_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Date_Interval_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="ONH - From CD +", Value=ATP_Interval_ONH_From, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONH", "From"], Validation="Integer")
    ATP_Interval_ONH_To_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Date_Interval_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="ONH - To CD +", Value=ATP_Interval_ONH_To, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONH", "To"], Validation="Integer")
    ATP_Interval_ONB_From_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Date_Interval_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="ONB - From CD +", Value=ATP_Interval_ONB_From, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONB", "From"], Validation="Integer")
    ATP_Interval_ONB_To_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_ATP_Date_Interval_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="ONB - To CD +", Value=ATP_Interval_ONB_To, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONB", "To"], Validation="Integer")

    # Add Fields to Widget Body
    Con_ATP_Date_Interval_Widget.Add_row(Rows=[ATP_Interval_ONH_From_Row, ATP_Interval_ONH_To_Row, ATP_Interval_ONB_From_Row, ATP_Interval_ONB_To_Row])

    return Con_ATP_Date_Interval_Widget

def PO_Items_Free_Method(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Free_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Method"]
    Free_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Methods_List"])
    Free_Method_Variable = StringVar(master=Frame, value=Free_Method, name="Free_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Free_Method_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Free of Charge", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will treat Free of Charge Items for Confirmation.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    ATP_Date_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Con_Free_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=Free_Method_Variable, Values=Free_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Method"], GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Con_Free_Method_Widget.Add_row(Rows=[ATP_Date_Method_Row])

    return Con_Free_Method_Widget

def PO_Items_Free_Cable(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Cable_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Number"]
    Cable_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Description"]
    Cable_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["QTY_per_Machine"]
    Cable_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Price"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Free_Cable_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Cable", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Fixed cable item settings.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Cable_Number_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Cable_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Number", Value=Cable_Number, placeholder_text="Cable number", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "Number"])
    Cable_Description_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Cable_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Description", Value=Cable_Description, placeholder_text="Cable Description", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "Description"])
    Cable_QTY_per_Machine_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Cable_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="QTY per Machine", Value=Cable_QTY_per_Machine, placeholder_text="Cable QTY per Machine", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "QTY_per_Machine"], Validation="Integer")
    Cable_Price_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Cable_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Price", Value=Cable_Price, placeholder_text="Cable Price", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "Price"], Validation="Float")

    # Add Fields to Widget Body
    Con_Free_Cable_Widget.Add_row(Rows=[Cable_Number_Row, Cable_Description_Row, Cable_QTY_per_Machine_Row, Cable_Price_Row])

    return Con_Free_Cable_Widget

def PO_Items_Free_Documentation(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Documentation_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Number"]
    Documentation_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Description"]
    Documentation_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["QTY_per_Machine"]
    Documentation_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Price"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Free_Document_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Documentation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Fixed documentation item settings.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Documentation_Number_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Document_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Number", Value=Documentation_Number, placeholder_text="Documentation number", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "Number"])
    Documentation_Description_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Document_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Description", Value=Documentation_Description, placeholder_text="Documentation Description", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "Description"])
    Documentation_QTY_per_Machine_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Document_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="QTY per Machine", Value=Documentation_QTY_per_Machine, placeholder_text="Documentation QTY per Machine", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "QTY_per_Machine"], Validation="Integer")
    Documentation_Price_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Document_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Price", Value=Documentation_Price, placeholder_text="Documentation Price", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "Price"], Validation="Float")

    # Add Fields to Widget Body
    Con_Free_Document_Widget.Add_row(Rows=[Documentation_Number_Row, Documentation_Description_Row, Documentation_QTY_per_Machine_Row, Documentation_Price_Row])
  
    return Con_Free_Document_Widget


def PO_Items_Free_Face_Sheet(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Face_Sheet_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Number"]
    Face_Sheet_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Description"]
    Face_Sheet_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["QTY_per_Machine"]
    Face_Sheet_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Price"]

    # ------------------------- Main Functions -------------------------#
    # Widget
    Con_Free_Face_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Face Sheet", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Fixed Face Sheets item settings.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Face_Sheet_Number_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Face_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Number", Value=Face_Sheet_Number, placeholder_text="Face Sheet number", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "Number"])
    Face_Sheet_Description_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Face_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Description", Value=Face_Sheet_Description, placeholder_text="Face Sheet Description", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "Description"])
    Face_Sheet_QTY_per_Machine_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Face_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="QTY per Machine", Value=Face_Sheet_QTY_per_Machine, placeholder_text="Face Sheet QTY per Machine", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "QTY_per_Machine"], Validation="Integer")
    Face_Sheet_Price_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Con_Free_Face_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Price", Value=Face_Sheet_Price, placeholder_text="Face Sheet Price", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "Price"], Validation="Float")

    # Add Fields to Widget Body
    Con_Free_Face_Widget.Add_row(Rows=[Face_Sheet_Number_Row, Face_Sheet_Description_Row, Face_Sheet_QTY_per_Machine_Row, Face_Sheet_Price_Row])

    return Con_Free_Face_Widget
