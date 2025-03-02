# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

def Page_Delivery(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_Delivery_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Widgets -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Delivery_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_DEL = TabView.add("Delivery")
    TabView.set("Delivery")
    Tab_DEL_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_DEL_ToolTip_But, message="Delivery Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)


    # Build look of Widget
    Frame_Delivery_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)