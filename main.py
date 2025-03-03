# BUG --> from some reason the null value appeare in TEmpalte and TEmplate list?
# BUG --> Tool Tip for Import Windows is not on Top
# TODO --> implementovat nejaký Counter kolik toho bylo vytvořeno a při zavárání aplikace aktualizovat něco na sharepointu / per NOC (aby bylo vidět kolik se toho skrz aplikaci udělalo)

# Import Libraries
import os
import json
import time
from glob import glob

import pywinstyles
from customtkinter import CTk, CTkFrame, set_appearance_mode, StringVar, CTkButton, deactivate_automatic_dpi_awareness
from tkhtmlview import HTMLLabel
from  markdown import markdown

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Data_Functions as Data_Functions
import Libs.File_Manipulation as File_Manipulation

# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    Actual_Template_Variable = StringVar(master=Frame, value=Template_Used)

    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 
        if Current_Theme == "Dark":
            set_appearance_mode(mode_string="light")
        elif Current_Theme == "Light":
            set_appearance_mode(mode_string="dark")
        elif Current_Theme == "System":
            set_appearance_mode(mode_string="dark")
        else:
            set_appearance_mode(mode_string="system")

    def Show_Version_List(Clicked_on: CTkButton) -> None:
        Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]
        Work_Area_Detail_Background = list(Configuration["Global_Appearance"]["GUI_Level_ID"]["2"]["fg_color"])

        # TopUp Window
        Version_List_Window_geometry = (2000, 800)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Version_List_Window_geometry[0])
        Version_List_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Version List", width=Version_List_Window_geometry[0], height=Version_List_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=False)

         # Get Theme --> because of background color
        Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 

        if Current_Theme == "Dark":
            HTML_Background_Color = Work_Area_Detail_Background[1]
            HTML_Font_Color = Work_Area_Detail_Font[1]
        elif Current_Theme == "Light":
            HTML_Background_Color = Work_Area_Detail_Background[0]
            HTML_Font_Color = Work_Area_Detail_Font[0]
        elif Current_Theme == "System":
            HTML_Background_Color = Work_Area_Detail_Background[1]
            HTML_Font_Color = Work_Area_Detail_Font[1]
        else:
            HTML_Background_Color = Work_Area_Detail_Background[1]
            HTML_Font_Color = Work_Area_Detail_Font[1]

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Version_List_Window, Name="Version List", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Show software changes.", GUI_Level_ID=1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Double_size", GUI_Level_ID=2)

        with open(Data_Functions.Absolute_path(relative_path=f"Libs\\App\\Version_list.md"), "r", encoding="UTF-8") as file:
            html_markdown=markdown(text=file.read())
        file.close()

        Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=html_markdown, background=HTML_Background_Color, font=("Roboto", 11), fg=HTML_Font_Color,)

        # Build look of Widget
        Frame_Main.pack(side="top", fill="y", expand=False, padx=10, pady=10)
        Frame_Information_Scrollable_Area.pack(side="top", fill="none", expand=False, padx=10, pady=10)
        Information_html.pack(side="top", fill="both", expand=False, padx=10, pady=10)


    def Save_Template(Actual_Template_Frame_Var: CTkScrollableDropdown) -> None:
        global Template_List
        # Define Name for new Template
        File_Name = CustomTkinter_Functions.Dialog_Window_Request(Configuration=Configuration, title="File Name", text="Write your desire Template name.", Dialog_Type="Confirmation")
        if File_Name == None:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="Cannot save, because of missing Filename.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Actual_Template_Variable, File_Name="Settings", JSON_path=["0", "General", "Template", "Last_Used"], Information=File_Name)
            Template_List.append(File_Name)
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Template", "Templates_List"], Information=Template_List)

            # Save My_Team Dict into Downloads Folder
            Actual_Template_Settings = Settings["0"]["HQ_Data_Handler"]
            Save_Template_dict = {
                "Type": "Template",
                "Data": Actual_Template_Settings}
            
            Save_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{File_Name}.json")
            with open(file=Save_Path, mode="w") as file: 
                json.dump(Save_Template_dict, file)

            # Update Option List
            Actual_Template_Frame_Var.configure(values=Template_List)

            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Actual settings were saved into saved templates.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Apply_Template(Selected_Value: str, Settings: dict, Actual_Template_Variable: StringVar) -> None:
        Load_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{Selected_Value}.json")
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Actual_Template_Variable, File_Name="Settings", JSON_path=["0", "General", "Template", "Last_Used"], Information=Selected_Value)
        Load_Path_List = [Load_Path] # Must be here because the "Import Data" function require it to be as first element (Drag&Drop works tis way)
        Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, import_file_path=Load_Path_List, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")

    def Export_Templates() -> None:
        Source_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template")
        Destination_Path = os.path.join(os.path.expanduser("~"), "Downloads")
        files = glob(pathname=os.path.join(Source_Path, "*"))

        for Source_file in files:
            Destination_file = Source_file.replace(Source_Path, Destination_Path)
            Defaults_Lists.Copy_File(Configuration=Configuration, Source_Path=Source_file, Destination_Path=Destination_file)

        Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="All Templates exported to Download folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Import_Template(Button: CTkButton, Actual_Template_Frame_Var: CTkScrollableDropdown) -> None:
        def Template_drop_func(file: str) -> None:
            global Template_List
            # Get File Name 
            Source_Path = file[0]
            Last_Div = (Source_Path.rfind("\\")) + 1
            File_Name = Source_Path[Last_Div:]
           
            # Copy File to Template Folder
            Destination_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{File_Name}")
            Defaults_Lists.Copy_File(Configuration=Configuration, Source_Path=Source_Path, Destination_Path=Destination_Path)

            # Update Template List
            Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings)

            # Update Option List
            Actual_Template_Frame_Var.configure(values=Template_List)

            Import_window.destroy()  
            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", width=Import_window_geometry[0], height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=lambda file: Template_drop_func(file=file))
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=1)

        Icon_Theme.pack(side="top", padx=50, pady=50)
       
    def Delete_Templates(Button: CTkButton, Actual_Template_Frame_Var: CTkScrollableDropdown) -> None:
        def Delete_Templates_Confirm(Frame_Body: CTkFrame, Actual_Template_Frame_Var: CTkScrollableDropdown, No_Lines: int) -> None:
            global Template_List
            Delete_Template_List = []
            # Analyze content --> what is marked to be deleted
            for line in range(0, No_Lines):
                if line == 0:
                    Frame_Index = ""
                else:
                    Frame_Index = str(line + 1)
                Line_Element_Group = Frame_Body.children[f"!ctkframe{Frame_Index}"]
                Delete_Label_Element = Line_Element_Group.children["!ctkframe"].children["!ctklabel"]
                Delete_CheckBox_Element = Line_Element_Group.children["!ctkframe3"].children["!ctkcheckbox"]

                if Delete_CheckBox_Element.get() == True:
                    Delete_Label = str(Delete_Label_Element.cget("text"))
                    try:
                        Delete_Label = Delete_Label.replace(":", "")
                    except:
                        pass
                    Delete_Template_List.append(Delete_Label)

            # Delete
            for Template in Delete_Template_List:
                file_path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{Template}.json")
                File_Manipulation.Delete_File(file_path=file_path) 

            # Update Template List
            Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings)

            # Update Option List
            Actual_Template_Frame_Var.configure(values=Template_List)

            Delete_Activity_Correct_Close() 

            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Selected Templates were deleted.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        def Delete_Activity_Correct_Close() -> None:
            Delete_Activity_Correct_Window.destroy()
        
        # TopUp Window
        Delete_Activity_Correct_Window_geometry = (300, 250)
        # TODO --> Should make pop-up with fix width, now it is taken from sub-elements
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button, New_Window_width=Delete_Activity_Correct_Window_geometry[0])
        Delete_Activity_Correct_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Delete Templates.", width=Delete_Activity_Correct_Window_geometry[0], height=Delete_Activity_Correct_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=False)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Delete_Activity_Correct_Window, Name="Delete Templates:", Additional_Text="", Widget_size="Half_size", Widget_Label_Tooltip="To delete unwanted templates.", GUI_Level_ID=1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        # Fields - Templates
        No_Lines = 0
        for template in Template_List:
            Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{template}", Field_Type="Input_CheckBox") 
            Var1 = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
            Var1.configure(text="")
            No_Lines += 1

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Templates_Confirm(Frame_Body=Frame_Body, Actual_Template_Frame_Var=Actual_Template_Frame_Var, No_Lines=No_Lines))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=0)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Activity_Correct_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=0)


    # ------------------------- Main Functions -------------------------#
    # Actual Template
    Actual_Template_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame)
    Actual_Template_Frame.configure(variable=Actual_Template_Variable)
    Actual_Template_Frame_Var = Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Actual_Template_Frame, values=Template_List, command=lambda Actual_Template_Frame_Var: Apply_Template(Selected_Value=Actual_Template_Frame_Var, Settings=Settings, Actual_Template_Variable=Actual_Template_Variable), GUI_Level_ID=0)

    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Version list
    Icon_Versions = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="file-stack", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Versions.configure(command = lambda: Show_Version_List(Clicked_on=Icon_Versions))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Versions, message="Show version changes log.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Save Template
    Icon_Save_Template = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="save", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Save_Template.configure(text="")
    Icon_Save_Template.configure(command = lambda: Save_Template(Actual_Template_Frame_Var=Actual_Template_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Save_Template, message="Save Current settings.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Export Templates
    Icon_Export_Templates = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="folder-output", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Export_Templates.configure(text="")
    Icon_Export_Templates.configure(command = lambda: Export_Templates())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Export_Templates, message="Export all templates to Download folder.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Import Templates
    Icon_Import_Templates = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="import", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Import_Templates.configure(text="")
    Icon_Import_Templates.configure(command = lambda: Import_Template(Button=Icon_Import_Templates, Actual_Template_Frame_Var=Actual_Template_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Import_Templates, message="Import Template file to program.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Delete Templates
    Icon_Delete_Templates = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="file-x-2", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Delete_Templates.configure(text="")
    Icon_Delete_Templates.configure(command = lambda: Delete_Templates(Button=Icon_Delete_Templates, Actual_Template_Frame_Var=Actual_Template_Frame_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Delete_Templates, message="Delete Templates file from program.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Build look of Widget
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Icon_Versions.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    Icon_Save_Template.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Actual_Template_Frame.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Icon_Export_Templates.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Icon_Import_Templates.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Icon_Delete_Templates.pack(side="left", fill="none", expand=False, padx=5, pady=5)

# ------------------------------------------------------------------------------------------------------------------------------------ Side Bar ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Side_Bar(Side_Bar_Frame: CTk|CTkFrame) -> CTkFrame:
    Program_Version = Application["Application"]["Version"]

    Icon_Default_pady = 10
    Side_Bar_Top_pady = 100
    Side_Bar_Bottom_pady = 75
    
    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()
            window.update_idletasks()

    def Show_Download_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Download as P_Download
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Top_pady, Icon_Default_pady), sticky="e")
        time.sleep(0.1)
        P_Download.Page_Download(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Confirmation_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Confirmation as P_Confirmation
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Confirmation.Page_Confirmation(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_CPDI_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_CPDI as P_CPDI
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_CPDI.Page_CPDI(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_PreAdvice_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_PreAdvice as P_PreAdvice
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_PreAdvice.Page_PreAdvice(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Delivery_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Delivery as P_Delivery
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Delivery.Page_Delivery(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Invoice_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Invoice as P_Invoice
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Invoice.Page_Invoice(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_IAL_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_IAL as P_IAL
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_IAL.Page_IAL(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Settings as P_Settings
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Settings.Page_Settings(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Logo
    Logo = Elements.Get_Custom_Image(Configuration=Configuration, Frame=Side_Bar_Frame, Image_Name="Company", postfix="png", width=70, heigh=50)

    # Page - Download
    Icon_Frame_Download = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="cpu", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=0))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Download, message="Process.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Confirmation
    Icon_Frame_Confirmation = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-check", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Confirmation.configure(command = lambda: Show_Confirmation_Page(Active_Window = Active_Window, Side_Bar_Row=1))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Confirmation, message="Confirmation.json setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - CPDI
    Icon_Frame_CPDI = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="wrench", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_CPDI.configure(command = lambda: Show_CPDI_Page(Active_Window = Active_Window, Side_Bar_Row=2))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_CPDI, message="CPDI.json setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - PreAdvice
    Icon_Frame_PreAdvice = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="package-open", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_PreAdvice.configure(command = lambda: Show_PreAdvice_Page(Active_Window = Active_Window, Side_Bar_Row=3))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_PreAdvice, message="PreAdvice.json setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Delivery
    Icon_Frame_Delivery = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="package-check", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Delivery.configure(command = lambda: Show_Delivery_Page(Active_Window = Active_Window, Side_Bar_Row=4))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Delivery, message="Delivery.json setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Invoice
    Icon_Frame_Invoice = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-text", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Invoice.configure(command = lambda: Show_Invoice_Page(Active_Window = Active_Window, Side_Bar_Row=5))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Invoice, message="Invoice/BackBoneBilling/CreditMemo.json setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - IAL
    Icon_Frame_IAL = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="coins", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_IAL.configure(command = lambda: Show_IAL_Page(Active_Window = Active_Window, Side_Bar_Row=6))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_IAL, message="IAL.json setup page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=7))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Application settings page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
    Icon_Frame_Close.configure(command = lambda: window.quit())
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


# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("Time Sheets")
        super().iconbitmap(bitmap=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\HQ_Data_Generator.ico"))

        display_width = self.winfo_screenwidth()
        display_height = self.winfo_screenheight()
        Window_Frame_width = 1180
        Window_Frame_height = 700
        left_position = int(display_width // 2 - Window_Frame_width // 2)
        top_position = int(display_height // 2 - Window_Frame_height // 2)
        self.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

        # Rounded corners 
        self.config(background="#000001")
        self.attributes("-transparentcolor", "#000001")

        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>",self.click_win)
        super().bind("<B1-Motion>", self.drag_win)

    def drag_win(self, event):
        # Move only when on Side Bar
        if (self._offsetx < SideBar_Width):
            x = super().winfo_pointerx() - self._offsetx
            y = super().winfo_pointery() - self._offsety
            super().geometry(f"+{x}+{y}")
        else:
            pass

    def click_win(self, event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

if __name__ == "__main__":
    deactivate_automatic_dpi_awareness()
    Application = Defaults_Lists.Load_Application()
    Settings = Defaults_Lists.Load_Settings()
    Configuration = Defaults_Lists.Load_Configuration() 

    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]

    Template_Used = Settings["0"]["General"]["Template"]["Last_Used"]
    Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings)

    # Create folders if do not exists
    try:
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\"))
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\"))
    except:
        pass

    window = Win()
    
    # Base Windows style setup --> always keep normal before change
    set_appearance_mode(mode_string=Theme_Actual)
    pywinstyles.apply_style(window=window, style="normal")

    # ---------------------------------- Content ----------------------------------#
    # Background
    Frame_Background = Elements.Get_Frame(Configuration=Configuration, Frame=window, Frame_Size="Background", GUI_Level_ID=0)
    Frame_Background.pack(side="top", fill="none", expand=False)

    # SideBar
    Frame_Side_Bar = Elements.Get_SideBar_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="SideBar")
    Frame_Side_Bar.pack(side="left", fill="y", expand=False)

    # Work Area
    Frame_Work_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="Work_Area", GUI_Level_ID=0)
    Frame_Work_Area.pack(side="top", fill="both", expand=False)

    Frame_Header = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Header", GUI_Level_ID=0)
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="both", expand=False)

    Frame_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Main", GUI_Level_ID=0)
    Frame_Work_Area_Main.pack_propagate(flag=False)
    Frame_Work_Area_Main.pack(side="left", fill="none", expand=False)

    Get_Header(Frame=Frame_Header)
    Get_Side_Bar(Side_Bar_Frame=Frame_Side_Bar)   
    
    # run
    window.mainloop()