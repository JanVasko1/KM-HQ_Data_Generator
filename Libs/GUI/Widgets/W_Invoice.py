# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, CTkEntry, BooleanVar

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Entry_field_Insert(Field: CTkEntry, Value: str|int) -> None:
    if type(Value) == str:
        if Value != "":
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    elif type(Value) == int:
        if Value > 0:
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    else:
        pass

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #--------------------------------------------------- Tabs--------------------------------------------------------------------------#
def PO_INV_Number(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]

    Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="Numbers_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Invoice Number.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    INV_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    INV_Number_Frame_Var = INV_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    INV_Number_Frame_Var.configure(variable=Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=INV_Number_Frame_Var, values=Numbers_Method_List, command=lambda INV_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Method"], Information=INV_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Automatic Prefix
    NUM_INV_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_INV_FIX_Frame_Var = NUM_INV_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_INV_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_INV_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Fixed_Options", "Number"], Information=NUM_INV_FIX_Frame_Var.get()))
    Entry_field_Insert(Field=NUM_INV_FIX_Frame_Var, Value=Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Column_Header")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Price_Currency(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Method"]
    Currency_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Methods_List"])
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Method"]
    Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Prices"]["Methods_List"])

    Price_Method_Variable = StringVar(master=Frame, value=Price_Method, name="Price_Method_Variable")
    Currency_Method_Variable = StringVar(master=Frame, value=Currency_Method, name="Currency_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Price Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Price Method
    Prices_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_OptionMenu") 
    Prices_Method_Frame_Var = Prices_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Prices_Method_Frame_Var.configure(variable=Price_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Prices_Method_Frame_Var, values=Price_Method_List, command=lambda Prices_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Price_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Prices", "Method"], Information=Prices_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Number Method
    Currency_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Currency", Field_Type="Input_OptionMenu") 
    Currency_Method_Frame_Var = Currency_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Currency_Method_Frame_Var.configure(variable=Currency_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Currency_Method_Frame_Var, values=Currency_Method_List, command=lambda Currency_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Currency_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Currency", "Method"], Information=Currency_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Currency
    Fixed_Currency_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Currency", Field_Type="Input_Normal") 
    Fixed_Currency_Frame_Var = Fixed_Currency_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Currency_Frame_Var.configure(placeholder_text="Manual Currency", placeholder_text_color="#949A9F")
    Fixed_Currency_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Currency", "Fixed_Options", "Fix_Currency"], Information=Fixed_Currency_Frame_Var.get()))
    Entry_field_Insert(Field=Fixed_Currency_Frame_Var, Value=Fixed_Currency)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Posting_Date(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Posting_Date"]["Method"]
    Posting_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Posting_Date"]["Methods_List"])
    INV_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Posting_Date"]["Fixed_Options"]["Fix_Date"]

    INV_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Posting_Date"]["Random_Options"]["From"]
    INV_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Posting_Date"]["Random_Options"]["To"]

    Posting_Date_Method_Variable = StringVar(master=Frame, value=Posting_Date_Method, name="Posting_Date_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Invoice Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Vendor Invoice Date.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Invoice Date
    Invoice_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Invoice_Date_Method_Frame_Var = Invoice_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Invoice_Date_Method_Frame_Var.configure(variable=Posting_Date_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Invoice_Date_Method_Frame_Var, values=Posting_Date_Method_List, command=lambda Invoice_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Posting_Date_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Posting_Date", "Method"], Information=Invoice_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Date
    INV_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Entry_DropDown", Validation="Date") 
    INV_Fixed_Date_Frame_Var = INV_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_INV_Fixed_Date_Frame_Var = INV_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    INV_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    INV_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Posting_Date", "Fixed_Options", "Fix_Date"], Information=INV_Fixed_Date_Frame_Var.get()))
    Button_INV_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=INV_Fixed_Date_Frame_Var, Clicked_on_Button=Button_INV_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=INV_Fixed_Date_Frame_Var, Value=INV_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_INV_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automation", Label_Size="Field_Label" , Font_Size="Column_Header")

    # Field - Invoice Date - From CD + Entry Field
    INV_Random_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    INV_Random_From_Frame_Var = INV_Random_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    INV_Random_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    INV_Random_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Posting_Date", "Random_Options", "From"], Information=int(INV_Random_From_Frame_Var.get())))
    Entry_field_Insert(Field=INV_Random_From_Frame_Var, Value=INV_Rand_From_Date)

    # Field - Invoice Date - To CD + Entry Field
    INV_Random_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    INV_Random_To_Frame_Var = INV_Random_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    INV_Random_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    INV_Random_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Posting_Date", "Random_Options", "To"], Information=int(INV_Random_To_Frame_Var.get())))
    Entry_field_Insert(Field=INV_Random_To_Frame_Var, Value=INV_Rand_To_Date)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def PO_Plant(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Method"]
    Inv_Plant_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Methods_List"])
    Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    Inv_Fixed_Plant_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Plants"]["Fixed_Options"]["Plant_List"])
    
    Inv_Plant_Method_Variable = StringVar(master=Frame, value=Inv_Plant_Method, name="Inv_Plant_Method_Variable")
    Inv_Fixed_Plant_Variable = StringVar(master=Frame, value=Inv_Fixed_Plant, name="Inv_Fixed_Plant_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Plants", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Plants assignment details.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Plant Method
    Inv_Plant_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Inv_Plant_Method_Frame_Var = Inv_Plant_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Inv_Plant_Method_Frame_Var.configure(variable=Inv_Plant_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Inv_Plant_Method_Frame_Var, values=Inv_Plant_Method_List, command=lambda Inv_Plant_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Inv_Plant_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Plants", "Method"], Information=Inv_Plant_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Plant
    Inv_Plant_Fixed_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Inv_Plant_Fixed_Frame_Var = Inv_Plant_Fixed_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Inv_Plant_Fixed_Frame_Var.configure(variable=Inv_Fixed_Plant_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Inv_Plant_Fixed_Frame_Var, values=Inv_Fixed_Plant_List, command=lambda Inv_Plant_Fixed_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Inv_Fixed_Plant_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Plants", "Fixed_Options", "Fixed_Plant"], Information=Inv_Plant_Fixed_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_CountryOrigin(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Method"]
    Count_Origin_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Methods_List"])
    Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    Count_Origin_Method_Variable = StringVar(master=Frame, value=Count_Origin_Method, name="Count_Origin_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Country of Origin", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Country Codes in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    Count_Origin_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Count_Origin_Method_Frame_Var = Count_Origin_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Count_Origin_Method_Frame_Var.configure(variable=Count_Origin_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Count_Origin_Method_Frame_Var, values=Count_Origin_Method_List, command=lambda Count_Origin_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Count_Origin_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Country_Of_Origin", "Method"], Information=Count_Origin_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Count_Origin
    Fixed_Count_Origin_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Count code", Field_Type="Input_Normal") 
    Fixed_Count_Origin_Frame_Var = Fixed_Count_Origin_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Count_Origin_Frame_Var.configure(placeholder_text="Manual Country Code", placeholder_text_color="#949A9F")
    Fixed_Count_Origin_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Country_Of_Origin", "Fixed_Options", "Fix_Country_Of_Origin"], Information=Fixed_Count_Origin_Frame_Var.get()))
    Entry_field_Insert(Field=Fixed_Count_Origin_Frame_Var, Value=Fixed_Count_Origin)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Tariff(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Method"]
    Tariff_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Methods_List"])
    Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    Tariff_Method_Variable = StringVar(master=Frame, value=Tariff_Method, name="Tariff_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Tariffs", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define tariffs numbers in Invoice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    Tariff_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Tariff_Method_Frame_Var = Tariff_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Tariff_Method_Frame_Var.configure(variable=Tariff_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Tariff_Method_Frame_Var, values=Tariff_Method_List, command=lambda Tariff_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Tariff_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Tariff", "Method"], Information=Tariff_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Tariff
    Fixed_Tariff_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Count code", Field_Type="Input_Normal") 
    Fixed_Tariff_Frame_Var = Fixed_Tariff_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Tariff_Frame_Var.configure(placeholder_text="Manual Tariff Code", placeholder_text_color="#949A9F")
    Fixed_Tariff_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Tariff", "Fixed_Options", "Fix_Tariff"], Information=Fixed_Tariff_Frame_Var.get()))
    Entry_field_Insert(Field=Fixed_Tariff_Frame_Var, Value=Fixed_Tariff)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main