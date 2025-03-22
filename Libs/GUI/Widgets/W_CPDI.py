# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, CTkEntry

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

def General(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
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
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Generate", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related what CPDI status should be created.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Delivery", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Delivery MEthod
    CPDI_Delivery_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    CPDI_Delivery_Frame_Var = CPDI_Delivery_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    CPDI_Delivery_Frame_Var.configure(variable=CPDI_Delivery_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CPDI_Delivery_Frame_Var, values=CPDI_Delivery_Method_List, command=lambda CPDI_Delivery_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=CPDI_Delivery_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Delivery_select", "Method"], Information=CPDI_Delivery_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Delivery
    Fixed_Delivery_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Delivery", Field_Type="Input_Normal") 
    Fixed_Delivery_Frame_Var = Fixed_Delivery_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Delivery_Frame_Var.configure(placeholder_text="Manual Delivery", placeholder_text_color="#949A9F")
    Fixed_Delivery_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Delivery_select", "Fixed_Options", "Fix_Delivery"], Information=Fixed_Delivery_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Fixed_Delivery_Frame_Var, Value=Fixed_Delivery)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Level Provided", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field -Level Method
    CPDI_Level_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    CPDI_Level_Frame_Var = CPDI_Level_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    CPDI_Level_Frame_Var.configure(variable=CPDI_Level_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CPDI_Level_Frame_Var, values=CPDI_Level_Method_List, command=lambda CPDI_Level_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=CPDI_Level_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Level_Provided", "Method"], Information=CPDI_Level_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Level
    Fixed_Level_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Level", Field_Type="Input_Normal") 
    Fixed_Level_Frame_Var = Fixed_Level_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Level_Frame_Var.configure(placeholder_text="Manual Level provided", placeholder_text_color="#949A9F")
    Fixed_Level_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Level_Provided", "Fixed_Options", "Fix_Level"], Information=Fixed_Level_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Fixed_Level_Frame_Var, Value=Fixed_CPDI_Level)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Status", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Number Method
    CPDI_Status_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    CPDI_Status_Frame_Var = CPDI_Status_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    CPDI_Status_Frame_Var.configure(variable=CPDI_Status_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CPDI_Status_Frame_Var, values=CPDI_Status_Method_List, command=lambda CPDI_Status_Frame_Var: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=CPDI_Status_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Status", "Method"], Information=CPDI_Status_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Field - Fixed Delivery
    Fixed_Status_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Fixed Status", Field_Type="Input_Normal") 
    Fixed_Status_Frame_Var = Fixed_Status_Frame.children["!ctkframe3"].children["!ctkentry"]
    Fixed_Status_Frame_Var.configure(placeholder_text="Manual Delivery", placeholder_text_color="#949A9F")
    Fixed_Status_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Status", "Fixed_Options", "Fix_Status"], Information=Fixed_Status_Frame_Var.get()))
    Data_Functions.Entry_field_Insert(Field=Fixed_Status_Frame_Var, Value=Fixed_CPDI_Status)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main