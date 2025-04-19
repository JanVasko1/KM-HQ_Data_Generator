# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Delivery as W_Delivery

def Page_Delivery(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_Delivery_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Widgets -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Delivery_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_DEL1 = TabView.add("Delivery - 1")
    Tab_DEL2 = TabView.add("Delivery - 2")
    Tab_T_P = TabView.add("Tracking - Packages")
    TabView.set("Delivery - 1")
    Tab_DEL1_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_DEL2_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_T_P_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_DEL1_ToolTip_But, message="Base delivery Settings.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_DEL2_ToolTip_But, message="Base delivery Settings.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_T_P_ToolTip_But, message="Packages Settings.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- Delivery - 1 ---------- #
    Frame_Tab_DEL1_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL1, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_DEL1_Column_A.pack_propagate(flag=False)
    Frame_Tab_DEL1_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL1, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_DEL1_Column_B.pack_propagate(flag=False)

    Del_Count_Widget = W_Delivery.DEL_Count(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL1_Column_A, GUI_Level_ID=2)
    Del_Number_Widget = W_Delivery.DEL_Number(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL1_Column_A, GUI_Level_ID=2)

    Del_Items_Widget = W_Delivery.Item_Delivery_Assignment(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL1_Column_B, GUI_Level_ID=2)
    Del_Dates_Widget = W_Delivery.Delivery_Date(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL1_Column_B, GUI_Level_ID=2)
    
    # ---------- Delivery - 2 ---------- #
    Frame_Tab_DEL2_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL2, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_DEL2_Column_A.pack_propagate(flag=False)
    Frame_Tab_DEL2_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_DEL2, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_DEL2_Column_B.pack_propagate(flag=False)

    Del_SN_Widget = W_Delivery.Serial_Numbers(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL2_Column_A, GUI_Level_ID=2)
    Del_Ship_Method_Widget = W_Delivery.Shipment_Method(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL2_Column_A, GUI_Level_ID=2)
    
    Del_Carrier_Widget = W_Delivery.Carrier_ID(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL2_Column_B, GUI_Level_ID=2)
    Del_Bill_Land_Widget = W_Delivery.BillOfLanding(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_DEL2_Column_B, GUI_Level_ID=2)

    # ---------- Tracking - Packages ---------- #
    Frame_Tab_T_P_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_T_P, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_T_P_Column_A.pack_propagate(flag=False)
    Frame_Tab_T_P_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_T_P, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_T_P_Column_B.pack_propagate(flag=False)

    Del_PACK_Num_Widget = W_Delivery.Packages_Numbers(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_T_P_Column_A, GUI_Level_ID=2)
    Del_PACK_EXIDV_Widget = W_Delivery.EXIDV2(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_T_P_Column_A, GUI_Level_ID=2)
    
    Del_PACK_UoM_Widget = W_Delivery.Packages_UOM(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_T_P_Column_B, GUI_Level_ID=2)
    Del_PACK_Plant_Widget = W_Delivery.Packages_Plants(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_T_P_Column_B, GUI_Level_ID=2)
    
    # Build look of Widget
    Frame_Delivery_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Tab_DEL1_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_DEL1_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Del_Count_Widget.Show()
    Del_Number_Widget.Show()
    Del_Items_Widget.Show()
    Del_Dates_Widget.Show()

    Frame_Tab_DEL2_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_DEL2_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Del_SN_Widget.Show()
    Del_Ship_Method_Widget.Show()
    Del_Carrier_Widget.Show()
    Del_Bill_Land_Widget.Show()

    Frame_Tab_T_P_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_T_P_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Del_PACK_Num_Widget.Show()
    Del_PACK_EXIDV_Widget.Show()
    Del_PACK_UoM_Widget.Show()
    Del_PACK_Plant_Widget.Show()
