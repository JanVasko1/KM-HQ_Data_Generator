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
def PO_CON_Number(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
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
    CON_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    CON_Number_Frame_Var = CON_Number_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    CON_Number_Frame_Var.configure(variable=Numbers_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CON_Number_Frame_Var, values=Numbers_Method_List, command=lambda CON_Number_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Numbers_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Method"], Information=CON_Number_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Automatic Prefix
    NUM_CON_FIX_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Number", Field_Type="Input_Normal") 
    NUM_CON_FIX_Frame_Var = NUM_CON_FIX_Frame.children["!ctkframe3"].children["!ctkentry"]
    NUM_CON_FIX_Frame_Var.configure(placeholder_text="Manual Number", placeholder_text_color="#949A9F")
    NUM_CON_FIX_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Fixed_Options", "Number"], Information=NUM_CON_FIX_Frame_Var.get()))
    Entry_field_Insert(Field=NUM_CON_FIX_Frame_Var, Value=Fixed_Number)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Automatic Setup", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Automatic Prefix
    AUT_Prefix_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Prefix", Field_Type="Input_Normal") 
    AUT_Prefix_Frame_Var = AUT_Prefix_Frame.children["!ctkframe3"].children["!ctkentry"]
    AUT_Prefix_Frame_Var.configure(placeholder_text="Prefix for unique number", placeholder_text_color="#949A9F")
    AUT_Prefix_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Number", "Automatic_Options", "Prefix"], Information=AUT_Prefix_Frame_Var.get()))
    Entry_field_Insert(Field=AUT_Prefix_Frame_Var, Value=Automatic_Prefix)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Generation_Date(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Generation_Date_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Method"]
    Generation_Date_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Methods_List"])
    Gen_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Fixed_Options"]["Fix_Date"]

    Generation_Date_Method_Variable = StringVar(master=Frame, value=Generation_Date_Method, name="Generation_Date_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Generation Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Date of generation Confirmation.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Confirmation Date
    Generation_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Generation_Date_Method_Frame_Var = Generation_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Generation_Date_Method_Frame_Var.configure(variable=Generation_Date_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Generation_Date_Method_Frame_Var, values=Generation_Date_Method_List, command=lambda Generation_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generation_Date_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Generation_Date", "Method"], Information=Generation_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Date
    Gen_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Entry_DropDown", Validation="Date") 
    Gen_Fixed_Date_Frame_Var = Gen_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Gen_Fixed_Date_Frame_Var = Gen_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Gen_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    Gen_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Generation_Date", "Fixed_Options", "Fix_Date"], Information=Gen_Fixed_Date_Frame_Var.get()))
    Button_Gen_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Gen_Fixed_Date_Frame_Var, Clicked_on_Button=Button_Gen_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=Gen_Fixed_Date_Frame_Var, Value=Gen_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Gen_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Unit_of_Measure(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    UoM_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Method"]
    UoM_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Methods_List"])
    Fixed_UoM = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Unit_of_Measure"]["Fixed_Options"]["Fix_UoM"]

    UoM_Method_Variable = StringVar(master=Frame, value=UoM_Method, name="UoM_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Unit of Measure", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define Unit of Measure in Confirmation.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    UoM_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Unit of Measure", Field_Type="Input_OptionMenu") 
    UoM_Method_Frame_Var = UoM_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    UoM_Method_Frame_Var.configure(variable=UoM_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=UoM_Method_Frame_Var, values=UoM_Method_List, command=lambda UoM_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=UoM_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Unit_of_Measure", "Method"], Information=UoM_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed UoM
    Fixed_UoM_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Unit of Measure", Field_Type="Input_Normal") 
    Fixed_UoM_Frame_Var = Fixed_UoM_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_UoM_Frame_Var.configure(placeholder_text="Manual Unit of Measure", placeholder_text_color="#949A9F")
    Fixed_UoM_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Unit_of_Measure", "Fixed_Options", "Fix_UoM"], Information=Fixed_UoM_Frame_Var.get()))
    Entry_field_Insert(Field=Fixed_UoM_Frame_Var, Value=Fixed_UoM)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Price_Currency(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
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
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Price and Currency", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will define price and currency in Confirmation.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Price Method
    Prices_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_OptionMenu") 
    Prices_Method_Frame_Var = Prices_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Prices_Method_Frame_Var.configure(variable=Price_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Prices_Method_Frame_Var, values=Price_Method_List, command=lambda Prices_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Price_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Prices", "Method"], Information=Prices_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Number Method
    Currency_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Currency", Field_Type="Input_OptionMenu") 
    Currency_Method_Frame_Var = Currency_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Currency_Method_Frame_Var.configure(variable=Currency_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Currency_Method_Frame_Var, values=Currency_Method_List, command=lambda Currency_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Currency_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Currency", "Method"], Information=Currency_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Currency
    Fixed_Currency_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Currency", Field_Type="Input_Normal") 
    Fixed_Currency_Frame_Var = Fixed_Currency_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Currency_Frame_Var.configure(placeholder_text="Manual Currency", placeholder_text_color="#949A9F")
    Fixed_Currency_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Currency", "Fixed_Options", "Fix_Currency"], Information=Fixed_Currency_Frame_Var.get()))
    Entry_field_Insert(Field=Fixed_Currency_Frame_Var, Value=Fixed_Currency)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Line_Flags(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
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
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Line Flags", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will treat Line Flags.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Use_Line_Flags_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_Line_Flags_Frame_Var = Use_Line_Flags_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Line_Flags_Frame_Var.configure(variable=Line_Flags_Enabled_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Line_Flags_Enabled_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Use"], Information=Line_Flags_Enabled_Variable))

    # Field - Number Method
    Line_Flags_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Line_Flags_Method_Frame_Var = Line_Flags_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Line_Flags_Method_Frame_Var.configure(variable=Line_Flags_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Line_Flags_Method_Frame_Var, values=Line_Flags_Method_List, command=lambda Line_Flags_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Line_Flags_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Method"], Information=Line_Flags_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Global Flags", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Label Use always
    Use_Line_Flag_Label_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Label always", Field_Type="Input_CheckBox") 
    Use_Line_Flag_Label_Frame_Var = Use_Line_Flag_Label_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_Line_Flag_Label_Frame_Var.configure(variable=Line_Flag_Label_Enabled_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Line_Flag_Label_Enabled_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Labels_always"], Information=Line_Flag_Label_Enabled_Variable))

    # Field - Item End of Live always Finished
    Finished_EOL_Item_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Finish EOL Item", Field_Type="Input_CheckBox") 
    Finished_EOL_Item_Frame_Var = Finished_EOL_Item_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Finished_EOL_Item_Frame_Var.configure(variable=Line_Flag_Item_EOL_Finished_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Line_Flag_Item_EOL_Finished_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Item_EOL_Finish"], Information=Line_Flag_Item_EOL_Finished_Variable))

    # Field - Always Substitute
    Always_Substitute_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Always Substitute", Field_Type="Input_CheckBox") 
    Always_Substitute_Frame_Var = Always_Substitute_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Always_Substitute_Frame_Var.configure(variable=Line_Flag_Always_Substitute_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Line_Flag_Always_Substitute_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Line_Flags", "Always_Substitute"], Information=Line_Flag_Always_Substitute_Variable))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_ATP_General(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_Enabled = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Use"]
    ATP_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Method"]
    ATP_Quantity_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Methods_List"])

    ATP_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Method"]
    ATP_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Methods_List"])

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
    Use_ATP_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Use", Field_Type="Input_CheckBox") 
    Use_ATP_Frame_Var = Use_ATP_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Use_ATP_Frame_Var.configure(variable=ATP_Enabled_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=ATP_Enabled_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Use"], Information=ATP_Enabled_Variable))

    # Field - Quantities Methods
    ATP_QTY_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Quantity Method", Field_Type="Input_OptionMenu") 
    ATP_QTY_Method_Frame_Var = ATP_QTY_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    ATP_QTY_Method_Frame_Var.configure(variable=ATP_Quantity_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=ATP_QTY_Method_Frame_Var, values=ATP_Quantity_Method_List, command=lambda ATP_QTY_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=ATP_Quantity_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Method"], Information=ATP_QTY_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Dates Methods
    ATP_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date Method", Field_Type="Input_OptionMenu") 
    ATP_Date_Method_Frame_Var = ATP_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    ATP_Date_Method_Frame_Var.configure(variable=ATP_Dates_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=ATP_Date_Method_Frame_Var, values=ATP_Dates_Method_List, command=lambda ATP_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=ATP_Dates_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Method"], Information=ATP_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_ATP_Quantity_Distribution(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    ONH_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["ONH"]
    ONB_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["ONB"]
    BACK_Ratio = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Quantities"]["Ratio"]["BACK"]
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Quantity distribution", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to Ratio between each state.\nGood to distribute values as percentage up to 100", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - ATP Distribution ONH
    ONH_Ratio_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH Ratio", Field_Type="Input_Normal", Validation="Integer") 
    ONH_Ratio_Frame_Var = ONH_Ratio_Frame.children["!ctkframe3"].children["!ctkentry"]
    ONH_Ratio_Frame_Var.configure(placeholder_text="OnHand Ratio", placeholder_text_color="#949A9F")
    ONH_Ratio_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Ratio", "ONH"], Information=int(ONH_Ratio_Frame_Var.get())))
    Entry_field_Insert(Field=ONH_Ratio_Frame_Var, Value=ONH_Ratio)
   
    # Field - ATP Distribution ONB
    ONB_Ratio_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB Ratio", Field_Type="Input_Normal", Validation="Integer") 
    ONB_Ratio_Frame_Var = ONB_Ratio_Frame.children["!ctkframe3"].children["!ctkentry"]
    ONB_Ratio_Frame_Var.configure(placeholder_text="OnBoard Ratio", placeholder_text_color="#949A9F")
    ONB_Ratio_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Ratio", "ONB"], Information=int(ONB_Ratio_Frame_Var.get())))
    Entry_field_Insert(Field=ONB_Ratio_Frame_Var, Value=ONB_Ratio)
       
    # Field - ATP Distribution BACK
    BACK_Ratio_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="BACK Ratio", Field_Type="Input_Normal", Validation="Integer") 
    BACK_Ratio_Frame_Var = BACK_Ratio_Frame.children["!ctkframe3"].children["!ctkentry"]
    BACK_Ratio_Frame_Var.configure(placeholder_text="BackOrder Ratio", placeholder_text_color="#949A9F")
    BACK_Ratio_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Quantities", "Ratio", "BACK"], Information=int(BACK_Ratio_Frame_Var.get())))
    Entry_field_Insert(Field=BACK_Ratio_Frame_Var, Value=BACK_Ratio)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def PO_ATP_Fixed_Dates(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_ONH_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Fixed_Dates"]["ONH"]
    ATP_ONB_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Fixed_Dates"]["ONB"]

    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Fixed Dates", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will delivery Fixed Dates.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - On-Hand Date
    Man_ONH_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH Date", Field_Type="Entry_DropDown", Validation="Date") 
    Man_ONH_Date_Frame_Var = Man_ONH_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Man_ONH_DateFrame_Var_Var = Man_ONH_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Man_ONH_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    Man_ONH_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Fixed_Dates", "ONH"], Information=Man_ONH_Date_Frame_Var.get()))
    Button_Man_ONH_DateFrame_Var_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Man_ONH_Date_Frame_Var, Clicked_on_Button=Button_Man_ONH_DateFrame_Var_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=Man_ONH_Date_Frame_Var, Value=ATP_ONH_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Man_ONH_DateFrame_Var_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Field - Date To
    Man_ONB_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB Date", Field_Type="Entry_DropDown", Validation="Date")
    Man_ONB_Date_Frame_Var = Man_ONB_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Man_ONB_Date_Frame_Var_Var = Man_ONB_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Man_ONB_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    Man_ONB_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Fixed_Dates", "ONB"], Information=Man_ONB_Date_Frame_Var.get()))
    Button_Man_ONB_Date_Frame_Var_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Man_ONB_Date_Frame_Var, Clicked_on_Button=Button_Man_ONB_Date_Frame_Var_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=Man_ONB_Date_Frame_Var, Value=ATP_ONB_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Man_ONB_Date_Frame_Var_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_ATP_Interval_Dates(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    ATP_Interval_ONH_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["From"]
    ATP_Interval_ONH_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONH"]["To"]
    ATP_Interval_ONB_From = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["From"]
    ATP_Interval_ONB_To = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["ATP"]["Dates_Intervals"]["Intervals_Dates"]["ONB"]["To"]

    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Interval Dates", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will delivery Interval Dates.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - ONH - From CD + Entry Field
    ATP_Interval_ONH_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONH_From_Frame_Var = ATP_Interval_ONH_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONH_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONH_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONH", "From"], Information=int(ATP_Interval_ONH_From_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONH_From_Frame_Var, Value=ATP_Interval_ONH_From)

    # Field - ONH - To CD + Entry Field
    ATP_Interval_ONH_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONH - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONH_To_Frame_Var = ATP_Interval_ONH_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONH_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONH_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONH", "To"], Information=int(ATP_Interval_ONH_To_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONH_To_Frame_Var, Value=ATP_Interval_ONH_To)

    # Field - ONB - From CD + Entry Field
    ATP_Interval_ONB_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONB_From_Frame_Var = ATP_Interval_ONB_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONB_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONB_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONB", "From"], Information=int(ATP_Interval_ONB_From_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONB_From_Frame_Var, Value=ATP_Interval_ONB_From)

    # Field - ONB - To CD + Entry Field
    ATP_Interval_ONB_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="ONB - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    ATP_Interval_ONB_To_Frame_Var = ATP_Interval_ONB_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    ATP_Interval_ONB_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    ATP_Interval_ONB_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "ATP", "Dates_Intervals", "Intervals_Dates", "ONB", "To"], Information=int(ATP_Interval_ONB_To_Frame_Var.get())))
    Entry_field_Insert(Field=ATP_Interval_ONB_To_Frame_Var, Value=ATP_Interval_ONB_To)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def PO_Items_Free_Method(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Free_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Method"]
    Free_Method_List = list(Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Methods_List"])
    
    Free_Method_Variable = StringVar(master=Frame, value=Free_Method, name="Free_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Free of Charge", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program will treat Free of Charge Items for Confirmation.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Price Method
    Free_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Free_Method_Frame_Var = Free_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Free_Method_Frame_Var.configure(variable=Free_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Free_Method_Frame_Var, values=Free_Method_List, command=lambda Free_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Free_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Method"], Information=Free_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Items_Free_Cable(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Cable_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Number"]
    Cable_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Description"]
    Cable_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["QTY_per_Machine"]
    Cable_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Cable"]["Price"]
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Cable", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Fixed cable item settings.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Cable Number
    Cable_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Number", Field_Type="Input_Normal") 
    Cable_Number_Frame_Var = Cable_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
    Cable_Number_Frame_Var.configure(placeholder_text="Cable number", placeholder_text_color="#949A9F")
    Cable_Number_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "Number"], Information=Cable_Number_Frame_Var.get()))
    Entry_field_Insert(Field=Cable_Number_Frame_Var, Value=Cable_Number)

    # Field - Cable Description
    Cable_Description_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Cable_Description_Frame_Var = Cable_Description_Frame.children["!ctkframe3"].children["!ctkentry"]
    Cable_Description_Frame_Var.configure(placeholder_text="Cable Description", placeholder_text_color="#949A9F")
    Cable_Description_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "Description"], Information=Cable_Description_Frame_Var.get()))
    Entry_field_Insert(Field=Cable_Description_Frame_Var, Value=Cable_Description)

    # Field - Cable QTY_per_Machine
    Cable_QTY_per_Machine_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="QTY per Machine", Field_Type="Input_Normal", Validation="Integer") 
    Cable_QTY_per_Machine_Frame_Var = Cable_QTY_per_Machine_Frame.children["!ctkframe3"].children["!ctkentry"]
    Cable_QTY_per_Machine_Frame_Var.configure(placeholder_text="Cable QTY per Machine", placeholder_text_color="#949A9F")
    Cable_QTY_per_Machine_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "QTY_per_Machine"], Information=int(Cable_QTY_per_Machine_Frame_Var.get())))
    Entry_field_Insert(Field=Cable_QTY_per_Machine_Frame_Var, Value=Cable_QTY_per_Machine)

    # Field - Cable Price
    Cable_Price_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_Normal", Validation="Integer") 
    Cable_Price_Frame_Var = Cable_Price_Frame.children["!ctkframe3"].children["!ctkentry"]
    Cable_Price_Frame_Var.configure(placeholder_text="Cable Price", placeholder_text_color="#949A9F")
    Cable_Price_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Cable", "Price"], Information=int(Cable_Price_Frame_Var.get())))
    Entry_field_Insert(Field=Cable_Price_Frame_Var, Value=Cable_Price)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def PO_Items_Free_Documentation(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Documentation_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Number"]
    Documentation_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Description"]
    Documentation_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["QTY_per_Machine"]
    Documentation_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Documentation"]["Price"]
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Documentation", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Fixed documentation item settings.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Documentation Number
    Documentation_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Number", Field_Type="Input_Normal") 
    Documentation_Number_Frame_Var = Documentation_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
    Documentation_Number_Frame_Var.configure(placeholder_text="Documentation number", placeholder_text_color="#949A9F")
    Documentation_Number_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "Number"], Information=Documentation_Number_Frame_Var.get()))
    Entry_field_Insert(Field=Documentation_Number_Frame_Var, Value=Documentation_Number)

    # Field - Documentation Description
    Documentation_Description_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Documentation_Description_Frame_Var = Documentation_Description_Frame.children["!ctkframe3"].children["!ctkentry"]
    Documentation_Description_Frame_Var.configure(placeholder_text="Documentation Description", placeholder_text_color="#949A9F")
    Documentation_Description_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "Description"], Information=Documentation_Description_Frame_Var.get()))
    Entry_field_Insert(Field=Documentation_Description_Frame_Var, Value=Documentation_Description)

    # Field - Documentation QTY_per_Machine
    Documentation_QTY_per_Machine_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="QTY per Machine", Field_Type="Input_Normal", Validation="Integer") 
    Documentation_QTY_per_Machine_Frame_Var = Documentation_QTY_per_Machine_Frame.children["!ctkframe3"].children["!ctkentry"]
    Documentation_QTY_per_Machine_Frame_Var.configure(placeholder_text="Documentation QTY per Machine", placeholder_text_color="#949A9F")
    Documentation_QTY_per_Machine_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "QTY_per_Machine"], Information=int(Documentation_QTY_per_Machine_Frame_Var.get())))
    Entry_field_Insert(Field=Documentation_QTY_per_Machine_Frame_Var, Value=Documentation_QTY_per_Machine)

    # Field - Documentation Price
    Documentation_Price_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_Normal", Validation="Integer") 
    Documentation_Price_Frame_Var = Documentation_Price_Frame.children["!ctkframe3"].children["!ctkentry"]
    Documentation_Price_Frame_Var.configure(placeholder_text="Documentation Price", placeholder_text_color="#949A9F")
    Documentation_Price_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Documentation", "Price"], Information=int(Documentation_Price_Frame_Var.get())))
    Entry_field_Insert(Field=Documentation_Price_Frame_Var, Value=Documentation_Price)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def PO_Items_Free_Face_Sheet(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Face_Sheet_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Number"]
    Face_Sheet_Description = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Description"]
    Face_Sheet_QTY_per_Machine = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["QTY_per_Machine"]
    Face_Sheet_Price = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Free_Of_Charge"]["Fixed_Options"]["Face_Sheet"]["Price"]
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Others", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Fixed others (Label, Sticker ...) item settings.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Others Number
    Face_Sheet_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Number", Field_Type="Input_Normal") 
    Face_Sheet_Number_Frame_Var = Face_Sheet_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
    Face_Sheet_Number_Frame_Var.configure(placeholder_text="Others number", placeholder_text_color="#949A9F")
    Face_Sheet_Number_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "Number"], Information=Face_Sheet_Number_Frame_Var.get()))
    Entry_field_Insert(Field=Face_Sheet_Number_Frame_Var, Value=Face_Sheet_Number)

    # Field - Others Description
    Face_Sheet_Description_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Description", Field_Type="Input_Normal") 
    Face_Sheet_Description_Frame_Var = Face_Sheet_Description_Frame.children["!ctkframe3"].children["!ctkentry"]
    Face_Sheet_Description_Frame_Var.configure(placeholder_text="Others Description", placeholder_text_color="#949A9F")
    Face_Sheet_Description_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "Description"], Information=Face_Sheet_Description_Frame_Var.get()))
    Entry_field_Insert(Field=Face_Sheet_Description_Frame_Var, Value=Face_Sheet_Description)

    # Field - Others QTY_per_Machine
    Face_Sheet_QTY_per_Machine_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="QTY per Machine", Field_Type="Input_Normal", Validation="Integer") 
    Face_Sheet_QTY_per_Machine_Frame_Var = Face_Sheet_QTY_per_Machine_Frame.children["!ctkframe3"].children["!ctkentry"]
    Face_Sheet_QTY_per_Machine_Frame_Var.configure(placeholder_text="Others QTY per Machine", placeholder_text_color="#949A9F")
    Face_Sheet_QTY_per_Machine_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "QTY_per_Machine"], Information=int(Face_Sheet_QTY_per_Machine_Frame_Var.get())))
    Entry_field_Insert(Field=Face_Sheet_QTY_per_Machine_Frame_Var, Value=Face_Sheet_QTY_per_Machine)

    # Field - Others Price
    Face_Sheet_Price_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Price", Field_Type="Input_Normal", Validation="Integer") 
    Face_Sheet_Price_Frame_Var = Face_Sheet_Price_Frame.children["!ctkframe3"].children["!ctkentry"]
    Face_Sheet_Price_Frame_Var.configure(placeholder_text="Others Price", placeholder_text_color="#949A9F")
    Face_Sheet_Price_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Free_Of_Charge", "Fixed_Options", "Face_Sheet", "Price"], Information=int(Face_Sheet_Price_Frame_Var.get())))
    Entry_field_Insert(Field=Face_Sheet_Price_Frame_Var, Value=Face_Sheet_Price)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
