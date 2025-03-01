# Import Libraries

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

import pywinstyles

from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, CTkOptionMenu, CTkButton, set_appearance_mode
from CTkMessagebox import CTkMessagebox

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

# -------------------------------------------------------------------------- Tab Appearance --------------------------------------------------------------------------#
def Settings_General_Theme(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame, window: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    Theme_List = list(Configuration["Global_Appearance"]["Window"]["Theme_List"])
    Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
    Win_Style_List = list(Configuration["Global_Appearance"]["Window"]["Style_List"])

    # ------------------------- Local Functions ------------------------#
    def Appearance_Change_Theme(Theme_Frame_Var: CTkOptionMenu) ->  None:
        set_appearance_mode(mode_string=Theme_Frame_Var)
        Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Theme_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Theme"], Information=Theme_Frame_Var)

    def Appearance_Change_Win_Style(Win_Style_Selected: str, window: CTk|CTkFrame) -> None:
        # Base Windows style setup --> always keep normal before change
        pywinstyles.apply_style(window=window, style="normal")
        pywinstyles.apply_style(window=window, style=Win_Style_Selected)
        Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Win_Style_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Style"], Information=Win_Style_Selected)

    # ------------------------- Main Functions -------------------------#
    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Win_Style_Variable = StringVar(master=Frame, value=Win_Style_Actual)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="General Appearance", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="General Appearance settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(variable=Theme_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Theme_Frame_Var, values=Theme_List, command = lambda Theme_Frame_Var: Appearance_Change_Theme(Theme_Frame_Var=Theme_Frame_Var))

    # Field - Windows Style
    Win_Style_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Window Style", Field_Type="Input_OptionMenu") 
    Win_Style_Frame_Var = Win_Style_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Win_Style_Frame_Var.configure(variable=Win_Style_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Win_Style_Frame_Var, values=Win_Style_List, command= lambda Win_Style_Selected: Appearance_Change_Win_Style(Win_Style_Selected=Win_Style_Selected, window=window))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Color(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
    Accent_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
    Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

    Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
    Hover_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
    Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

    # ------------------------- Local Functions ------------------------#
    def Settings_Disabling_Color_Pickers(Selected_Value: str, Entry_Field: CTkEntry, Picker_Button: CTkButton, Variable: StringVar, Helper: str) -> None:
        if Selected_Value == "Windows":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Accent only
            Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "App Default":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Both
            if Helper == "Accent":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Accent Lighter":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Hover only
            Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Picker_Button.configure(state="normal")
            # Both
            if Helper == "Accent":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        else:
            Error_Message = CTkMessagebox(title="Error", message="Accent Color Method not allowed", icon="cancel", fade_in_duration=1)
            Error_Message.get()

    def Appearance_Pick_Manual_Color(Clicked_on: CTkButton, Color_Manual_Frame_Var: CTkEntry, Helper: str) -> None:
        def Quit_Save(Helper: str):
            Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", f"{Helper}", f"{Helper}_Color_Manual"], Information=Color_Picker_Frame.get())
            Color_Picker_window.destroy()

        Import_window_geometry = (300, 250)
        Top_middle_point = Defaults_Lists.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Import_window_geometry[0])
        Color_Picker_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Color Picker", width=Import_window_geometry[0], height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=False)
        Color_Picker_window.bind(sequence="<Escape>", func=lambda event: Quit_Save(Helper=Helper))

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Color_Picker_window, Name="", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Color_Picker_Frame = Elements.Get_Color_Picker(Configuration=Configuration, Frame=Frame_Body, Color_Manual_Frame_Var=Color_Manual_Frame_Var)

        # Build look of Widget --> must be before inset
        Color_Picker_Frame.pack(padx=0, pady=0) 

    # ------------------------- Main Functions -------------------------#
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Colors", Additional_Text="SideBar applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="Colors")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(variable=Accent_Color_Mode_Variable)
    
    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Entry_DropDown") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual, placeholder_text_color="#949A9F")
    Accent_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Information=Accent_Color_Manual_Frame_Var.get()))
    Button_Accent_Color_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Button_Accent_Color_Frame_Var.configure(command = lambda: Appearance_Pick_Manual_Color(Clicked_on=Button_Accent_Color_Frame_Var, Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var, Helper="Accent"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Accent_Color_Frame_Var, message="ColorPicker", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Accent_Color_Mode_Frame_Var, values=Accent_Color_Mode_List, command = lambda Accent_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode_Frame_Var, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Button_Accent_Color_Frame_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent"))
    Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Button_Accent_Color_Frame_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent")  # Must be here because of initial value

    # Field - Hover Color Mode
    Hover_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Mode", Field_Type="Input_OptionMenu") 
    Hover_Color_Mode_Frame_Var = Hover_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Hover_Color_Mode_Frame_Var.configure(variable=Hover_Color_Mode_Variable)

    # Field - Hover Color Manual
    Hover_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Manual", Field_Type="Entry_DropDown") 
    Hover_Color_Manual_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Hover_Color_Manual_Frame_Var.configure(placeholder_text=Hover_Color_Manual, placeholder_text_color="#949A9F")
    Hover_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=None, Configuration=Configuration, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Information=Hover_Color_Manual_Frame_Var.get()))
    Button_Hover_Color_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Button_Hover_Color_Frame_Var.configure(command = lambda: Appearance_Pick_Manual_Color(Clicked_on=Button_Hover_Color_Frame_Var, Color_Manual_Frame_Var=Hover_Color_Manual_Frame_Var, Helper="Hover"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Hover_Color_Frame_Var, message="ColorPicker", ToolTip_Size="Normal")

    # Disabling fields --> Hover_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Hover_Color_Mode_Frame_Var, values=Hover_Color_Mode_List, command = lambda Hover_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode_Frame_Var, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Button_Hover_Color_Frame_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover"))
    Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Button_Hover_Color_Frame_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover")   # Must be here because of initial value

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Settings_User_Widget(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    User_Name = Settings["0"]["General"]["User"]["Name"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    User_Email = Settings["0"]["General"]["User"]["Email"]
    
    # ------------------------- Local Functions ------------------------#
    def Password_required(User_Type_Variable: StringVar, User_Type_Frame_Var: str) -> None:
        def Dialog_Window_Request(title: str, text: str, Dialog_Type: str) -> str|None:
            # Password required
            dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type)
            Password = dialog.get_input()
            return Password
        
        if User_Type_Frame_Var == "User":
            User_Type_Variable.value = "User"
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=User_Type_Variable, File_Name="Settings", JSON_path=["0", "General", "User", "User_Type"], Information=User_Type_Frame_Var)
        elif User_Type_Frame_Var == "Manager":
            Password = Dialog_Window_Request(title="Admin", text="Write your password", Dialog_Type="Password")

            if Password == "JVA_is_best":
                User_Type_Variable.value = "Manager"
                Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=User_Type_Variable, File_Name="Settings", JSON_path=["0", "General", "User", "User_Type"], Information=User_Type_Frame_Var)
            else:
                User_Type_Variable.value = "User"
                Error_Message = CTkMessagebox(title="Error", message=f"Wrong administration password.", icon="cancel", fade_in_duration=1)
                Error_Message.get()
           

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="User", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="This is setup of definition if user is considerate as user or user leading team with additional functionality.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - User ID
    User_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User ID", Field_Type="Input_Normal")
    User_ID_Frame_Var = User_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    User_ID_Frame_Var.configure(placeholder_text="My Konica ID.")
    User_ID_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "General", "User", "Code"], Information=User_ID_Frame_Var.get()))
    Entry_field_Insert(Field=User_ID_Frame_Var, Value=User_ID)

    # Field - Name
    User_Name_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Name", Field_Type="Input_Normal") 
    User_Name_Frame_Var = User_Name_Frame.children["!ctkframe3"].children["!ctkentry"]
    User_Name_Frame_Var.configure(placeholder_text="My Name.")
    User_Name_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "General", "User", "Name"], Information=User_Name_Frame_Var.get()))
    Entry_field_Insert(Field=User_Name_Frame_Var, Value=User_Name)

    # Field - User Email
    User_Email_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="User Email", Field_Type="Input_Normal")
    User_Email_Frame_Var = User_Email_Frame.children["!ctkframe3"].children["!ctkentry"]
    User_Email_Frame_Var.configure(placeholder_text="My Konica ID.")
    User_Email_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["0", "General", "User", "Email"], Information=User_Email_Frame_Var.get()))
    Entry_field_Insert(Field=User_Email_Frame_Var, Value=User_Email)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main


