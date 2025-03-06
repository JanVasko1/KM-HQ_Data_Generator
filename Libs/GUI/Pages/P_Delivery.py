# Import Libraries
from customtkinter import CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Delivery as W_Delivery

def Page_Delivery(Settings: dict, Configuration: dict, Frame: CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_Delivery_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Widgets -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Delivery_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_DEL = TabView.add("Delivery")
    Tab_T_P = TabView.add("Tracking - Packages")
    Tab_T_O = TabView.add("Tracking - Others")
    TabView.set("Delivery")
    Tab_DEL_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_T_P_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_T_O_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_DEL_ToolTip_But, message="Base delivery Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_T_P_ToolTip_But, message="Packages Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_T_O_ToolTip_But, message="EXIDV2, Bill of Landing Settings.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # ---------- Delivery ---------- #
    Frame_Tab_DEL_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_DEL_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    PO_Number_Widget = W_Delivery.DEL_Number(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_DEL_Column_A, GUI_Level_ID=2)
    PO_Serial_Numbers_Widget = W_Delivery.Serial_Numbers(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_DEL_Column_A, GUI_Level_ID=2)
    PO_Delivery_Date_Widget = W_Delivery.Delivery_Date(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_DEL_Column_A, GUI_Level_ID=2)
    
    PO_Count_Widget = W_Delivery.DEL_Count(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_DEL_Column_B, GUI_Level_ID=2)
    PO_Carrier_Widget = W_Delivery.Carrier_ID(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_DEL_Column_B, GUI_Level_ID=2)
    Ship_Method_Widget = W_Delivery.Shipment_Method(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_DEL_Column_B, GUI_Level_ID=2)
    
    # ---------- Tracking - Packages ---------- #
    Frame_Tab_T_P_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_T_P, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_T_P_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_T_P, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Pack_Numbers_Widget = W_Delivery.Packages_Numbers(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_T_P_Column_A, GUI_Level_ID=2)
    Pack_Items_Widget = W_Delivery.Packages_Items(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_T_P_Column_A, GUI_Level_ID=2)
    Pack_Plants_Widget = W_Delivery.Packages_Plants(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_T_P_Column_B, GUI_Level_ID=2)
    Pack_UOM_Widget = W_Delivery.Packages_UOM(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_T_P_Column_B, GUI_Level_ID=2)

    # ---------- Tracking - Others ---------- #
    Frame_Tab_T_O_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_T_O, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_T_O_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_T_O, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    EXIDV2_Widget = W_Delivery.EXIDV2(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_T_O_Column_A, GUI_Level_ID=2)
    BillOfLanding_Widget = W_Delivery.BillOfLanding(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_T_O_Column_B, GUI_Level_ID=2)
    
    # Build look of Widget
    Frame_Delivery_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Tab_DEL_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_DEL_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PO_Number_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Serial_Numbers_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Delivery_Date_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Count_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Carrier_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Ship_Method_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    Frame_Tab_T_P_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_T_P_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Pack_Numbers_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Pack_Items_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Pack_Plants_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Pack_UOM_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_Tab_T_O_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_T_O_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    EXIDV2_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    BillOfLanding_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    