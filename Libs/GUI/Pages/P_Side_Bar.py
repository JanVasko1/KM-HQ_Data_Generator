# Import Libraries
import time

from customtkinter import CTk, CTkFrame

import Libs.Data_Functions as Data_Functions
import Libs.Defaults_Lists as Defaults_Lists

import Libs.GUI.Elements as Elements

def Get_Side_Bar(Settings: dict, Configuration: dict, Documents: dict, window: CTk, Frame_Work_Area_Main: CTkFrame, Side_Bar_Frame: CTkFrame) -> None:
    Application = Defaults_Lists.Load_Application()
    Program_Version = Application["Application"]["Version"]

    Icon_Default_pady = 10
    Side_Bar_Top_pady = 100
    Side_Bar_Bottom_pady = 75
    
    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame: CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()

    def Show_Download_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Download as P_Download
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Top_pady, Icon_Default_pady), sticky="e")
        P_Download.Page_Download(Settings=Settings, Configuration=Configuration, window=window, Documents=Documents, Frame=Frame_Work_Area_Main)

    def Show_Confirmation_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Confirmation as P_Confirmation
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Confirmation.Page_Confirmation(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_CPDI_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_CPDI as P_CPDI
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_CPDI.Page_CPDI(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_PreAdvice_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_PreAdvice as P_PreAdvice
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_PreAdvice.Page_PreAdvice(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_Delivery_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Delivery as P_Delivery
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Delivery.Page_Delivery(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_Invoice_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Invoice as P_Invoice
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Invoice.Page_Invoice(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_IAL_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_IAL as P_IAL
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_IAL.Page_IAL(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Settings as P_Settings
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Settings.Page_Settings(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Exit_Program() -> None:
        # Delete Operational data from Settings
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Used"], Information="")
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Process_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Used"], Information="")
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Vendors_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Order", "Purchase_Order_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=[])
        window.quit()

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Logo
    Logo = Elements.Get_Custom_Image(Configuration=Configuration, Frame=Side_Bar_Frame, Image_Name="Company", postfix="png", width=70, heigh=50)

    # Page - Download
    Icon_Frame_Download = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="cpu", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=0))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Download, message="Process page", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Confirmation
    Icon_Frame_Confirmation = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-check", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Confirmation.configure(command = lambda: Show_Confirmation_Page(Active_Window = Active_Window, Side_Bar_Row=1))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Confirmation, message="Confirmation setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - CPDI
    Icon_Frame_CPDI = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="wrench", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_CPDI.configure(command = lambda: Show_CPDI_Page(Active_Window = Active_Window, Side_Bar_Row=2))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_CPDI, message="CPDI setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - PreAdvice
    Icon_Frame_PreAdvice = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="package-open", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_PreAdvice.configure(command = lambda: Show_PreAdvice_Page(Active_Window = Active_Window, Side_Bar_Row=3))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_PreAdvice, message="PreAdvice setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Delivery
    Icon_Frame_Delivery = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="package-check", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Delivery.configure(command = lambda: Show_Delivery_Page(Active_Window = Active_Window, Side_Bar_Row=4))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Delivery, message="Delivery setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Invoice
    Icon_Frame_Invoice = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-text", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Invoice.configure(command = lambda: Show_Invoice_Page(Active_Window = Active_Window, Side_Bar_Row=5))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Invoice, message="Invoice setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - IAL
    Icon_Frame_IAL = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="coins", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_IAL.configure(command = lambda: Show_IAL_Page(Active_Window = Active_Window, Side_Bar_Row=6))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_IAL, message="IAL setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=7))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Application settings page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
    Icon_Frame_Close.configure(command = lambda: Exit_Program())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Close, message="Close application.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Program Version
    Program_Version_text = Elements.Get_Label(Configuration=Configuration, Frame=Side_Bar_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
    Program_Version_text.configure(text=f"{Program_Version}")

    # Build look of Widget
    Logo.grid(row=0, column=0, padx=(0, 0), pady=(10, 0), sticky="n", columnspan=2)
    Active_Window.grid(row=1, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")

    Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Top_pady, Icon_Default_pady), sticky="w")
    Icon_Frame_Confirmation.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_CPDI.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_PreAdvice.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Delivery.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Invoice.grid(row=5, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_IAL.grid(row=6, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Settings.grid(row=7, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Close.grid(row=8, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Bottom_pady), sticky="w")
    Program_Version_text.grid(row=9, column=0, padx=(0, 0), pady=(0, 10), sticky="s", columnspan=2)

    # Initiate default window
    Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=0)

