# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Widgets.W_Settings as Settings_Widgets
import Libs.GUI.Elements as Elements

def Page_Settings(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#
    Frame_Settings_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Settings_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Settings_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_App = TabView.add("Appearance")
    Tab_App.pack_propagate(flag=False)
    Tab_Usr = TabView.add("User")
    Tab_Usr.pack_propagate(flag=False)
    TabView.set("Appearance")

    Tab_App_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Usr_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_App_ToolTip_But, message="Application appearance Setup.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Usr_ToolTip_But, message="Setup related to Current User date.", ToolTip_Size="Normal")

    # General
    Theme_Widget = Settings_Widgets.Settings_General_Theme(Settings=Settings, Configuration=Configuration, Frame=Tab_App, window=window)
    Color_Palette_Widget = Settings_Widgets.Settings_General_Color(Settings=Settings, Configuration=Configuration, Frame=Tab_App)

    # User Page
    Program_User_Access_Widget = Settings_Widgets.Settings_User_Access(Settings=Settings, Configuration=Configuration, Frame=Tab_Usr)

    # Build look of Widget
    Frame_Settings_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    TabView.grid(row=0, column=0, padx=5, pady=0, sticky="n")

    Theme_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Color_Palette_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

    Program_User_Access_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")