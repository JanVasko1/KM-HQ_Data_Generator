# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, CTkEntry

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #--------------------------------------------------- Tabs--------------------------------------------------------------------------#
def PO_INV_Number(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]

    Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Invoice Number.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    INV_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    INV_Number_Frame_Var = INV_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    INV_Number_Frame_Var.configure(variable=Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=INV_Number_Frame_Var, values=Numbers_Method_List, command=lambda INV_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Method"], Information=INV_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Automatic Prefix
    NUM_INV_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_INV_FIX_Frame_Var = NUM_INV_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_INV_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_INV_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Fixed_Options", "Number"], Information=NUM_INV_FIX_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=NUM_INV_FIX_Frame_Var, Value=Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Price_Currency(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Method"]
    Currency_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Methods_List"])
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Method"]
    Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Methods_List"])

    Price_Method_Variable = StringVar(master=Frame, value=Price_Method, name="Price_Method_Variable")
    Currency_Method_Variable = StringVar(master=Frame, value=Currency_Method, name="Currency_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Price Method
    Prices_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_OptionMenu") 
    Prices_Method_Frame_Var = Prices_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Prices_Method_Frame_Var.configure(variable=Price_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Prices_Method_Frame_Var, values=Price_Method_List, command=lambda Prices_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Price_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Prices", "Method"], Information=Prices_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Number Method
    Currency_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Currency", Field_Type="Input_OptionMenu") 
    Currency_Method_Frame_Var = Currency_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Currency_Method_Frame_Var.configure(variable=Currency_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Currency_Method_Frame_Var, values=Currency_Method_List, command=lambda Currency_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Currency_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Currency", "Method"], Information=Currency_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Currency
    Fixed_Currency_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Currency", Field_Type="Input_Normal") 
    Fixed_Currency_Frame_Var = Fixed_Currency_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Currency_Frame_Var.configure(placeholder_text="Manual Currency", placeholder_text_color="#949A9F")
    Fixed_Currency_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Currency", "Fixed_Options", "Fix_Currency"], Information=Fixed_Currency_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Fixed_Currency_Frame_Var, Value=Fixed_Currency)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Posting_Date(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Method"]
    Posting_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Methods_List"])
    INV_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]

    INV_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Random_Options"]["From"]
    INV_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Random_Options"]["To"]

    Posting_Date_Method_Variable = StringVar(master=Frame, value=Posting_Date_Method, name="Posting_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Invoice Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Vendor Invoice Date.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Invoice Date
    Invoice_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Invoice_Date_Method_Frame_Var = Invoice_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Invoice_Date_Method_Frame_Var.configure(variable=Posting_Date_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Invoice_Date_Method_Frame_Var, values=Posting_Date_Method_List, command=lambda Invoice_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Posting_Date_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Method"], Information=Invoice_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Date
    INV_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Date_Picker", Validation="Date") 
    INV_Fixed_Date_Frame_Var = INV_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_INV_Fixed_Date_Frame_Var = INV_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    INV_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    INV_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Fixed_Options", "Fix_Date"], Information=INV_Fixed_Date_Frame_Var.get()))
    Button_INV_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=INV_Fixed_Date_Frame_Var, Clicked_on_Button=Button_INV_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Data_Functions.Entry_field_Insert(Field=INV_Fixed_Date_Frame_Var, Value=INV_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_INV_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automation", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Invoice Date - From CD + Entry Field
    INV_Random_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    INV_Random_From_Frame_Var = INV_Random_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    INV_Random_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    INV_Random_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Random_Options", "From"], Information=int(INV_Random_From_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=INV_Random_From_Frame_Var, Value=INV_Rand_From_Date)

    # Field - Invoice Date - To CD + Entry Field
    INV_Random_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    INV_Random_To_Frame_Var = INV_Random_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    INV_Random_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    INV_Random_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Invoice_Date", "Random_Options", "To"], Information=int(INV_Random_To_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=INV_Random_To_Frame_Var, Value=INV_Rand_To_Date)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def PO_Plant(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Method"]
    Inv_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Methods_List"])
    Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Plants_List"])
    
    Inv_Plant_Method_Variable = StringVar(master=Frame, value=Inv_Plant_Method, name="Inv_Plant_Method_Variable")
    Inv_Fixed_Plant_Variable = StringVar(master=Frame, value=Inv_Fixed_Plant, name="Inv_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Plant Method
    Inv_Plant_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Inv_Plant_Method_Frame_Var = Inv_Plant_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Inv_Plant_Method_Frame_Var.configure(variable=Inv_Plant_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Inv_Plant_Method_Frame_Var, values=Inv_Plant_Method_List, command=lambda Inv_Plant_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Inv_Plant_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Plants", "Method"], Information=Inv_Plant_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Plant
    Inv_Plant_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Plant", Field_Type="Input_OptionMenu") 
    Inv_Plant_Fixed_Frame_Var = Inv_Plant_Fixed_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Inv_Plant_Fixed_Frame_Var.configure(variable=Inv_Fixed_Plant_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Inv_Plant_Fixed_Frame_Var, values=Inv_Fixed_Plants_List, command=lambda Inv_Plant_Fixed_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Inv_Fixed_Plant_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Plants", "Fixed_Options", "Fixed_Plant"], Information=Inv_Plant_Fixed_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_CountryOrigin(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Method"]
    Count_Origin_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Methods_List"])
    Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    Count_Origin_Method_Variable = StringVar(master=Frame, value=Count_Origin_Method, name="Count_Origin_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Country of Origin", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Country Codes in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    Count_Origin_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Count_Origin_Method_Frame_Var = Count_Origin_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Count_Origin_Method_Frame_Var.configure(variable=Count_Origin_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Count_Origin_Method_Frame_Var, values=Count_Origin_Method_List, command=lambda Count_Origin_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Count_Origin_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Country_Of_Origin", "Method"], Information=Count_Origin_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Count_Origin
    Fixed_Count_Origin_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Country code", Field_Type="Input_Normal") 
    Fixed_Count_Origin_Frame_Var = Fixed_Count_Origin_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Count_Origin_Frame_Var.configure(placeholder_text="Manual Country Code", placeholder_text_color="#949A9F")
    Fixed_Count_Origin_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Country_Of_Origin", "Fixed_Options", "Fix_Country_Of_Origin"], Information=Fixed_Count_Origin_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Fixed_Count_Origin_Frame_Var, Value=Fixed_Count_Origin)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Tariff(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Method"]
    Tariff_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Methods_List"])
    Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    Tariff_Method_Variable = StringVar(master=Frame, value=Tariff_Method, name="Tariff_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Tariffs", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define tariffs numbers in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    Tariff_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Tariff_Method_Frame_Var = Tariff_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Tariff_Method_Frame_Var.configure(variable=Tariff_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Tariff_Method_Frame_Var, values=Tariff_Method_List, command=lambda Tariff_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Tariff_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Tariff", "Method"], Information=Tariff_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Tariff
    Fixed_Tariff_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Tariff code", Field_Type="Input_Normal") 
    Fixed_Tariff_Frame_Var = Fixed_Tariff_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Tariff_Frame_Var.configure(placeholder_text="Manual Tariff Code", placeholder_text_color="#949A9F")
    Fixed_Tariff_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Tariff", "Fixed_Options", "Fix_Tariff"], Information=Fixed_Tariff_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Fixed_Tariff_Frame_Var, Value=Fixed_Tariff)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_INV_Number(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Method"]
    BB_Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Methods_List"])
    BB_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Automatic_Options"]["Prefix"]
    BB_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Fixed_Options"]["Number"]

    BB_Numbers_Method_Variable = StringVar(master=Frame, value=BB_Numbers_Method, name="BB_Numbers_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Invoice Number.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    BB_INV_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_INV_Number_Frame_Var = BB_INV_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_INV_Number_Frame_Var.configure(variable=BB_Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_INV_Number_Frame_Var, values=BB_Numbers_Method_List, command=lambda BB_INV_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Number", "Method"], Information=BB_INV_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Automatic Prefix
    BB_NUM_INV_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    BB_NUM_INV_FIX_Frame_Var = BB_NUM_INV_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_NUM_INV_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    BB_NUM_INV_FIX_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Number", "Fixed_Options", "Number"], Information=BB_NUM_INV_FIX_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_NUM_INV_FIX_Frame_Var, Value=BB_Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Automatic Prefix
    BB_AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    BB_AUT_Prefix_Frame_Var = BB_AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    BB_AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Number", "Automatic_Options", "Prefix"], Information=BB_AUT_Prefix_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_AUT_Prefix_Frame_Var, Value=BB_Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def BB_Items(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    BB_Items_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Method"]
    BB_Items_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Methods_List"])
    BB_Fixed_Items = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Fixed_Options"]["Fix_Item"]

    BB_Items_Method_Variable = StringVar(master=Frame, value=BB_Items_Method, name="BB_Items_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Vendor Service Functions", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Service Functions in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Items Method
    BB_Items_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Items", Field_Type="Input_OptionMenu") 
    BB_Items_Method_Frame_Var = BB_Items_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Items_Method_Frame_Var.configure(variable=BB_Items_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Items_Method_Frame_Var, values=BB_Items_Method_List, command=lambda BB_Items_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Items_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Items", "Method"], Information=BB_Items_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Items
    BB_Fixed_Items_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Service ID", Field_Type="Input_Normal") 
    BB_Fixed_Items_Frame_Var = BB_Fixed_Items_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Fixed_Items_Frame_Var.configure(placeholder_text="Manual Service ID", placeholder_text_color="#949A9F")
    BB_Fixed_Items_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Items", "Fixed_Options", "Fix_Item"], Information=BB_Fixed_Items_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_Fixed_Items_Frame_Var, Value=BB_Fixed_Items)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_Quantity(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    BB_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Quantity"]["Method"]
    BB_Quantity_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Quantity"]["Methods_List"])

    BB_Quantity_Method_Variable = StringVar(master=Frame, value=BB_Quantity_Method, name="BB_Quantity_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Quantity", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Quantity in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Quantity Method
    BB_Quantity_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Quantity", Field_Type="Input_OptionMenu") 
    BB_Quantity_Method_Frame_Var = BB_Quantity_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Quantity_Method_Frame_Var.configure(variable=BB_Quantity_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Quantity_Method_Frame_Var, values=BB_Quantity_Method_List, command=lambda BB_Quantity_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Quantity_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Quantity", "Method"], Information=BB_Quantity_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_Price_Currency(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Method"]
    BB_Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Methods_List"])
    BB_Fixed_Price = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Fixed_Options"]["Fix_Price"]

    BB_Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Currency"]["Fix_Currency"]
    
    BB_Price_Method_Variable = StringVar(master=Frame, value=BB_Price_Method, name="BB_Price_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Price Method
    BB_Prices_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_OptionMenu") 
    BB_Prices_Method_Frame_Var = BB_Prices_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Prices_Method_Frame_Var.configure(variable=BB_Price_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Prices_Method_Frame_Var, values=BB_Price_Method_List, command=lambda BB_Prices_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Price_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Prices", "Method"], Information=BB_Prices_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Price
    BB_Fixed_Price_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Price", Field_Type="Input_Normal", Validation="Integer") 
    BB_Fixed_Price_Frame_Var = BB_Fixed_Price_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Fixed_Price_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")
    BB_Fixed_Price_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Prices", "Fixed_Options", "Fix_Price"], Information=int(BB_Fixed_Price_Frame_Var.get())))
    Data_Functions.Entry_field_Insert(Field=BB_Fixed_Price_Frame_Var, Value=BB_Fixed_Price)

    # Field - Fixed Currency
    BB_Fixed_Currency_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Currency", Field_Type="Input_Normal") 
    BB_Fixed_Currency_Frame_Var = BB_Fixed_Currency_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Fixed_Currency_Frame_Var.configure(placeholder_text="Manual Currency", placeholder_text_color="#949A9F")
    BB_Fixed_Currency_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Currency", "Fix_Currency"], Information=BB_Fixed_Currency_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_Fixed_Currency_Frame_Var, Value=BB_Fixed_Currency)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_Posting_Date(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Method"]
    BB_Posting_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Methods_List"])
    BB_PD_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]

    BB_Posting_Date_Method_Variable = StringVar(master=Frame, value=BB_Posting_Date_Method, name="BB_Posting_Date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Invoice Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Vendor Invoice Date.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Invoice Date
    BB_Invoice_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_Invoice_Date_Method_Frame_Var = BB_Invoice_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Invoice_Date_Method_Frame_Var.configure(variable=BB_Posting_Date_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Invoice_Date_Method_Frame_Var, values=BB_Posting_Date_Method_List, command=lambda BB_Invoice_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Posting_Date_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Invoice_Date", "Method"], Information=BB_Invoice_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Date
    BB_PD_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Date_Picker", Validation="Date") 
    BB_PD_Fixed_Date_Frame_Var = BB_PD_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Button_INV_Fixed_Date_Frame_Var = BB_PD_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    BB_PD_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    BB_PD_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Invoice_Date", "Fixed_Options", "Fix_Date"], Information=BB_PD_Fixed_Date_Frame_Var.get()))
    BB_Button_INV_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=BB_PD_Fixed_Date_Frame_Var, Clicked_on_Button=BB_Button_INV_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Data_Functions.Entry_field_Insert(Field=BB_PD_Fixed_Date_Frame_Var, Value=BB_PD_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=BB_Button_INV_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_Order_reference(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Order_id_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Method"]
    BB_Order_id_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Methods_List"])
    BB_Fixed_Order_id = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Fixed_Options"]["Fixed_Order_ID"]

    BB_Order_date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Method"]
    BB_Order_date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Methods_List"])
    BB_OD_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Fixed_Options"]["Fixed_Order_Date"]

    BB_Order_id_Method_Variable = StringVar(master=Frame, value=BB_Order_id_Method, name="BB_Order_id_Method_Variable")
    BB_Order_date_Method_Variable = StringVar(master=Frame, value=BB_Order_date_Method, name="BB_Order_date_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Order Reference", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Order Reference like fictive Confirmation Id and Vendor creation date.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Section Order ID
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Order ID", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Number Method
    BB_Order_id_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_Order_id_Method_Frame_Var = BB_Order_id_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Order_id_Method_Frame_Var.configure(variable=BB_Order_id_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Order_id_Method_Frame_Var, values=BB_Order_id_Method_List, command=lambda BB_Order_id_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Order_id_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_id", "Method"], Information=BB_Order_id_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Order_id
    BB_Fixed_Order_id_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Order id", Field_Type="Input_Normal") 
    BB_Fixed_Order_id_Frame_Var = BB_Fixed_Order_id_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Fixed_Order_id_Frame_Var.configure(placeholder_text="Manual Order id", placeholder_text_color="#949A9F")
    BB_Fixed_Order_id_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_id", "Fixed_Options", "Fixed_Order_ID"], Information=BB_Fixed_Order_id_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_Fixed_Order_id_Frame_Var, Value=BB_Fixed_Order_id)

    # Section Order Date
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Order Date", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Number Method
    BB_Order_date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_Order_date_Method_Frame_Var = BB_Order_date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Order_date_Method_Frame_Var.configure(variable=BB_Order_date_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Order_date_Method_Frame_Var, values=BB_Order_date_Method_List, command=lambda BB_Order_date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Order_date_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_date", "Method"], Information=BB_Order_date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Order_date
    BB_OD_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Date_Picker", Validation="Date") 
    BB_OD_Fixed_Date_Frame_Var = BB_OD_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_BB_OD_Fixed_Date_Frame_Var = BB_OD_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    BB_OD_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    BB_OD_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Order_reference", "Order_date", "Fixed_Options", "Fixed_Order_Date"], Information=BB_OD_Fixed_Date_Frame_Var.get()))
    Button_BB_OD_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=BB_OD_Fixed_Date_Frame_Var, Clicked_on_Button=Button_BB_OD_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Data_Functions.Entry_field_Insert(Field=BB_OD_Fixed_Date_Frame_Var, Value=BB_OD_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_BB_OD_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_Plant(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Method"]
    BB_Inv_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Methods_List"])
    BB_Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    BB_Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Fixed_Options"]["Plants_List"])
    
    BB_Inv_Plant_Method_Variable = StringVar(master=Frame, value=BB_Inv_Plant_Method, name="BB_Inv_Plant_Method_Variable")
    BB_Inv_Fixed_Plant_Variable = StringVar(master=Frame, value=BB_Inv_Fixed_Plant, name="BB_Inv_Fixed_Plant_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Plant Method
    BB_Inv_Plant_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_Inv_Plant_Method_Frame_Var = BB_Inv_Plant_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Inv_Plant_Method_Frame_Var.configure(variable=BB_Inv_Plant_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Inv_Plant_Method_Frame_Var, values=BB_Inv_Plant_Method_List, command=lambda BB_Inv_Plant_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Inv_Plant_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Plants", "Method"], Information=BB_Inv_Plant_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Plant
    BB_Inv_Plant_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Plant", Field_Type="Input_OptionMenu") 
    BB_Inv_Plant_Fixed_Frame_Var = BB_Inv_Plant_Fixed_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Inv_Plant_Fixed_Frame_Var.configure(variable=BB_Inv_Fixed_Plant_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Inv_Plant_Fixed_Frame_Var, values=BB_Inv_Fixed_Plants_List, command=lambda BB_Inv_Plant_Fixed_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Inv_Fixed_Plant_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Plants", "Fixed_Options", "Fixed_Plant"], Information=BB_Inv_Plant_Fixed_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_CountryOrigin(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Method"]
    BB_Count_Origin_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Methods_List"])
    BB_Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    BB_Count_Origin_Method_Variable = StringVar(master=Frame, value=BB_Count_Origin_Method, name="BB_Count_Origin_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Country of Origin", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Country Codes in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    BB_Count_Origin_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_Count_Origin_Method_Frame_Var = BB_Count_Origin_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Count_Origin_Method_Frame_Var.configure(variable=BB_Count_Origin_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Count_Origin_Method_Frame_Var, values=BB_Count_Origin_Method_List, command=lambda BB_Count_Origin_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Count_Origin_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Country_Of_Origin", "Method"], Information=BB_Count_Origin_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Count_Origin
    BB_Fixed_Count_Origin_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Country code", Field_Type="Input_Normal") 
    BB_Fixed_Count_Origin_Frame_Var = BB_Fixed_Count_Origin_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Fixed_Count_Origin_Frame_Var.configure(placeholder_text="Manual Country Code", placeholder_text_color="#949A9F")
    BB_Fixed_Count_Origin_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Country_Of_Origin", "Fixed_Options", "Fix_Country_Of_Origin"], Information=BB_Fixed_Count_Origin_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_Fixed_Count_Origin_Frame_Var, Value=BB_Fixed_Count_Origin)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def BB_Tariff(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    BB_Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Method"]
    BB_Tariff_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Methods_List"])
    BB_Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    BB_Tariff_Method_Variable = StringVar(master=Frame, value=BB_Tariff_Method, name="BB_Tariff_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Tariffs", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define tariffs numbers in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    BB_Tariff_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    BB_Tariff_Method_Frame_Var = BB_Tariff_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Tariff_Method_Frame_Var.configure(variable=BB_Tariff_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Tariff_Method_Frame_Var, values=BB_Tariff_Method_List, command=lambda BB_Tariff_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=BB_Tariff_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Tariff", "Method"], Information=BB_Tariff_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Tariff
    BB_Fixed_Tariff_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Tariff", Field_Type="Input_Normal") 
    BB_Fixed_Tariff_Frame_Var = BB_Fixed_Tariff_Frame.children["!ctkframe3"].children["!ctkentry"]
    BB_Fixed_Tariff_Frame_Var.configure(placeholder_text="Manual Tariff Code", placeholder_text_color="#949A9F")
    BB_Fixed_Tariff_Frame_Var.bind("<FocusOut>", lambda BB_Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Tariff", "Fixed_Options", "Fix_Tariff"], Information=BB_Fixed_Tariff_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=BB_Fixed_Tariff_Frame_Var, Value=BB_Fixed_Tariff)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main