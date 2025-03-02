# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements

def Page_Invoice(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    #------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Invoice_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)
    Frame_Invoice_Work_Area_Main.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Invoice_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_PO = TabView.add("Purchase Order")
    Tab_BB = TabView.add("BackBone Billing")
    Tab_PCM = TabView.add("Credit Memo")
    TabView.set("Purchase Order")

    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_BB_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_PCM_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Settings related to Invoice document created because of Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_ToolTip_But, message="Settings related to BackBone Billing document, send from BEU as Stand Alone Invoice for services.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PCM_ToolTip_But, message="Settings related to Credit Memo document created because of Return Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- Widgets ---------- #
    # Purchase Order
    Frame_PO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # Purchase Order
    Frame_BB_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_BB_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # Purchase Order
    Frame_PRO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PRO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # ------------------------- Build look of Widget-------------------------#
    Frame_Invoice_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_PO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    Frame_BB_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_BB_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    Frame_PRO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PRO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)