def Settings_User_Access(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()

    # ------------------------- Local Functions ------------------------#
    def Exchange_Request_Permissions() -> None:
        print("Exchange_Request_Permissions")
        # TODO --> show new popup and let fill password to let automatically be re-generated
        pass

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Azure Authorization", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Authorization for OAuth2 protocol.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Client ID
    NAV_Client_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client ID", Field_Type="Input_Normal") 
    NAV_Client_ID_Frame_Var = NAV_Client_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Client_ID_Frame_Var.configure(placeholder_text=client_id, placeholder_text_color="#949A9F")
    NAV_Client_ID_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_set_key_env(Key="client_id", Value=NAV_Client_ID_Frame_Var.get()))
    Entry_field_Insert(Field=NAV_Client_ID_Frame_Var, Value=client_id)

    # Field - Client Secret
    NAV_Client_Secret_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Client Secret", Field_Type="Password_Normal")
    NAV_Client_Secret_Frame_Var = NAV_Client_Secret_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Client_Secret_Frame_Var.configure(placeholder_text_color="#949A9F")
    NAV_Client_Secret_Frame_Var.bind("<FocusOut>", lambda Entry_value: Defaults_Lists.Save_set_key_env(Key="client_secret", Value=NAV_Client_Secret_Frame_Var.get()))
    Entry_field_Insert(Field=NAV_Client_Secret_Frame_Var, Value=client_secret)

    # Field - Tenant ID
    NAV_Tenant_ID_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Tenant ID", Field_Type="Input_Normal")
    NAV_Tenant_ID_Frame_Var = NAV_Tenant_ID_Frame.children["!ctkframe3"].children["!ctkentry"]
    NAV_Tenant_ID_Frame_Var.configure(placeholder_text=tenant_id)
    NAV_Tenant_ID_Frame_Var.configure(state="disabled", placeholder_text_color="#949A9F")

    # Update Request NEw Secret
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Configuration=Configuration, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Button_MT_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_MT_Del_One_Var.configure(text="Request", command = lambda:Exchange_Request_Permissions())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_MT_Del_One_Var, message="Request access for your User-Client_ID to .", ToolTip_Size="Normal")


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main
