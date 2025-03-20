# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Confirmation as W_Confirmation

def Page_Confirmation(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame):
    #------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Confirmation_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # ------------------------- Work Area -------------------------#
    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Confirmation_Work_Detail_Area, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_PO = TabView.add("Purchase Order")
    Tab_Free = TabView.add("Purchase Order - Free of Charge")
    Tab_ATP = TabView.add("Purchase Order - ATP")
    Tab_PRO = TabView.add("Return Order")
    TabView.set("Purchase Order")

    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_FREE_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_PRO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Settings related to Confirmation document created because of Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_FREE_ToolTip_But, message="Application Manual Free of Charge in case that are not downloadable from Business Central", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PRO_ToolTip_But, message="Settings related to Confirmation document created because of Return Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- Purchase Order ---------- #
    Frame_PO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    
    PO_Number_Widget = W_Confirmation.PO_CON_Number(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_Currency_Widget = W_Confirmation.PO_Price_Currency(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_Unit_of_Measure_Widget = W_Confirmation.PO_Unit_of_Measure(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_Generation_Date_Widget = W_Confirmation.PO_Generation_Date(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_B, GUI_Level_ID=2)
    PO_Line_Flags_Widget = W_Confirmation.PO_Line_Flags(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_B, GUI_Level_ID=2)

    # ---------- Purchase Order Free Of Charge ---------- #
    Frame_FREE_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Free, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_FREE_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Free, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    PO_Items_Free_Method_Widget = W_Confirmation.PO_Items_Free_Method(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_FREE_Column_A, GUI_Level_ID=2)
    PO_Items_Free_Cable_Widget = W_Confirmation.PO_Items_Free_Cable(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_FREE_Column_A, GUI_Level_ID=2)
    PO_Items_Free_Documentation_Widget = W_Confirmation.PO_Items_Free_Documentation(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_FREE_Column_A, GUI_Level_ID=2)
    PO_Items_Free_Face_Sheet_Widget = W_Confirmation.PO_Items_Free_Face_Sheet(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_FREE_Column_B, GUI_Level_ID=2)

    # ---------- Purchase Order ATP ---------- #
    Frame_ATP_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_ATP, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_ATP_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_ATP, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    PO_ATP_General_Widget = W_Confirmation.PO_ATP_General(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_ATP_Column_A, GUI_Level_ID=2)
    PO_ATP_Quantity_Distribution_Widget = W_Confirmation.PO_ATP_Quantity_Distribution(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_ATP_Column_A, GUI_Level_ID=2)
    PO_ATP_Fixed_Dates_Widget = W_Confirmation.PO_ATP_Fixed_Dates(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_ATP_Column_B, GUI_Level_ID=2)
    PO_ATP_Interval_Dates_Widget = W_Confirmation.PO_ATP_Interval_Dates(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_ATP_Column_B, GUI_Level_ID=2)

    # ---------- Purchase Return Order ---------- #
    Frame_PRO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PRO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PRO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PRO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    
    # ------------------------- Build look of Widget-------------------------#
    Frame_Confirmation_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_PO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PO_Number_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Currency_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Unit_of_Measure_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Generation_Date_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Line_Flags_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    Frame_FREE_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_FREE_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PO_Items_Free_Method_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Items_Free_Cable_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Items_Free_Documentation_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Items_Free_Face_Sheet_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_ATP_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_ATP_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PO_ATP_General_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_ATP_Quantity_Distribution_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_ATP_Fixed_Dates_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_ATP_Interval_Dates_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_PRO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PRO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
