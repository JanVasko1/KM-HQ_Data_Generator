# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements

def Page_Invoice(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    #------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_PO = TabView.add("Purchase Order")
    Tab_PO.pack_propagate(flag=False)
    Tab_PCM = TabView.add("Credit Memo")
    Tab_PCM.pack_propagate(flag=False)
    Tab_BB = TabView.add("BackBone Billing")
    Tab_BB.pack_propagate(flag=False)
    TabView.set("Purchase Order")

    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_PCM_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_BB_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Settings related to Invoice document created because of Purchase Order.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PCM_ToolTip_But, message="Settings related to Credit Memo document created because of Return Purchase Order.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_ToolTip_But, message="Settings related to BackBone Billing document, send from BEU as Stand Alone Invoice for services.", ToolTip_Size="Normal")


    # ---------- Widgets ---------- #

    # ------------------------- Build look of Widget-------------------------#
    Frame_Download_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.grid(row=0, column=0, padx=5, pady=0, sticky="n")