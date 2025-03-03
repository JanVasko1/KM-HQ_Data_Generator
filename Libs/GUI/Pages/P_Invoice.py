# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Invoice as W_Invoice

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

    # ---------- Purchase Order ---------- #
    Frame_PO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    PO_INV_Number_Widget = W_Invoice.PO_INV_Number(Settings=Settings, Configuration=Configuration, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_Price_Currency_Widget = W_Invoice.PO_Price_Currency(Settings=Settings, Configuration=Configuration, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_Plant_Widget = W_Invoice.PO_Plant(Settings=Settings, Configuration=Configuration, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_Posting_Date_Widget = W_Invoice.PO_Posting_Date(Settings=Settings, Configuration=Configuration, Frame=Frame_PO_Column_B, GUI_Level_ID=2)
    PO_CountryOrigin_Widget = W_Invoice.PO_CountryOrigin(Settings=Settings, Configuration=Configuration, Frame=Frame_PO_Column_B, GUI_Level_ID=2)
    PO_Tariff_Widget = W_Invoice.PO_Tariff(Settings=Settings, Configuration=Configuration, Frame=Frame_PO_Column_B, GUI_Level_ID=2)

    # ---------- BackBone Billing ---------- #
    Frame_BB_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_BB_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # ---------- Purchase Return Order ---------- #
    Frame_PRO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PRO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # ------------------------- Build look of Widget-------------------------#
    Frame_Invoice_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_PO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PO_INV_Number_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Price_Currency_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Plant_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Posting_Date_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_CountryOrigin_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Tariff_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_BB_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_BB_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    Frame_PRO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PRO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)