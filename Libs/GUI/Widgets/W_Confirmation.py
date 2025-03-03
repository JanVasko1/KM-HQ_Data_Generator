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
def PO_CON_Number(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Method"]
    Numbers_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Methods_List"])
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]

    Numbers_Method_Variable = StringVar(master=Frame, value=Numbers_Method, name="Numbers_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Numbers", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will build Confirmation Number.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    CON_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    CON_Number_Frame_Var = CON_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    CON_Number_Frame_Var.configure(variable=Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CON_Number_Frame_Var, values=Numbers_Method_List, command=lambda CON_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Method"], Information=CON_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Automatic Prefix
    NUM_CON_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_CON_FIX_Frame_Var = NUM_CON_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_CON_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_CON_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Fixed_Options", "Number"], Information=NUM_CON_FIX_Frame_Var.get()))
    Entry_field_Insert(Field=NUM_CON_FIX_Frame_Var, Value=Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Column_Header")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Price_Currency(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Method"]
    Currency_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Methods_List"])
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    Price_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Prices"]["Method"]
    Price_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Prices"]["Methods_List"])

    Price_Method_Variable = StringVar(master=Frame, value=Price_Method, name="Price_Method_Variable")
    Currency_Method_Variable = StringVar(master=Frame, value=Currency_Method, name="Currency_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Price Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Confirmation.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Price Method
    Prices_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_OptionMenu") 
    Prices_Method_Frame_Var = Prices_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Prices_Method_Frame_Var.configure(variable=Price_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Prices_Method_Frame_Var, values=Price_Method_List, command=lambda Prices_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Price_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Prices", "Method"], Information=Prices_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Number Method
    Currency_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Currency", Field_Type="Input_OptionMenu") 
    Currency_Method_Frame_Var = Currency_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Currency_Method_Frame_Var.configure(variable=Currency_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Currency_Method_Frame_Var, values=Currency_Method_List, command=lambda Currency_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Currency_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Currency", "Method"], Information=Currency_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Currency
    Fixed_Currency_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Currency", Field_Type="Input_Normal") 
    Fixed_Currency_Frame_Var = Fixed_Currency_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Currency_Frame_Var.configure(placeholder_text="Manual Currency", placeholder_text_color="#949A9F")
    Fixed_Currency_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Currency", "Fixed_Options", "Fix_Currency"], Information=Fixed_Currency_Frame_Var.get()))
    Entry_field_Insert(Field=Fixed_Currency_Frame_Var, Value=Fixed_Currency)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Line_Flags(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Line_Flags_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Use"]
    Line_Flag_Label_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Labels_always"]
    Line_Flags_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Method"]
    Line_Flags_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Line_Flags"]["Methods_List"])

    Line_Flags_Enabled_Variable = BooleanVar(master=Frame, value=Line_Flags_Enabled, name="Line_Flags_Enabled_Variable")
    Line_Flag_Label_Enabled_Variable = BooleanVar(master=Frame, value=Line_Flag_Label_Enabled, name="Line_Flag_Label_Enabled_Variable")
    Line_Flags_Method_Variable = StringVar(master=Frame, value=Line_Flags_Method, name="Line_Flags_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Line Flags", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will treat Line Flags.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Line_Flags_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Line_Flags_Frame_Var = Use_Line_Flags_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Line_Flags_Frame_Var.configure(variable=Line_Flags_Enabled_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Line_Flags_Enabled_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Use"], Information=Line_Flags_Enabled_Variable))

    # Field - Label Use always
    Use_Line_Flag_Label_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Label always", Field_Type="Input_CheckBox") 
    Use_Line_Flag_Label_Frame_Var = Use_Line_Flag_Label_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Line_Flag_Label_Frame_Var.configure(variable=Line_Flag_Label_Enabled_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Line_Flag_Label_Enabled_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Labels_always"], Information=Line_Flag_Label_Enabled_Variable))

    # Field - Number Method
    Line_Flags_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Line_Flags_Method_Frame_Var = Line_Flags_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Line_Flags_Method_Frame_Var.configure(variable=Line_Flags_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Line_Flags_Method_Frame_Var, values=Line_Flags_Method_List, command=lambda Line_Flags_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Line_Flags_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Method"], Information=Line_Flags_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_ATP(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Use"]
    ATP_Max_Records = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Max_ATP_Records"]
    ATP_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Method"]
    ATP_Quantity_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Methods_List"])
    ATP_Quantity_Random_Distr_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Random_Distribution_Percentage"])

    ATP_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Method"]
    ATP_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Methods_List"])

    ATP_Interval_ONH_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["From"]
    ATP_Interval_ONH_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["To"]
    ATP_Interval_ONB_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["From"]
    ATP_Interval_ONB_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["To"]

    ATP_ONH_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Manual_Dates"]["ONH"]
    ATP_ONB_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Manual_Dates"]["ONH"]

    ATP_Enabled_Variable = BooleanVar(master=Frame, value=ATP_Enabled, name="ATP_Enabled_Variable")
    ATP_Quantity_Method_Variable = StringVar(master=Frame, value=ATP_Quantity_Method, name="ATP_Quantity_Method_Variable")
    ATP_Dates_Method_Variable = StringVar(master=Frame, value=ATP_Dates_Method, name="ATP_Dates_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="ATP", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will work on ATP for each line.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_ATP_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_ATP_Frame_Var = Use_ATP_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_ATP_Frame_Var.configure(variable=ATP_Enabled_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=ATP_Enabled_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Use"], Information=ATP_Enabled_Variable))

    # Field - ATP Max Records per Item
    ATP_Max_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Max Records", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Max_Frame_Var = ATP_Max_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Max_Frame_Var.configure(placeholder_text="Max records per Item", placeholder_text_color="#949A9F")
    ATP_Max_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Max_ATP_Records"], Information=int(ATP_Max_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Max_Frame_Var, Value=ATP_Max_Records)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Quantities", Label_Size="Field_Label" , Font_Size="Column_Header")

    # Field - Quantities Methods
    ATP_QTY_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    ATP_QTY_Method_Frame_Var = ATP_QTY_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    ATP_QTY_Method_Frame_Var.configure(variable=ATP_Quantity_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=ATP_QTY_Method_Frame_Var, values=ATP_Quantity_Method_List, command=lambda ATP_QTY_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=ATP_Quantity_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Method"], Information=ATP_QTY_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # TODO --> Quantity Distribution Percentage --> somyslet jak to ukázat v DB

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Dates", Label_Size="Field_Label" , Font_Size="Column_Header")

    # Field - Dates Methods
    ATP_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    ATP_Date_Method_Frame_Var = ATP_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    ATP_Date_Method_Frame_Var.configure(variable=ATP_Dates_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=ATP_Date_Method_Frame_Var, values=ATP_Dates_Method_List, command=lambda ATP_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=ATP_Dates_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Method"], Information=ATP_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - ONH - From CD + Entry Field
    ATP_Interval_ONH_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONH_From_Frame_Var = ATP_Interval_ONH_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONH_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONH_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONH", "From"], Information=int(ATP_Interval_ONH_From_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONH_From_Frame_Var, Value=ATP_Interval_ONH_From)

    # Field - ONH - To CD + Entry Field
    ATP_Interval_ONH_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONH_To_Frame_Var = ATP_Interval_ONH_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONH_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONH_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONH", "To"], Information=int(ATP_Interval_ONH_To_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONH_To_Frame_Var, Value=ATP_Interval_ONH_To)

    # Field - ONB - From CD + Entry Field
    ATP_Interval_ONB_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONB_From_Frame_Var = ATP_Interval_ONB_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONB_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONB_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONB", "From"], Information=int(ATP_Interval_ONB_From_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONB_From_Frame_Var, Value=ATP_Interval_ONB_From)

    # Field - ONB - To CD + Entry Field
    ATP_Interval_ONB_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONB_To_Frame_Var = ATP_Interval_ONB_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONB_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONB_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONB", "To"], Information=int(ATP_Interval_ONB_To_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONB_To_Frame_Var, Value=ATP_Interval_ONB_To)

    # Field - On-Hand Date
    Man_ONH_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH Date", Field_Type="Entry_DropDown", Validation="Date") 
    Man_ONH_Date_Frame_Var = Man_ONH_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Man_ONH_DateFrame_Var_Var = Man_ONH_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Man_ONH_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    Man_ONH_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Manual_Dates", "ONH"], Information=Man_ONH_Date_Frame_Var.get()))
    Button_Man_ONH_DateFrame_Var_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Man_ONH_Date_Frame_Var, Clicked_on_Button=Button_Man_ONH_DateFrame_Var_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=Man_ONH_Date_Frame_Var, Value=ATP_ONH_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Man_ONH_DateFrame_Var_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Field - Date To
    Man_ONB_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB Date", Field_Type="Entry_DropDown", Validation="Date")
    Man_ONB_Date_Frame_Var = Man_ONB_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Man_ONB_Date_Frame_Var_Var = Man_ONB_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Man_ONB_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    Man_ONB_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Manual_Dates", "ONB"], Information=Man_ONB_Date_Frame_Var.get()))
    Button_Man_ONB_Date_Frame_Var_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Man_ONB_Date_Frame_Var, Clicked_on_Button=Button_Man_ONB_Date_Frame_Var_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=Man_ONB_Date_Frame_Var, Value=ATP_ONB_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Man_ONB_Date_Frame_Var_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
