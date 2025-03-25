# Import Libraries
import os
import json
from glob import glob

import pywinstyles
from customtkinter import CTk, CTkFrame, CTkButton, CTkOptionMenu, StringVar, BooleanVar, IntVar, set_appearance_mode
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 
from tkhtmlview import HTMLLabel
from markdown import markdown

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.File_Manipulation as File_Manipulation

import Libs.Data_Functions as Data_Functions
import Libs.Azure.Authorization as Authorization

# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Settings: dict, Configuration: dict|None, window: CTk|None, Documents: dict, Frame: CTkFrame) -> CTkFrame:
    global Actual_Template_Variable
    # Global Variables
    Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings, window=window)
    Actual_Template_Variable = StringVar(master=window, value=Settings["0"]["General"]["Template"]["Last_Used"], name="Actual_Template_Variable")
    Export_folder_Variable = BooleanVar(master=Frame, value=Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"], name="Export_folder_Variable")

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
        Version_List_Window_geometry = (1400, 800)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Version_List_Window_geometry[0])
        Version_List_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Version List", max_width=Version_List_Window_geometry[0], max_height=Version_List_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)

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
        Frame_Main.configure(bg_color = "#000001", height=700)
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


    def Save_Template(Button: CTkButton, Actual_Template_Frame_Var: CTkScrollableDropdown) -> None:
        Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings, window=window)
        # Define Name for new Template
        File_Name = CustomTkinter_Functions.Dialog_Window_Request(Configuration=Configuration, title="File Name", text="Write your desire Template name.", Dialog_Type="Confirmation", GUI_Level_ID=1)
        File_Name = File_Name.replace(" ", "_")

        if File_Name == None:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Cannot save, because of missing Filename.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            # Update Variable
            global Actual_Template_Variable
            # Actual_Template_Variable.set(value=File_Name)
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Actual_Template_Variable, File_Name="Settings", JSON_path=["0", "General", "Template", "Last_Used"], Information=File_Name, User_Change=False)
            Template_List.append(File_Name)
            Template_List = list(set(Template_List))
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Template", "Templates_List"], Information=Template_List, User_Change=False)

            # Save Template to Operational folder
            Actual_Template_Settings = Settings["0"]["HQ_Data_Handler"]
            Save_Template_dict = {
                "Type": "Template",
                "Data": Actual_Template_Settings}
            
            Save_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{File_Name}.json")
            with open(file=Save_Path, mode="w") as file: 
                json.dump(Save_Template_dict, file)

            # Update Option List
            Actual_Template_Frame_Var.configure(values=Template_List)

            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Actual settings were saved into saved templates.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Apply_Template(Selected_Value: str, Settings: dict) -> None:
        global Actual_Template_Variable

        # Save actual Template
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Actual_Template_Variable, File_Name="Settings", JSON_path=["0", "General", "Template", "Last_Used"], Information=Selected_Value, User_Change=False)

        # Load File
        Load_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{Selected_Value}.json")
        Load_Path_List = [Load_Path] # Must be here because the "Import Data" function require it to be as first element (Drag&Drop works tis way)
        Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=Load_Path_List, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite", User_Change=False)

    def Export_Templates() -> None:
        Source_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template")
        Destination_Path = os.path.join(os.path.expanduser("~"), "Downloads")
        files = glob(pathname=os.path.join(Source_Path, "*"))

        for Source_file in files:
            Destination_file = Source_file.replace(Source_Path, Destination_Path)
            File_Manipulation.Copy_File(Configuration=Configuration, window=window, Source_Path=Source_file, Destination_Path=Destination_file)

        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="All Templates exported to Download folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Import_Template(Button: CTkButton, Actual_Template_Frame_Var: CTkScrollableDropdown) -> None:
        def Template_drop_func(file: str) -> None:
            global Template_List
            # Get File Name 
            for Source_Path in file:
                Last_Div = (Source_Path.rfind("\\")) + 1
                File_Name = Source_Path[Last_Div:]
            
                # Copy File to Template Folder
                Destination_Path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{File_Name}")
                File_Manipulation.Copy_File(Configuration=Configuration, window=window, Source_Path=Source_Path, Destination_Path=Destination_Path)

                # Update Template List
                Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings, window=window)

                # Update Option List
                Actual_Template_Frame_Var.configure(values=Template_List)

            Import_window.destroy()  
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Your settings file has been imported. You can close Window.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=1)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=lambda file: Template_drop_func(file=file))
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=1)

        Icon_Theme.pack(side="top", padx=50, pady=50)
       
    def Delete_Templates(Button: CTkButton, Actual_Template_Frame_Var: CTkScrollableDropdown) -> None:
        Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings, window=window)
        def Delete_Templates_Confirm(Frame_Body: CTkFrame, Actual_Template_Frame_Var: CTkScrollableDropdown, No_Lines: int) -> None:
            global Template_List, Actual_Template_Variable
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

                    # Update Template Variable if needed
                    if Delete_Label == Actual_Template_Variable.get():
                        Actual_Template_Variable.set(value="")
                        Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "Template", "Last_Used"], Information="", User_Change=False)
                    else:
                        pass

            # Delete
            for Template in Delete_Template_List:
                file_path = Data_Functions.Absolute_path(relative_path=f"Operational\\Template\\{Template}.json")
                File_Manipulation.Delete_File(file_path=file_path) 

            # Update Template List
            Template_List = Data_Functions.Get_All_Templates_List(Settings=Settings, window=window)

            # Update Option List
            Actual_Template_Frame_Var.configure(values=Template_List)

            Delete_Activity_Correct_Close() 
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Selected Templates were deleted.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

        def Delete_Activity_Correct_Close() -> None:
            Delete_Activity_Correct_Window.destroy()
        
        # TopUp Window
        Delete_Activity_Correct_Window_geometry = (320, 500)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button, New_Window_width=Delete_Activity_Correct_Window_geometry[0])
        Delete_Activity_Correct_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Delete Templates.", max_width=Delete_Activity_Correct_Window_geometry[0], max_height=Delete_Activity_Correct_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Delete_Activity_Correct_Window, Name=f"Delete Templates:", Additional_Text="", Widget_size="Half_size", Widget_Label_Tooltip=f"To delete unwanted templates.", GUI_Level_ID=1)
        Frame_Body = Frame_Main.children["!ctkframe2"]

        # Fields - Templates
        No_Lines = 0
        for template in Template_List:
            Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{template}",  Field_Type="Input_CheckBox")  
            Var1 = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
            Var1.configure(text="")
            No_Lines += 1

        # Dynamic Content height
        content_row_count = len(Frame_Body.winfo_children())
        content_height = content_row_count * 35 + 30 + 50  # Lines multiplied + button + additional space for header
        if content_height > Delete_Activity_Correct_Window_geometry[1]:
            content_height = Delete_Activity_Correct_Window_geometry[1]
        Frame_Main.configure(bg_color = "#000001", height=content_height)

        # Buttons
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda:Delete_Templates_Confirm(Frame_Body=Frame_Body, Actual_Template_Frame_Var=Actual_Template_Frame_Var, No_Lines=No_Lines))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm line delete.", ToolTip_Size="Normal", GUI_Level_ID=0)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda:Delete_Activity_Correct_Close())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Dont process, closing Window.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # ------------------------- Main Functions -------------------------#
    Status_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Columns", GUI_Level_ID=0)
    Status_Frame.configure(width=15)

    # Authorization OAuth2 Flag
    try:
        Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
        Auth_Result = Authorization.Azure_OAuth_Test(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    except:
        Auth_Result = False
    Auth_Result_Variable = IntVar(master=Status_Frame, value=Auth_Result, name="Auth_Result_Variable")
    Authorization_Frame = Elements.Get_RadioButton_Normal(Configuration=Configuration, Frame=Status_Frame, Var_Value=True) 
    Authorization_Frame.configure(width=2, height=2, radiobutton_width=10, radiobutton_height=10, border_width_unchecked=2, border_width_checked=2, fg_color="#517A31", text="", state="disabled", variable=Auth_Result_Variable)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Authorization_Frame, message="Initial Azure authorization status.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Authorization OAuth2 Flag
    Export_folder_Frame = Elements.Get_RadioButton_Normal(Configuration=Configuration, Frame=Status_Frame, Var_Value=True) 
    Export_folder_Frame.configure(width=2, height=2, radiobutton_width=10, radiobutton_height=10, border_width_unchecked=2, border_width_checked=2, fg_color="#517A31", text="", state="disabled", variable=Export_folder_Variable)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Export_folder_Frame, message="Export files to NAV folders.", ToolTip_Size="Normal", GUI_Level_ID=0)
    
    # Actual Template
    Actual_Template_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame)
    Actual_Template_Frame.configure(variable=Actual_Template_Variable)
    Actual_Template_Frame_Var = Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Actual_Template_Frame, values=Template_List, command=lambda Selected_Value: Apply_Template(Selected_Value=Selected_Value, Settings=Settings), GUI_Level_ID=0)

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
    Icon_Save_Template.configure(command = lambda: Save_Template(Button=Icon_Save_Template, Actual_Template_Frame_Var=Actual_Template_Frame_Var))
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
    Status_Frame.pack(side="right", fill="none", expand=False, padx=5, pady=(2,2))
    Authorization_Frame.pack(side="top", fill="none", expand=False, padx=(0, 3), pady=2)
    Export_folder_Frame.pack(side="top", fill="none", expand=False, padx=(0, 3), pady=2)
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Icon_Versions.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    Icon_Save_Template.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Actual_Template_Frame.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Icon_Export_Templates.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Icon_Import_Templates.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Icon_Delete_Templates.pack(side="left", fill="none", expand=False, padx=5, pady=5)