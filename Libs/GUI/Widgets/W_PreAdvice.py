# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, CTkEntry

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

def Delivery_Date(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    PReAdvice_Dates_Method = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Method"]
    PReAdvice_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Methods_List"])
    Pre_Fix_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Fixed_Options"]["Fix_Date"]

    Pre_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Random_Options"]["From"]
    Pre_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Random_Options"]["To"]
    Pre_Delivery_Shift = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Delivery_Date_Shift_Options"]["Shift_by"]

    PReAdvice_Dates_Method_Variable = StringVar(master=Frame, value=PReAdvice_Dates_Method, name="PReAdvice_Dates_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # TODO --> Blocking Fields
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Delivery Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Delivery Date
    Delivery_Date_Method_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    Delivery_Date_Method_Frame_Var = Delivery_Date_Method_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Delivery_Date_Method_Frame_Var.configure(variable=PReAdvice_Dates_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Delivery_Date_Method_Frame_Var, values=PReAdvice_Dates_Method_List, command=lambda Delivery_Date_Method_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=PReAdvice_Dates_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Method"], Information=Delivery_Date_Method_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Fixed Date
    Pre_Fixed_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Date", Field_Type="Entry_DropDown", Validation="Date") 
    Pre_Fixed_Date_Frame_Var = Pre_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
    Button_Pre_Fixed_Date_Frame_Var = Pre_Fixed_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Pre_Fixed_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
    Pre_Fixed_Date_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Fixed_Options", "Fix_Date"], Information=Pre_Fixed_Date_Frame_Var.get()))
    Button_Pre_Fixed_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Pre_Fixed_Date_Frame_Var, Clicked_on_Button=Button_Pre_Fixed_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=GUI_Level_ID))
    Entry_field_Insert(Field=Pre_Fixed_Date_Frame_Var, Value=Pre_Fix_Date)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Pre_Fixed_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Interval Date", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Delivery Date - From CD + Entry Field
    Pre_Random_From_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - From CD +", Field_Type="Input_Normal", Validation="Integer") 
    Pre_Random_From_Frame_Var = Pre_Random_From_Frame.children["!ctkframe3"].children["!ctkentry"]
    Pre_Random_From_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    Pre_Random_From_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Random_Options", "From"], Information=int(Pre_Random_From_Frame_Var.get())))
    Entry_field_Insert(Field=Pre_Random_From_Frame_Var, Value=Pre_Rand_From_Date)

    # Field - Delivery Date - To CD + Entry Field
    Pre_Random_To_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Date - To CD +", Field_Type="Input_Normal", Validation="Integer") 
    Pre_Random_To_Frame_Var = Pre_Random_To_Frame.children["!ctkframe3"].children["!ctkentry"]
    Pre_Random_To_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    Pre_Random_To_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Random_Options", "To"], Information=int(Pre_Random_To_Frame_Var.get())))
    Entry_field_Insert(Field=Pre_Random_To_Frame_Var, Value=Pre_Rand_To_Date)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Shift", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Delivery Date Shift by Entry field
    Pre_Del_Shift_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Delivery Date shift by", Field_Type="Input_Normal", Validation="Integer") 
    Pre_Del_Shift_Frame_Var = Pre_Del_Shift_Frame.children["!ctkframe3"].children["!ctkentry"]
    Pre_Del_Shift_Frame_Var.configure(placeholder_text="Number of Days", placeholder_text_color="#949A9F")
    Pre_Del_Shift_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Delivery_Date_Shift_Options", "Shift_by"], Information=int(Pre_Del_Shift_Frame_Var.get())))
    Entry_field_Insert(Field=Pre_Del_Shift_Frame_Var, Value=Pre_Delivery_Shift)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
