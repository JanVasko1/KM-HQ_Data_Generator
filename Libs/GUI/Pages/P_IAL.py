# Import Libraries
from customtkinter import CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

def Page_IAL(Settings: dict, Configuration: dict, Frame: CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_IAL_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Widgets -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_IAL_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_IAL = TabView.add("IAL")
    TabView.set("IAL")
    Tab_IAL_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_IAL_ToolTip_But, message="IAL Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_IAL, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_IAL, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)


    # Build look of Widget
    Frame_IAL_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)