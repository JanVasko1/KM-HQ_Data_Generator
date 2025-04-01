# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_CPDI as W_CPDI

def Page_CPDI(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_CPDI_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Widgets -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_CPDI_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_CPDI = TabView.add("CPDI")
    TabView.set("CPDI")
    Tab_CPDI_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_CPDI_ToolTip_But, message="CPDI Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_CPDI, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Column_A.pack_propagate(flag=False)

    CPDI_Method_Widget = W_CPDI.General(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Column_A, GUI_Level_ID=2)

    # Build look of Widget
    Frame_CPDI_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    CPDI_Method_Widget.Show()