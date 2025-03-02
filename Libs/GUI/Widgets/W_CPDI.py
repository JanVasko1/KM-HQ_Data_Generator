# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements


def General(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    CPDI_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Method"]
    CPDI_Method_List = list(Settings["0"]["HQ_Data_Handler"]["CPDI"]["Methods_List"])

    CPDI_Method_Variable = StringVar(master=Frame, value=CPDI_Method, name="CPDI_Method_Variable")
    # ------------------------- Local Functions -------------------------#
    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Generate", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Settings related what CPDI status should be created.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Number Method
    CPDI_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Method", Field_Type="Input_OptionMenu") 
    CPDI_Frame_Var = CPDI_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    CPDI_Frame_Var.configure(variable=CPDI_Method_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CPDI_Frame_Var, values=CPDI_Method_List, command=lambda CPDI_Frame_Var: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=CPDI_Method_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Method"], Information=CPDI_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main