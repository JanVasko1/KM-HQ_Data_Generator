# Import Libraries
import time

from customtkinter import CTk, CTkFrame

import Libs.GUI.Pages.P_Download as P_Download
import Libs.GUI.Pages.P_Confirmation as P_Confirmation
import Libs.GUI.Pages.P_CPDI as P_CPDI
import Libs.GUI.Pages.P_PreAdvice as P_PreAdvice
import Libs.GUI.Pages.P_Delivery as P_Delivery
import Libs.GUI.Pages.P_Invoice as P_Invoice
import Libs.GUI.Pages.P_IAL as P_IAL
import Libs.GUI.Pages.P_Settings as P_Settings

import Libs.Data_Functions as Data_Functions
import Libs.Defaults_Lists as Defaults_Lists

import Libs.GUI.Elements as Elements


class SidebarApp:
    def __init__(self, Side_Bar_Frame: CTkFrame, Settings: dict, Configuration: dict, Documents: dict, window: CTk, Frame_Work_Area_Main: CTkFrame):
        self.Side_Bar_Frame = Side_Bar_Frame
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.window = window
        self.Frame_Work_Area_Main = Frame_Work_Area_Main

        # Application
        self.Application = Defaults_Lists.Load_Application()
        self.Program_Version = self.Application["Application"]["Version"]
            
        # Add buttons to the sidebar
        self.names = ["Download", 
                        "Confirmation", 
                        "CPDI", 
                        "PreAdvice", 
                        "Delivery", 
                        "Invoice", 
                        "IAL", 
                        "Settings",
                        "Close"]
        
        self.icons = ["cpu", 
                      "file-check", 
                      "wrench", 
                      "package-check", 
                      "truck", 
                      "file-text",
                      "coins",
                      "settings",
                      "power"]
        
        self.messages = ["Process page.", 
                        "Confirmation setup page", 
                        "CPDI setup page.", 
                        "PreAdvice setup page.", 
                        "Delivery setup page.", 
                        "Invoice setup page.",
                        "IAL setup page.",
                        "Application settings page.",
                        "Close application."]
        
        # Icons
        self.Icon_Default_pady = 10
        self.Side_Bar_Top_pady = 40
        self.Side_Bar_Bottom_pady = 80
        self.Icon_count = len(self.names)

        # Active button tracker
        self.active_button = "Download"
        
        # Build SideBar
        self.create_company_logo()
        self.create_sidebar_buttons()
        self.create_Application_version()
        self.Show_Download_Page()

    def create_company_logo(self):
        Logo = Elements.Get_Custom_Image(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Image_Name="Company", postfix="png", width=70, heigh=50)
        Logo.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    def create_sidebar_buttons(self):
        self.Active_Window = 0
        self.buttons = []
        for button_index, button_name in enumerate(self.names):
            if button_name == "Close":
                # TurnOff wit red color
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
            elif  button_name == self.active_button:
                # Initiate Active Button
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_Active", Button_Size="Picture_Transparent")
            else:
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
            button.configure(command = self.create_command(button_index=button_index, button_name=button_name))
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=button, message=self.messages[button_index], ToolTip_Size="Normal", GUI_Level_ID=0)

            # Place button 
            if button_index == 0:
                # First Icon
                button.pack(side="top", fill="none", expand=False, padx=5, pady=(self.Side_Bar_Top_pady, self.Icon_Default_pady))
            elif (button_index > 0) and (button_index < self.Icon_count - 1):
                # Middle Icons
                button.pack(side="top", fill="none", expand=False, padx=5, pady=self.Icon_Default_pady)
            else:
                # Last Icon
                button.pack(side="top", fill="none", expand=False, padx=5, pady=(self.Icon_Default_pady, self.Side_Bar_Bottom_pady))
            self.buttons.append(button)

    def create_Application_version(self):
        Program_Version_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
        Program_Version_text.configure(text=f"{self.Program_Version}", text_color = "#efefef")
        Program_Version_text.pack(side="top", fill="none", expand=False, padx=5, pady=(0, 10))

    def create_command(self, button_index, button_name):
        """Return a command function for the given page."""
        def command():
            self.change_page(button_index=button_index, button_name=button_name)
        return command

    def change_page(self, button_index, button_name):
        # Reset the color of all buttons
        for button_index_intern, button in enumerate(self.buttons):
            if button_index_intern < self.Icon_count - 1:
                button.configure(image=Elements.Get_CTk_Icon(Configuration=self.Configuration, Icon_Name=self.icons[button_index_intern], Icon_Size="Side_Bar_regular"))

        # Mark Active button
        self.buttons[button_index].configure(image=Elements.Get_CTk_Icon(Configuration=self.Configuration, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_Active"))

        if button_name == "Download":
            self.Show_Download_Page()
        elif button_name == "Confirmation":
            self.Show_Confirmation_Page()
        elif button_name == "CPDI":
            self.Show_CPDI_Page()
        elif button_name == "PreAdvice":
            self.Show_PreAdvice_Page()
        elif button_name == "Delivery":
            self.Show_Delivery_Page()
        elif button_name == "Invoice":
            self.Show_Invoice_Page()
        elif button_name == "IAL":
            self.Show_IAL_Page()
        elif button_name == "Settings":
            self.Show_Settings_Page()
        elif button_name == "Close":
            self.Show_Close_Page()
        else:
            pass

    def Clear_Frame(self, Pre_Working_Frame: CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()

    def Show_Download_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Download.Page_Download(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Documents=self.Documents, Frame=self.Frame_Work_Area_Main)

    def Show_Confirmation_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Confirmation.Page_Confirmation(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_CPDI_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_CPDI.Page_CPDI(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_PreAdvice_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_PreAdvice.Page_PreAdvice(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_Delivery_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Delivery.Page_Delivery(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
    
    def Show_Invoice_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Invoice.Page_Invoice(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_IAL_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_IAL.Page_IAL(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        
    def Show_Settings_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Settings.Page_Settings(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)
        

    def Show_Close_Page(self) -> None:
        # Delete Operational data from Settings
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=self.Documents, window=self.window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Used"], Information="")
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=self.Documents, window=self.window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Process_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=self.Documents, window=self.window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Used"], Information="")
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=self.Documents, window=self.window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Vendors_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=self.Documents, window=self.window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Order", "Purchase_Order_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=self.Documents, window=self.window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=[])
        self.window.quit()
