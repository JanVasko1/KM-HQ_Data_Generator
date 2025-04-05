# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar

import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row

def General(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    CPDI_Delivery_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Delivery_select"]["Method"]
    CPDI_Delivery_Method_List = list(Settings["0"]["HQ_Data_Handler"]["CPDI"]["Delivery_select"]["Methods_List"])
    Fixed_Delivery = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Delivery_select"]["Fixed_Options"]["Fix_Delivery"]

    CPDI_Level_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Level_Provided"]["Method"]
    CPDI_Level_Method_List = list(Settings["0"]["HQ_Data_Handler"]["CPDI"]["Level_Provided"]["Methods_List"])
    Fixed_CPDI_Level = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Level_Provided"]["Fixed_Options"]["Fix_Level"]

    CPDI_Status_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Status"]["Method"]
    CPDI_Status_Method_List = list(Settings["0"]["HQ_Data_Handler"]["CPDI"]["Status"]["Methods_List"])
    Fixed_CPDI_Status = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Status"]["Fixed_Options"]["Fix_Status"]

    CPDI_Delivery_Method_Variable = StringVar(master=Frame, value=CPDI_Delivery_Method, name="CPDI_Delivery_Method_Variable")
    CPDI_Level_Method_Variable = StringVar(master=Frame, value=CPDI_Level_Method, name="CPDI_Level_Method_Variable")
    CPDI_Status_Method_Variable = StringVar(master=Frame, value=CPDI_Status_Method, name="CPDI_Status_Method_Variable")

    # ------------------------- Main Functions -------------------------#
    # Widget
    CPDI_Method_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Generate", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related what CPDI status should be created.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Delivery_Section_Row = Widget_Section_Row(Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Delivery", Label_Size="Field_Label", Font_Size="Section_Separator")
    Fixed_Delivery_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Delivery", Value=Fixed_Delivery, placeholder_text="Manual Delivery number", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Delivery_select", "Fixed_Options", "Fix_Delivery"])
    CPDI_Delivery_Method_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "All Deliveries", "Prompt"], Freeze_fields=[[],[Fixed_Delivery_Row],[Fixed_Delivery_Row]])
    CPDI_Delivery_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=CPDI_Delivery_Method_Variable, Values=CPDI_Delivery_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Delivery_select", "Method"], Field_list=[Fixed_Delivery_Row], Field_Blocking_dict=CPDI_Delivery_Method_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Level_Section_Row = Widget_Section_Row(Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Level Provided", Label_Size="Field_Label", Font_Size="Section_Separator")
    Fixed_Level_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Level", Value=Fixed_CPDI_Level, placeholder_text="Manual Level provided", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Level_Provided", "Fixed_Options", "Fix_Level"])
    CPDI_Level_Method_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "Purchase Order", "Random", "Prompt"], Freeze_fields=[[],[Fixed_Level_Row],[Fixed_Level_Row],[Fixed_Level_Row]])
    CPDI_Level_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=CPDI_Level_Method_Variable, Values=CPDI_Level_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Level_Provided", "Method"], Field_list=[Fixed_Level_Row], Field_Blocking_dict=CPDI_Level_Method_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Status_Section_Row = Widget_Section_Row(Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Status", Label_Size="Field_Label", Font_Size="Section_Separator")
    Fixed_Status_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Fixed Status", Value=Fixed_CPDI_Status, placeholder_text="Manual Status", placeholder_text_color="#949A9F", Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Status", "Fixed_Options", "Fix_Status"])
    CPDI_Status_Method_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["Fixed", "All Statuses", "Prompt"], Freeze_fields=[[],[Fixed_Status_Row],[Fixed_Status_Row]])
    CPDI_Statius_Method_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=CPDI_Method_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Method", Variable=CPDI_Status_Method_Variable, Values=CPDI_Status_Method_List, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Status", "Method"], Field_list=[Fixed_Status_Row], Field_Blocking_dict=CPDI_Status_Method_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    CPDI_Method_Widget.Add_row(Rows=[Delivery_Section_Row, CPDI_Delivery_Method_Row, Fixed_Delivery_Row, Level_Section_Row, CPDI_Level_Method_Row, Fixed_Level_Row, Status_Section_Row, CPDI_Statius_Method_Row, Fixed_Status_Row])

    return CPDI_Method_Widget

