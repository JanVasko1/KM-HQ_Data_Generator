# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Widgets.W_Settings as Settings_Widgets
import Libs.GUI.Elements as Elements

def Page_Settings(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame):
    # ------------------------- Main Functions -------------------------#
    Frame_Settings_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Settings_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_Gen = TabView.add("General")
    TabView.set("General")

    Tab_App_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_App_ToolTip_But, message="Application appearance Setup.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- Appearance ---------- #
    Frame_Tab_Gen_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Appearance_Widget = Settings_Widgets.Settings_General_Color(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_A, GUI_Level_ID=2)
    Program_User_Access_Widget = Settings_Widgets.Settings_User_Access(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_B, GUI_Level_ID=2)

    # Build look of Widget
    Frame_Settings_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Tab_Gen_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Gen_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Appearance_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Program_User_Access_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)