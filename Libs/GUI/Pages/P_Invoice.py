# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Invoice as W_Invoice

def Page_Invoice(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame):
    #------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Invoice_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)
    Frame_Invoice_Work_Area_Main.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Invoice_Work_Area_Main, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_PO = TabView.add("Purchase Order")
    Tab_BB_A = TabView.add("BackBone Billing")
    Tab_BB_B = TabView.add("BackBone Billing - Additional")
    Tab_BB_C = TabView.add("BackBone Billing - IAL")
    Tab_PCM = TabView.add("Credit Memo")
    TabView.set("Purchase Order")

    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_BB_A_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_BB_B_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Tab_BB_C_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton4"]
    Tab_PCM_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton5"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Settings related to Invoice document created because of Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_A_ToolTip_But, message="Settings related to BackBone Billing document, send from BEU as Stand Alone Invoice for services.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_B_ToolTip_But, message="Settings related to BackBone Billing document, send from BEU as Stand Alone Invoice for services.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_C_ToolTip_But, message="Settings related to BackBone Billing document, IAL.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PCM_ToolTip_But, message="Settings related to Credit Memo document created because of Return Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- Purchase Order ---------- #
    Frame_PO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PO_Column_A.pack_propagate(flag=False)
    Frame_PO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PO_Column_B.pack_propagate(flag=False)

    PO_INV_Number_Widget = W_Invoice.PO_INV_Number(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_INV_Price_Widget = W_Invoice.PO_Price_Currency(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_INV_Plant_Widget = W_Invoice.PO_Plant(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_A, GUI_Level_ID=2)
    PO_INV_Date_Widget = W_Invoice.PO_Invoice_Date(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_B, GUI_Level_ID=2)
    PO_INV_Origin_Widget = W_Invoice.PO_CountryOrigin(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_B, GUI_Level_ID=2)
    PO_INV_Tariff_Widget = W_Invoice.PO_Tariff(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PO_Column_B, GUI_Level_ID=2)

    # ---------- BackBone Billing ---------- #
    Frame_BB_A_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_BB_A, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_BB_A_Column_A.pack_propagate(flag=False)
    Frame_BB_A_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_BB_A, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_BB_A_Column_B.pack_propagate(flag=False)

    BB_INV_Number_Widget = W_Invoice.BB_INV_Number(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_A_Column_A, GUI_Level_ID=2)
    BB_INV_Items_Widget = W_Invoice.BB_Items(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_A_Column_A, GUI_Level_ID=2)
    BB_INV_Price_Widget = W_Invoice.BB_Price_Currency(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_A_Column_A, GUI_Level_ID=2)
    BB_INV_Qty_Widget = W_Invoice.BB_Quantity(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_A_Column_B, GUI_Level_ID=2)
    BB_INV_Date_Widget = W_Invoice.BB_Posting_Date(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_A_Column_B, GUI_Level_ID=2)
    BB_INV_Reference_Widget = W_Invoice.BB_Order_reference(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_A_Column_B, GUI_Level_ID=2)
    

    Frame_BB_B_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_BB_B, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_BB_B_Column_A.pack_propagate(flag=False)

    BB_INV_Plant_Widget = W_Invoice.BB_Plant(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_B_Column_A, GUI_Level_ID=2)
    BB_INV_Origin_Widget = W_Invoice.BB_CountryOrigin(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_B_Column_A, GUI_Level_ID=2)
    BB_INV_Tariff_Widget = W_Invoice.BB_Tariff(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_BB_B_Column_A, GUI_Level_ID=2)

    # ---------- IAL ---------- #
    Frame_IAL_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_BB_C, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_IAL_Column_A.pack_propagate(flag=False)
    Frame_IAL_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_BB_C, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_IAL_Column_B.pack_propagate(flag=False)


    # ---------- Purchase Return Order ---------- #
    Frame_PRO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PCM, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PRO_Column_A.pack_propagate(flag=False)
    Frame_PRO_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_PCM, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_PRO_Column_B.pack_propagate(flag=False)

    PRO_INV_Number_Widget = W_Invoice.PRO_INV_Number(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PRO_Column_A, GUI_Level_ID=2)
    PRO_INV_Price_Widget = W_Invoice.PRO_Price_Currency(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PRO_Column_A, GUI_Level_ID=2)
    PRO_INV_Plant_Widget = W_Invoice.PRO_Plant(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PRO_Column_A, GUI_Level_ID=2)
    PRO_INV_Date_Widget = W_Invoice.PRO_Invoice_Date(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PRO_Column_B, GUI_Level_ID=2)
    PRO_INV_Origin_Widget = W_Invoice.PRO_CountryOrigin(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PRO_Column_B, GUI_Level_ID=2)
    PRO_INV_Tariff_Widget = W_Invoice.PRO_Tariff(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_PRO_Column_B, GUI_Level_ID=2)


    # ------------------------- Build look of Widget-------------------------#
    Frame_Invoice_Work_Area_Main.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_PO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PO_INV_Number_Widget.Show()
    PO_INV_Price_Widget.Show()
    PO_INV_Plant_Widget.Show()
    PO_INV_Date_Widget.Show()
    PO_INV_Origin_Widget.Show()
    PO_INV_Tariff_Widget.Show()

    Frame_BB_A_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_BB_A_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    BB_INV_Number_Widget.Show()
    BB_INV_Items_Widget.Show()
    BB_INV_Price_Widget.Show()
    BB_INV_Qty_Widget.Show()
    BB_INV_Date_Widget.Show()
    BB_INV_Reference_Widget.Show()

    Frame_BB_B_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    BB_INV_Plant_Widget.Show()
    BB_INV_Origin_Widget.Show()
    BB_INV_Tariff_Widget.Show()
    
    Frame_IAL_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_IAL_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    Frame_PRO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_PRO_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    PRO_INV_Number_Widget.Show()
    PRO_INV_Price_Widget.Show()
    PRO_INV_Plant_Widget.Show()
    PRO_INV_Date_Widget.Show()
    PRO_INV_Origin_Widget.Show()
    PRO_INV_Tariff_Widget.Show()