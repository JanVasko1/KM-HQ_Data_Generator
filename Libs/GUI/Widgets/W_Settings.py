# Import Libraries

import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, BooleanVar, CTkOptionMenu, CTkButton, set_appearance_mode

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Entry_field_Insert(Field: CTkEntry, Value: str|int) -> None:
    if type(Value) == str:
        if Value != "":
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    elif type(Value) == int:
        if Value > 0:
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    else:
        pass

def Settings_General_Color(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    Theme_List = list(Configuration["Global_Appearance"]["Window"]["Theme_List"])
    Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
    Accent_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
    Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

    Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
    Hover_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
    Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # ------------------------- Local Functions ------------------------#
    def Settings_Disabling_Color_Pickers(Selected_Value: str, Entry_Field: CTkEntry, Picker_Button: CTkButton, Variable: StringVar, Helper: str) -> None:
        if Selected_Value == "Windows":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Accent only
            Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "App Default":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Both
            if Helper == "Accent":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Accent Lighter":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Hover only
            Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Picker_Button.configure(state="normal")
            # Both
            if Helper == "Accent":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Accent Color Method not allowed", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Appearance_Pick_Manual_Color(Clicked_on: CTkButton, Color_Manual_Frame_Var: CTkEntry, Helper: str, GUI_Level_ID: int|None = None) -> None:
        def Quit_Save(Helper: str):
            Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", f"{Helper}", f"{Helper}_Color_Manual"], Information=Color_Picker_Frame.get())
            Color_Picker_window.destroy()

        Import_window_geometry = (300, 300)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Import_window_geometry[0])
        Color_Picker_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Color Picker", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=False)
        Color_Picker_window.bind(sequence="<Escape>", func=lambda event: Quit_Save(Helper=Helper))

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Color_Picker_window, Name="", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="", GUI_Level_ID=GUI_Level_ID)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Color_Picker_Frame = Elements.Get_Color_Picker(Configuration=Configuration, Frame=Frame_Body, Color_Manual_Frame_Var=Color_Manual_Frame_Var, GUI_Level_ID=GUI_Level_ID)

        # Build look of Widget --> must be before inset
        Color_Picker_Frame.pack(padx=0, pady=0) 

    def Appearance_Change_Theme(Theme_Frame_Var: CTkOptionMenu) ->  None:
        set_appearance_mode(mode_string=Theme_Frame_Var)
        Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Theme_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Theme"], Information=Theme_Frame_Var)

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Colors", Additional_Text="SideBar applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="Colors", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(variable=Theme_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Theme_Frame_Var, values=Theme_List, command = lambda Theme_Frame_Var: Appearance_Change_Theme(Theme_Frame_Var=Theme_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent color", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(variable=Accent_Color_Mode_Variable)
    
    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Entry_DropDown") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual, placeholder_text_color="#949A9F")
    Accent_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Information=Accent_Color_Manual_Frame_Var.get()))
    Button_Accent_Color_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Button_Accent_Color_Frame_Var.configure(command = lambda: Appearance_Pick_Manual_Color(Clicked_on=Button_Accent_Color_Frame_Var, Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var, Helper="Accent", GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Accent_Color_Frame_Var, message="ColorPicker", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Accent_Color_Mode_Frame_Var, values=Accent_Color_Mode_List, command = lambda Accent_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode_Frame_Var, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Button_Accent_Color_Frame_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent"), GUI_Level_ID=GUI_Level_ID)
    Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Button_Accent_Color_Frame_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent")  # Must be here because of initial value

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover color", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Hover Color Mode
    Hover_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Mode", Field_Type="Input_OptionMenu") 
    Hover_Color_Mode_Frame_Var = Hover_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Hover_Color_Mode_Frame_Var.configure(variable=Hover_Color_Mode_Variable)

    # Field - Hover Color Manual
    Hover_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Manual", Field_Type="Entry_DropDown") 
    Hover_Color_Manual_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Hover_Color_Manual_Frame_Var.configure(placeholder_text=Hover_Color_Manual, placeholder_text_color="#949A9F")
    Hover_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Information=Hover_Color_Manual_Frame_Var.get()))
    Button_Hover_Color_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Button_Hover_Color_Frame_Var.configure(command = lambda: Appearance_Pick_Manual_Color(Clicked_on=Button_Hover_Color_Frame_Var, Color_Manual_Frame_Var=Hover_Color_Manual_Frame_Var, Helper="Hover", GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Hover_Color_Frame_Var, message="ColorPicker", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Disabling fields --> Hover_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Hover_Color_Mode_Frame_Var, values=Hover_Color_Mode_List, command = lambda Hover_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode_Frame_Var, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Button_Hover_Color_Frame_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover"), GUI_Level_ID=GUI_Level_ID)
    Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Button_Hover_Color_Frame_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover")   # Must be here because of initial value

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Settings_User_Access(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Export_folder = Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"]

    Export_folder_Variable = BooleanVar(master=Frame, value=Export_folder, name="Export_folder_Variable")

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Azure Authorization", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Authorization for OAuth2 protocol.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Display Name
    NAV_Display_name_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client Name", Field_Type="Input_Normal") 
    NAV_Display_name_Frame_Var = NAV_Display_name_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Display_name_Frame_Var.configure(placeholder_text="Enter Name of Auth app")
    NAV_Display_name_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_set_key_Auth(Key="Display_name", Value=NAV_Display_name_Frame_Var.get()))
    Entry_field_Insert(Field=NAV_Display_name_Frame_Var, Value=Display_name)

    # Field - Client ID
    NAV_Client_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client ID", Field_Type="Input_Normal") 
    NAV_Client_ID_Frame_Var = NAV_Client_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Client_ID_Frame_Var.configure(placeholder_text="Enter Client ID of Auth app")
    NAV_Client_ID_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_set_key_Auth(Key="client_id", Value=NAV_Client_ID_Frame_Var.get()))
    Entry_field_Insert(Field=NAV_Client_ID_Frame_Var, Value=client_id)

    # Field - Client Secret
    NAV_Client_Secret_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client Secret", Field_Type="Password_Normal")
    NAV_Client_Secret_Frame_Var = NAV_Client_Secret_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Client_Secret_Frame_Var.configure(placeholder_text="Enter Secret ID of Auth app")
    NAV_Client_Secret_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_set_key_Auth(Key="client_secret", Value=NAV_Client_Secret_Frame_Var.get()))
    Entry_field_Insert(Field=NAV_Client_Secret_Frame_Var, Value=client_secret)

    # Field - Tenant ID
    NAV_Tenant_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Tenant ID", Field_Type="Input_Normal")
    NAV_Tenant_ID_Frame_Var = NAV_Tenant_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Tenant_ID_Frame_Var.configure(placeholder_text=tenant_id)
    NAV_Tenant_ID_Frame_Var.configure(state="disabled", placeholder_text_color="#949A9F")

    # Field - Use
    Export_Download_Folder_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Export NAV folder", Field_Type="Input_CheckBox") 
    Export_Download_Folder_Frame_Var = Export_Download_Folder_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Export_Download_Folder_Frame_Var.configure(variable=Export_folder_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Export_folder_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Export", "Download_Folder"], Information=Export_folder_Variable))

   
    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
