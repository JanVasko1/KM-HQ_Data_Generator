# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_CPDI as W_CPDI

def Page_CPDI(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_CPDI_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_CPDI_Work_Detail_Area.grid_propagate(flag=False)

    Frame_CPDI_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_CPDI_Work_Detail_Area, Frame_Size="Triple_size")

    Frame_Conf_Column_A = CTkFrame(master=Frame_CPDI_Scrollable_Area)
    Frame_Conf_Column_B = CTkFrame(master=Frame_CPDI_Scrollable_Area)

    # ------------------------- Widgets -------------------------#
    CPDI_General_Widget = W_CPDI.General(Settings=Settings, Configuration=Configuration, Frame=Frame_Conf_Column_A)

    # Build look of Widget
    Frame_CPDI_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_CPDI_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Conf_Column_A.pack(side="left", fill="both", expand=False, padx=0, pady=0)
    Frame_Conf_Column_B.pack(side="left", fill="both", expand=False, padx=0, pady=0)

    CPDI_General_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)