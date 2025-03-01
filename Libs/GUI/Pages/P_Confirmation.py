# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Confirmation as W_Confirmation

def Page_Confirmation(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    #------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Confirmation_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Confirmation_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Confirmation_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_PO = TabView.add("Purchase Order")
    Tab_PRO = TabView.add("Return Order")
    TabView.set("Purchase Order")

    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_PRO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Settings related to Confirmation document created because of Purchase Order.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PRO_ToolTip_But, message="Settings related to Confirmation document created because of Return Purchase Order.", ToolTip_Size="Normal")

    Frame_Conf_Column_A = CTkFrame(master=Tab_PO)
    Frame_Conf_Column_B = CTkFrame(master=Tab_PO)

    # ---------- Widgets ---------- #
    # Purchase Order
    PO_Number_Widget = W_Confirmation.PO_Number(Settings=Settings, Configuration=Configuration, Frame=Frame_Conf_Column_A)
    PO_Prices_Widget = W_Confirmation.PO_Prices(Settings=Settings, Configuration=Configuration, Frame=Frame_Conf_Column_A)
    PO_Currency_Widget = W_Confirmation.PO_Currency(Settings=Settings, Configuration=Configuration, Frame=Frame_Conf_Column_A)
    PO_Line_Flags_Widget = W_Confirmation.PO_Line_Flags(Settings=Settings, Configuration=Configuration, Frame=Frame_Conf_Column_A)
    PO_ATP_Widget = W_Confirmation.PO_ATP(Settings=Settings, Configuration=Configuration, Frame=Frame_Conf_Column_B)

    # ------------------------- Build look of Widget-------------------------#
    Frame_Confirmation_Work_Detail_Area.pack(side="top", fill="both", expand=False, padx=0, pady=0)
    TabView.grid(row=0, column=0, padx=5, pady=0, sticky="n")

    Frame_Conf_Column_A.pack(side="left", fill="both", expand=False, padx=0, pady=0)
    Frame_Conf_Column_B.pack(side="left", fill="both", expand=False, padx=0, pady=0)

    PO_Number_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Prices_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Currency_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Line_Flags_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_ATP_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)