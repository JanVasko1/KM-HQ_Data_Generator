# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, CTkEntry, BooleanVar

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #--------------------------------------------------- Tabs--------------------------------------------------------------------------#
def DEL_Number(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Fixed_Options"]["Number"]

    DEL_Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="DEL_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Delivery Number.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    DEL_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    DEL_Number_Frame_Var = DEL_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    DEL_Number_Frame_Var.configure(variable=DEL_Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=DEL_Number_Frame_Var, values=Numbers_Method_List, command=lambda DEL_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=DEL_Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Number", "Method"], Information=DEL_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Date
    NUM_DEL_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_DEL_FIX_Frame_Var = NUM_DEL_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_DEL_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_DEL_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Number", "Fixed_Options", "Number"], Information=NUM_DEL_FIX_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=NUM_DEL_FIX_Frame_Var, Value=Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def DEL_Count(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    DEL_Count_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Method"]
    DEL_Count_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Methods_List"])
    Random_Max_count = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["Random_Max_count"]
    Fixed_Count = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Fixed_Options"]["Count"]

    DEL_Count_Method_Variable = StringVar(master=Frame, value=DEL_Count_Method, name="DEL_Count_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Delivery Count", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Definition how many Deliveries will be created.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Count Method
    DEL_Count_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    DEL_Count_Frame_Var = DEL_Count_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    DEL_Count_Frame_Var.configure(variable=DEL_Count_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=DEL_Count_Frame_Var, values=DEL_Count_Method_List, command=lambda DEL_Count_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=DEL_Count_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Counts", "Method"], Information=DEL_Count_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Random Maximal count
    DEL_Random_Max_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Maximal count", Field_Type="Input_Normal", Validation="Integer") 
    DEL_Random_Max_Frame_Var = DEL_Random_Max_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Random_Max_Frame_Var.configure(placeholder_text="Maximal delivery Count", placeholder_text_color="#949A9F")
    DEL_Random_Max_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Counts", "Random_Options", "Random_Max_count"], Information=int(DEL_Random_Max_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=DEL_Random_Max_Frame_Var, Value=Random_Max_count)

    # Field - Count Fix
    DEL_Count_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed count", Field_Type="Input_Normal", Validation="Integer") 
    DEL_Count_FIX_Frame_Var = DEL_Count_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Count_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    DEL_Count_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Counts", "Fixed_Options", "Count"], Information=int(DEL_Count_FIX_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=DEL_Count_FIX_Frame_Var, Value=Fixed_Count)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Item_Delivery_Assignment(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    DEL_Assignment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["Method"]
    DEL_Assignment_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["Methods_List"])
    DEL_FOCH_with_Main = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["FreeOfCharge_with_Main"]

    DEL_Assignment_Method_Variable = StringVar(master=Frame, value=DEL_Assignment_Method, name="DEL_Assignment_Method_Variable")
    DEL_FOCH_with_Main_Variable = BooleanVar(master=Frame, value=DEL_FOCH_with_Main, name="DEL_FOCH_with_Main_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Item Assignment to Delivery", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="How program will select Items and Qty to the Delivery.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Delivery Assignment Method
    DEL_Assignment_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    DEL_Assignment_Frame_Var = DEL_Assignment_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    DEL_Assignment_Frame_Var.configure(variable=DEL_Assignment_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=DEL_Assignment_Frame_Var, values=DEL_Assignment_Method_List, command=lambda DEL_Assignment_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=DEL_Assignment_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Item_Delivery_Assignment", "Method"], Information=DEL_Assignment_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Free of Charge with Machine
    DEL_FOCH_with_Main_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="FOCHs with Machine", Field_Type="Input_CheckBox") 
    DEL_FOCH_with_Main_Frame_Var = DEL_FOCH_with_Main_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    DEL_FOCH_with_Main_Frame_Var.configure(variable=DEL_FOCH_with_Main_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=DEL_FOCH_with_Main_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Item_Delivery_Assignment", "FreeOfCharge_with_Main"], Information=DEL_FOCH_with_Main_Variable))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Serial_Numbers(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    SN_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Prefix"]
    SN_Middle_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Method"]
    SN_Middle_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Methods_List"])
    SN_Middle_Manual = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Middle"]["Fixed"]
    SN_Suffix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Serial_Numbers"]["Suffix"]

    SN_Middle_Method_Variable = StringVar(master=Frame, value=SN_Middle_Method, name="Serial_Number_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Serial Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Serial Numbers creation options.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - SN Prefix
    SN_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    SN_Prefix_Frame_Var = SN_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    SN_Prefix_Frame_Var.configure(placeholder_text="Prefix", placeholder_text_color="#949A9F")
    SN_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Prefix"], Information=SN_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=SN_Prefix_Frame_Var, Value=SN_Prefix)

    # Field - SN Middle Method
    SN_Middle_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Middle Method", Field_Type="Input_OptionMenu") 
    SN_Middle_Method_Frame_Var = SN_Middle_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    SN_Middle_Method_Frame_Var.configure(variable=SN_Middle_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=SN_Middle_Method_Frame_Var, values=SN_Middle_Method_List, command=lambda SN_Middle_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=SN_Middle_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Middle", "Method"], Information=SN_Middle_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - SN Middle manual
    SN_Middle_Man_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Manual middle", Field_Type="Input_Normal") 
    SN_Middle_Man_Frame_Var = SN_Middle_Man_Frame.children["!ctkframe3"].children["!ctkentry"]
    SN_Middle_Man_Frame_Var.configure(placeholder_text="Manual Middle part", placeholder_text_color="#949A9F")
    SN_Middle_Man_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Serial_Numbers", "Middle", "Manual"], Information=SN_Middle_Man_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=SN_Middle_Man_Frame_Var, Value=SN_Middle_Manual)

    # Field - SN Suffix
    SN_Suffix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Suffix", Field_Type="Input_Normal") 
    SN_Suffix_Frame_Var = SN_Suffix_Frame.children["!ctkframe3"].children["!ctkentry"]
    Data_Functions.Entry_field_Insert(Field=SN_Suffix_Frame_Var, Value=SN_Suffix)
    SN_Suffix_Frame_Var.configure(state="disabled")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Delivery_Date(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Delivery_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Method"]
    Delivery_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Methods_List"])
    DEL_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Fixed_Options"]["Fix_Date"]

    DEL_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Random_Options"]["From"]
    DEL_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Random_Options"]["To"]

    Delivery_Dates_Method_Variable = StringVar(master=Frame, value=Delivery_Dates_Method, name="Delivery_Dates_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Delivery Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Delivery Date
    Delivery_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Delivery_Date_Method_Frame_Var = Delivery_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Delivery_Date_Method_Frame_Var.configure(variable=Delivery_Dates_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Delivery_Date_Method_Frame_Var, values=Delivery_Dates_Method_List, command=lambda Delivery_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Delivery_Dates_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Method"], Information=Delivery_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Date
    DEL_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Entry_DropDown", Validation="Date") 
    DEL_Fixed_Date_Frame_Var = DEL_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_DEL_Fixed_Date_Frame_Var = DEL_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    DEL_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    DEL_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Fixed_Options", "Fix_Date"], Information=DEL_Fixed_Date_Frame_Var.get()))
    Button_DEL_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=DEL_Fixed_Date_Frame_Var, Clicked_on_Button=Button_DEL_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Data_Functions.Entry_field_Insert(Field=DEL_Fixed_Date_Frame_Var, Value=DEL_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_DEL_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Field - Delivery Date - From CD + Entry Field
    DEL_Random_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    DEL_Random_From_Frame_Var = DEL_Random_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Random_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    DEL_Random_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Random_Options", "From"], Information=int(DEL_Random_From_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=DEL_Random_From_Frame_Var, Value=DEL_Rand_From_Date)

    # Field - Delivery Date - To CD + Entry Field
    DEL_Random_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    DEL_Random_To_Frame_Var = DEL_Random_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Random_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    DEL_Random_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Date", "Random_Options", "To"], Information=int(DEL_Random_To_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=DEL_Random_To_Frame_Var, Value=DEL_Rand_To_Date)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Carrier_ID(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Carrier_ID_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Method"]
    Carrier_ID_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Methods_List"])
    Carrier_ID_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Fixed_Options"]["Fix_Carrier"]

    Carrier_ID_Method_Variable = StringVar(master=Frame, value=Carrier_ID_Method, name="Carrier_ID_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Carrier", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Carrier ID
    Carrier_ID_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Carrier_ID_Method_Frame_Var = Carrier_ID_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Carrier_ID_Method_Frame_Var.configure(variable=Carrier_ID_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Carrier_ID_Method_Frame_Var, values=Carrier_ID_Method_List, command=lambda Carrier_ID_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Carrier_ID_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Carrier_ID", "Method"], Information=Carrier_ID_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - SN Prefix
    Carrier_ID_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Carrier", Field_Type="Input_Normal") 
    Carrier_ID_Fixed_Frame_Var = Carrier_ID_Fixed_Frame.children["!ctkframe3"].children["!ctkentry"]
    Carrier_ID_Fixed_Frame_Var.configure(placeholder_text="Prefix", placeholder_text_color="#949A9F")
    Carrier_ID_Fixed_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Carrier_ID", "Fixed_Options", "Fix_Carrier"], Information=Carrier_ID_Fixed_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Carrier_ID_Fixed_Frame_Var, Value=Carrier_ID_Fixed)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Shipment_Method(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Shipment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Method"]
    Shipment_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Methods_List"])
    Shipment_Method_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Fixed_Options"]["Fixed_Shipment_Method"]

    Shipment_Method_Variable = StringVar(master=Frame, value=Shipment_Method, name="Shipment_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Shipment Method", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Carrier ID
    Shipment_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Shipment_Method_Frame_Var = Shipment_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Shipment_Method_Frame_Var.configure(variable=Shipment_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Shipment_Method_Frame_Var, values=Shipment_Method_List, command=lambda Shipment_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Shipment_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Shipment_Method", "Method"], Information=Shipment_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - SN Prefix
    Ship_Method_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Shp. Method", Field_Type="Input_Normal") 
    Ship_Method_Fixed_Frame_Var = Ship_Method_Fixed_Frame.children["!ctkframe3"].children["!ctkentry"]
    Ship_Method_Fixed_Frame_Var.configure(placeholder_text="Fixed Shipment Method", placeholder_text_color="#949A9F")
    Ship_Method_Fixed_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Shipment_Method", "Fixed_Options", "Fixed_Shipment_Method"], Information=Ship_Method_Fixed_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Ship_Method_Fixed_Frame_Var, Value=Shipment_Method_Fixed)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Packages_Numbers(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Pack_Number_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Method"]
    Pack_Number_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Methods_List"])
    Pack_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Automatic_Options"]["Prefix"]
    Pack_Max_Records = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Automatic_Options"]["Max_Packages_Records"]

    Pack_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Number"]["Fixed_Options"]["Fixed_Package_No"]
    
    Pack_Number_Method_Variable = StringVar(master=Frame, value=Pack_Number_Method, name="Pack_Number_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Numbers creation logic.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    Pack_Number_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Pack_Number_Method_Frame_Var = Pack_Number_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Pack_Number_Method_Frame_Var.configure(variable=Pack_Number_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Pack_Number_Method_Frame_Var, values=Pack_Number_Method_List, command=lambda Pack_Number_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Pack_Number_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Method"], Information=Pack_Number_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Package Number
    DEL_Pack_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    DEL_Pack_FIX_Frame_Var = DEL_Pack_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Pack_FIX_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    DEL_Pack_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Fixed_Options", "Fixed_Package_No"], Information=DEL_Pack_FIX_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=DEL_Pack_FIX_Frame_Var, Value=Pack_Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Package Prefix
    DEL_Pack_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    DEL_Pack_Prefix_Frame_Var = DEL_Pack_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Pack_Prefix_Frame_Var.configure(placeholder_text="Prefix", placeholder_text_color="#949A9F")
    DEL_Pack_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Automatic_Options", "Prefix"], Information=DEL_Pack_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=DEL_Pack_Prefix_Frame_Var, Value=Pack_Prefix)

    # Field - Maximal Records per delivery
    DEL_Pack_MAX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Maximal Package Count", Field_Type="Input_Normal", Validation="Integer") 
    DEL_Pack_MAX_Frame_Var = DEL_Pack_MAX_Frame.children["!ctkframe3"].children["!ctkentry"]
    DEL_Pack_MAX_Frame_Var.configure(placeholder_text="Fill maximal Package count per Delivery", placeholder_text_color="#949A9F")
    DEL_Pack_MAX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Number", "Automatic_Options", "Max_Packages_Records"], Information=int(DEL_Pack_MAX_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=DEL_Pack_MAX_Frame_Var, Value=Pack_Max_Records)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Packages_Plants(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Pack_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Method"]
    Pack_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Methods_List"])
    Pack_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Pack_Fixed_Plant_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["Packages"]["Plants"]["Fixed_Options"]["Plant_List"])
    
    Pack_Plant_Method_Variable = StringVar(master=Frame, value=Pack_Plant_Method, name="Pack_Plant_Method_Variable")
    Pack_Fixed_Plant_Variable = StringVar(master=Frame, value=Pack_Fixed_Plant, name="Pack_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Plant Method
    Pack_Plant_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Pack_Plant_Method_Frame_Var = Pack_Plant_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Pack_Plant_Method_Frame_Var.configure(variable=Pack_Plant_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Pack_Plant_Method_Frame_Var, values=Pack_Plant_Method_List, command=lambda Pack_Plant_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Pack_Plant_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Plants", "Method"], Information=Pack_Plant_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Plant
    Pack_Plant_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Pack_Plant_Fixed_Frame_Var = Pack_Plant_Fixed_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Pack_Plant_Fixed_Frame_Var.configure(variable=Pack_Fixed_Plant_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Pack_Plant_Fixed_Frame_Var, values=Pack_Fixed_Plant_List, command=lambda Pack_Plant_Fixed_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Pack_Fixed_Plant_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Plants", "Fixed_Options", "Fixed_Plant"], Information=Pack_Plant_Fixed_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Packages_UOM(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
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
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Unit of Measure", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Packages unit of measure for measurements.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Weight", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Weight UoM Method
    Pack_Weight_UoM_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Pack_Weight_UoM_Method_Frame_Var = Pack_Weight_UoM_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Pack_Weight_UoM_Method_Frame_Var.configure(variable=Pack_Weight_UoM_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Pack_Weight_UoM_Method_Frame_Var, values=Pack_Weight_UoM_Method_List, command=lambda Pack_Weight_UoM_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Pack_Weight_UoM_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Weight", "Method"], Information=Pack_Weight_UoM_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Package Number
    Pack_Weight_UoM_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Weight UoM", Field_Type="Input_Normal") 
    Pack_Weight_UoM_Fixed_Frame_Var = Pack_Weight_UoM_Fixed_Frame.children["!ctkframe3"].children["!ctkentry"]
    Pack_Weight_UoM_Fixed_Frame_Var.configure(placeholder_text="Fixed weight UoM", placeholder_text_color="#949A9F")
    Pack_Weight_UoM_Fixed_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Weight", "Fixed_Options", "Fixed_Weight_UoM"], Information=Pack_Weight_UoM_Fixed_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Pack_Weight_UoM_Fixed_Frame_Var, Value=Pack_Weight_UoM_Fixed)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Volume", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Volume UoM Method
    Pack_Volume_UoM_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Pack_Volume_UoM_Method_Frame_Var = Pack_Volume_UoM_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Pack_Volume_UoM_Method_Frame_Var.configure(variable=Pack_Volume_UoM_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Pack_Volume_UoM_Method_Frame_Var, values=Pack_Volume_UoM_Method_List, command=lambda Pack_Volume_UoM_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Pack_Volume_UoM_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Volume", "Method"], Information=Pack_Volume_UoM_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Package Number
    Pack_Volume_UoM_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Volume UoM", Field_Type="Input_Normal") 
    Pack_Volume_UoM_Fixed_Frame_Var = Pack_Volume_UoM_Fixed_Frame.children["!ctkframe3"].children["!ctkentry"]
    Pack_Volume_UoM_Fixed_Frame_Var.configure(placeholder_text="Fixed Volume UoM", placeholder_text_color="#949A9F")
    Pack_Volume_UoM_Fixed_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "Packages", "Unit_Of_Measure", "Volume", "Fixed_Options", "Fixed_Volume_UoM"], Information=Pack_Volume_UoM_Fixed_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Pack_Volume_UoM_Fixed_Frame_Var, Value=Pack_Volume_UoM_Fixed)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def EXIDV2(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
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
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="EXIDV2", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="EXIDV2 Number logic assignment.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    EXIDV2_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    EXIDV2_Number_Frame_Var = EXIDV2_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    EXIDV2_Number_Frame_Var.configure(variable=EXIDV2_Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=EXIDV2_Number_Frame_Var, values=EXIDV2_Numbers_Method_List, command=lambda EXIDV2_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=EXIDV2_Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Number", "Method"], Information=EXIDV2_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Number
    NUM_EXIDV2_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_EXIDV2_FIX_Frame_Var = NUM_EXIDV2_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_EXIDV2_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_EXIDV2_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Number", "Fixed_Options", "Fixed_EXIDV2"], Information=NUM_EXIDV2_FIX_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=NUM_EXIDV2_FIX_Frame_Var, Value=EXIDV2_Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=EXIDV2_Automatic_Prefix)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Package Assign Method", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Assignment
    EXIDV2_Assign_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Assign method", Field_Type="Input_OptionMenu") 
    EXIDV2_Assign_Frame_Var = EXIDV2_Assign_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    EXIDV2_Assign_Frame_Var.configure(variable=EXIDV2_Assign_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=EXIDV2_Assign_Frame_Var, values=EXIDV2_Assign_Method_List, command=lambda EXIDV2_Assign_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=EXIDV2_Assign_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "EXIDV2", "Method"], Information=EXIDV2_Assign_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BillOfLanding(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BOL_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Method"]
    BOL_Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Methods_List"])
    BOL_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Automatic_Options"]["Prefix"]
    BOL_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Fixed_Options"]["Fixed_BOL"]

    BOL_Numbers_Method_Variable = StringVar(master=Frame, value=BOL_Numbers_Method, name="BOL_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Bill of Landing", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Bill of Landing number logic assignment.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    BOL_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BOL_Number_Frame_Var = BOL_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BOL_Number_Frame_Var.configure(variable=BOL_Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BOL_Number_Frame_Var, values=BOL_Numbers_Method_List, command=lambda BOL_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BOL_Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "BillOfLanding", "Number", "Method"], Information=BOL_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Number
    NUM_BOL_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_BOL_FIX_Frame_Var = NUM_BOL_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_BOL_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_BOL_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "BillOfLanding", "Number", "Fixed_Options", "Fixed_BOL"], Information=NUM_BOL_FIX_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=NUM_BOL_FIX_Frame_Var, Value=BOL_Fixed_Number)

    # Section
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Delivery_Tracking_Information", "BillOfLanding", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=BOL_Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main