# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_PreAdvice as W_PreAdvice

def Page_PreAdvice(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_PreAdvice_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Widgets -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_PreAdvice_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    Tab_PRE = TabView.add("PreAdvice")
    TabView.set("PreAdvice")
    Tab_PRE_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PRE_ToolTip_But, message="PreAdvice Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PRE, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Pre_Delivery_Date_Widget = W_PreAdvice.Delivery_Date(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, GUI_Level_ID=2)

    # Build look of Widget
    Frame_PreAdvice_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Pre_Delivery_Date_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)