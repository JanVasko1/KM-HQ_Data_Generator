# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements

def Page_PreAdvice(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_PreAdvice_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_PreAdvice_Work_Detail_Area.grid_propagate(flag=False)

    Frame_PreAdvice_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_PreAdvice_Work_Detail_Area, Frame_Size="Triple_size")

    Frame_Conf_Column_A = CTkFrame(master=Frame_PreAdvice_Scrollable_Area)
    Frame_Conf_Column_B = CTkFrame(master=Frame_PreAdvice_Scrollable_Area)

    # ------------------------- Widgets -------------------------#


    # Build look of Widget
    Frame_PreAdvice_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_PreAdvice_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Conf_Column_A.pack(side="left", fill="both", expand=False, padx=0, pady=0)
    Frame_Conf_Column_B.pack(side="left", fill="both", expand=False, padx=0, pady=0)
