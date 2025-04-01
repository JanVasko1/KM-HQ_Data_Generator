# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar

import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Date_Picker

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #

def Delivery_Date(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    PreAdvice_Dates_Method = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Method"]
    PreAdvice_Dates_Method_List = list(Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Methods_List"])
    Pre_Fix_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Fixed_Options"]["Fix_Date"]

    Pre_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Random_Options"]["From"]
    Pre_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Random_Options"]["To"]
    Pre_Gen_Date_Shift = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Shift_Options"]["Generation_Date_Shift_by"]
    Pre_Delivery_Shift = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Shift_Options"]["Delivery_Date_Shift_by"]

    PreAdvice_Dates_Method_Variable = StringVar(master=Frame, value=PreAdvice_Dates_Method, name="PreAdvice_Dates_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    PreAdvice_Del_Date_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Delivery Date", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related to how program define Delivery Date for PreAdvice.", GUI_Level_ID=GUI_Level_ID)

    Fixed_Date_Section_Row = Widget_Section_Row(Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Fixed Date", Label_Size="Field_Label", Font_Size="Section_Separator")
    Pre_Fixed_Date_Row = WidgetRow_Date_Picker(Settings=Settings, Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Fixed Date", Date_format=Date_Format, Value=Pre_Fix_Date, placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Fixed_Options", "Fix_Date"], Button_ToolTip="Date Picker.", Picker_Always_on_Top=True, Validation="Date", GUI_Level_ID=GUI_Level_ID + 1)
 
    Interval_Date_Section_Row = Widget_Section_Row(Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Interval Date", Label_Size="Field_Label", Font_Size="Section_Separator")
    Pre_Random_From_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - From CD +", Value=Pre_Rand_From_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Random_Options", "From"], Validation="Integer")
    Pre_Random_To_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Date - To CD +", Value=Pre_Rand_To_Date, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Random_Options", "To"], Validation="Integer")

    Shift_Date_Section_Row = Widget_Section_Row(Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Delivery Date shift", Label_Size="Field_Label", Font_Size="Section_Separator")
    Pre_Del_Shift_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Delivery Date shift by", Value=Pre_Delivery_Shift, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Shift_Options", "Delivery_Date_Shift_by"], Validation="Integer")
    Pre_Gen_Shift_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Generation Date shift by", Value=Pre_Gen_Date_Shift, placeholder_text="Number of Days", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Shift_Options", "Generation_Date_Shift_by"], Validation="Integer")

    Option_Menu_Blocking_dict = CustomTkinter_Functions.OptionMenu_Blocking(Values=["Fixed", "Random", "Delivery Date Shift", "Prompt"], Freeze_fields=[[Pre_Random_From_Row, Pre_Random_To_Row, Pre_Del_Shift_Row, Pre_Gen_Shift_Row],[Pre_Fixed_Date_Row, Pre_Del_Shift_Row, Pre_Gen_Shift_Row],[Pre_Fixed_Date_Row, Pre_Random_From_Row, Pre_Random_To_Row],[Pre_Fixed_Date_Row, Pre_Random_From_Row, Pre_Random_To_Row, Pre_Del_Shift_Row, Pre_Gen_Shift_Row]])
    CON_Number_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=PreAdvice_Del_Date_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=PreAdvice_Dates_Method_Variable, Values=PreAdvice_Dates_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Delivery_Date", "Method"], Field_list=[Pre_Fixed_Date_Row, Pre_Random_From_Row, Pre_Random_To_Row, Pre_Del_Shift_Row, Pre_Gen_Shift_Row], Field_Blocking_dict=Option_Menu_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    PreAdvice_Del_Date_Widget.Add_row(Rows=[CON_Number_Row, Fixed_Date_Section_Row, Pre_Fixed_Date_Row, Interval_Date_Section_Row, Pre_Random_From_Row, Pre_Random_To_Row, Shift_Date_Section_Row, Pre_Del_Shift_Row, Pre_Gen_Shift_Row])

    return PreAdvice_Del_Date_Widget
