# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_CheckBox, WidgetRow_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Color_Picker

from customtkinter import CTk, CTkFrame, StringVar, BooleanVar, set_appearance_mode

def Settings_General_Color(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
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
    def Appearance_Change_Theme() ->  None:
        set_appearance_mode(mode_string=Theme_Variable.get())

    # ------------------------- Main Functions -------------------------#
    # Widget
    Appearance_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Appearance", Additional_Text="SideBar applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="General Appearance setup.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Theme_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Theme", Variable=Theme_Variable, Values=Theme_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Theme"], Local_function_list=[Appearance_Change_Theme], GUI_Level_ID=GUI_Level_ID) 

    Accent_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Appearance_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Accent color", Label_Size="Field_Label", Font_Size="Section_Separator")
    Accent_Color_Manual_Row = WidgetRow_Color_Picker(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Accent Color Manual", Value=Accent_Color_Manual, placeholder_text_color="#949A9F", Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Button_ToolTip="Color Picker.", Picker_Always_on_Top=True, Picker_Fixed_position=True, GUI_Level_ID=GUI_Level_ID + 1)
    Accent_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["App Default", "Windows", "Manual"], Freeze_fields=[[Accent_Color_Manual_Row],[Accent_Color_Manual_Row],[]])
    Accent_Color_Mode_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Accent Color Mode", Variable=Accent_Color_Mode_Variable, Values=Accent_Color_Mode_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Field_list=[Accent_Color_Manual_Row], Field_Blocking_dict=Accent_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    Hover_Section_Row = Widget_Section_Row(Configuration=Configuration, master=Appearance_Widget.Body_Frame, Field_Frame_Type="Single_Column", Label="Hover color", Label_Size="Field_Label", Font_Size="Section_Separator")
    Hover_Color_Manual_Row = WidgetRow_Color_Picker(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Hover Color Manual", Value=Hover_Color_Manual, placeholder_text_color="#949A9F", Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Button_ToolTip="Color Picker.", Picker_Always_on_Top=True, Picker_Fixed_position=True, GUI_Level_ID=GUI_Level_ID + 1)
    Hover_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=["App Default", "Accent Lighter", "Manual"], Freeze_fields=[[Hover_Color_Manual_Row],[Hover_Color_Manual_Row],[]])
    Hover_Color_Mode_Row = WidgetRow_OptionMenu(Settings=Settings, Configuration=Configuration, master=Appearance_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Hover Color Mode", Variable=Hover_Color_Mode_Variable, Values=Hover_Color_Mode_List, Save_To="Configuration", Save_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Field_list=[Hover_Color_Manual_Row], Field_Blocking_dict=Hover_Fields_Blocking_dict, GUI_Level_ID=GUI_Level_ID) 

    # Add Fields to Widget Body
    Appearance_Widget.Add_row(Rows=[Theme_Row, Accent_Section_Row, Accent_Color_Mode_Row, Accent_Color_Manual_Row, Hover_Section_Row, Hover_Color_Mode_Row, Hover_Color_Manual_Row])

    return Appearance_Widget


def Settings_User_Access(Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Display_name, client_id, client_secret, tenant_id = Defaults_Lists.Load_Azure_Auth()
    Export_folder = Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"]
    Export_folder_Variable = BooleanVar(master=Frame, value=Export_folder, name="Export_folder_Variable")

    # ------------------------- Local Functions ------------------------#
    def Save_set_key_Auth(Key: str, Value: str) ->  None:
        Defaults_Lists.Save_set_key_Auth(Key=Key, Value=Value)

    # ------------------------- Main Functions -------------------------#
    # Widget
    Azure_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Azure Authorization", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Authorization for OAuth2 protocol.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    NAV_Display_name_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Azure_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Client Name", Value=Display_name, placeholder_text="Enter Name of Auth app.")
    NAV_Display_name_Row.Local_function_list = [lambda: Save_set_key_Auth(Key="Display_name", Value=NAV_Display_name_Row.Get_Value())]
    NAV_Client_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Azure_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Client ID", Value=client_id, placeholder_text="Enter Client ID of Auth app.")
    NAV_Client_ID_Row.Local_function_list = [lambda: Save_set_key_Auth(Key="client_id", Value=NAV_Client_ID_Row.Get_Value())]
    NAV_Client_Secret_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Azure_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Password", Label="Client Secret", Value=client_secret, placeholder_text="Enter Secret ID of Auth app.")
    NAV_Client_Secret_Row.Local_function_list = [lambda: Save_set_key_Auth(Key="client_secret", Value=NAV_Client_Secret_Row.Get_Value())]
    NAV_Tenant_ID_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Azure_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Field_Size="Normal", Label="Tenant ID", placeholder_text=tenant_id, placeholder_text_color="#949A9F")
    Export_Download_Folder_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Azure_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column", Label="Export NAV folder", Variable=Export_folder_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Export", "Download_Folder"])

    # Add Fields to Widget Body
    Azure_Widget.Add_row(Rows=[NAV_Display_name_Row, NAV_Client_ID_Row, NAV_Client_Secret_Row, NAV_Tenant_ID_Row, Export_Download_Folder_Row])
    NAV_Tenant_ID_Row.Freeze()

    return Azure_Widget
