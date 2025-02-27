# Import Libraries
from PIL import Image
from datetime import datetime

from customtkinter import CTkButton, CTk, CTkFrame, CTkScrollableFrame, CTkEntry, CTkLabel, CTkFont, CTkImage, CTkRadioButton, CTkTabview, CTkOptionMenu, CTkCheckBox, CTkProgressBar, CTkInputDialog, CTkComboBox, get_appearance_mode
from CTkTable import CTkTable
from CTkColorPicker import CTkColorPicker
from CTkToolTip import CTkToolTip
from CTkMessagebox import CTkMessagebox

import Libs.Defaults_Lists as Defaults_Lists
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

from iconipy import IconFactory 
import winaccent

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Time_Validate(Settings: dict, Value: str) -> None:
    Time_Format = Settings["0"]["General"]["Formats"]["Time"]

    if Value != "":
        try:
            datetime.strptime(Value, Time_Format)
        except:
            Error_Message = CTkMessagebox(title="Error", message=f"Value: {Value} in not proper Time format, should be: HH:MM.", icon="cancel", fade_in_duration=1)
            Error_Message.get()
    else:
        pass

def Date_Validate(Settings: dict, Value: str) -> None:
    Date_Format = Settings["0"]["General"]["Formats"]["Date"]

    if Value != "":
        try:
            datetime.strptime(Value, Date_Format)
        except:
            Error_Message = CTkMessagebox(title="Error", message=f"Value: {Value} in not in proper Date format, should be: YYYY-MM-DD.", icon="cancel", fade_in_duration=1)
            Error_Message.get()
    else:
        pass

def Int_Validate(Settings: dict, Value: str) -> None:
    if Value != "":
        try:
            int(Value)
        except:
            Error_Message = CTkMessagebox(title="Error", message=f"Value: {Value} in not whole number.", icon="cancel", fade_in_duration=1)
            Error_Message.get()
    else:
        pass

def Float_Validate(Settings: dict, Value: str) -> None:
    if Value != "":
        try:
            float(Value)
        except:
            Error_Message = CTkMessagebox(title="Error", message=f"Value: {Value} in not float number.", icon="cancel", fade_in_duration=1)
            Error_Message.get()
    else:
        pass


def lighten_hex_color(hex_color, percentage):
    # Remove the hash symbol if present
    hex_color = hex_color.lstrip('#')

    # Convert hex to RGB
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    # Calculate the new RGB values
    r = int(r + (255 - r) * percentage)
    g = int(g + (255 - g) * percentage)
    b = int(b + (255 - b) * percentage)

    # Ensure the values are within the valid range
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))

    # Convert RGB back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


def Define_Accent_Color(Configuration:dict, Color_json: list|str) -> tuple|str|None:

    Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
    Accent_Color_Windows = winaccent.accent_normal
    Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

    if Accent_Color_Mode == "Windows":
        Selected_color = tuple([Accent_Color_Windows, Accent_Color_Windows])
    elif Accent_Color_Mode == "Manual":
        Selected_color = tuple([Accent_Color_Manual, Accent_Color_Manual])
    elif Accent_Color_Mode == "App Default":
        if type(Color_json) is list:
            Selected_color = tuple(Color_json)
        else:
            Selected_color = Color_json
    return Selected_color

def Define_Hover_Color(Configuration:dict, Color_json: list|str, Accent_Color: tuple|str) -> tuple|str|None:
        
    Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
    Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

    if Hover_Color_Mode == "Accent Lighter":
        if type(Accent_Color) is tuple:
            Select_Color1 = lighten_hex_color(hex_color=Accent_Color[0], percentage=0.2)
            Select_Color2 = lighten_hex_color(hex_color=Accent_Color[1], percentage=0.2)
            Selected_color = tuple([Select_Color1, Select_Color2])
        else:
            if Accent_Color == "transparent":
                Selected_color = ""
            else:
                Select_Color1 = lighten_hex_color(hex_color=Accent_Color, percentage=0.2)
                Selected_color = tuple([Select_Color1, Select_Color1])
    elif Hover_Color_Mode == "Manual":
        Selected_color = tuple([Hover_Color_Manual, Hover_Color_Manual])
    elif Hover_Color_Mode == "App Default":
        if type(Color_json) is list:
            Selected_color = tuple(Color_json)
        else:
            Selected_color = Color_json
    return Selected_color

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Font ----------------------------------------------# 
def Get_Font(Configuration:dict, Font_Size: str) -> CTkFont:
    Configuration_Font_Text_Main = Configuration["Font"][f"{Font_Size}"]
    Font_Text_Main = CTkFont(
        family = Configuration_Font_Text_Main["family"],
        size = Configuration_Font_Text_Main["size"],
        weight = Configuration_Font_Text_Main["weight"],
        slant = Configuration_Font_Text_Main["slant"],
        underline = Configuration_Font_Text_Main["underline"],
        overstrike = Configuration_Font_Text_Main["overstrike"])
    return Font_Text_Main

# ---------------------------------------------- Text ----------------------------------------------# 
def Get_Label(Configuration:dict, Frame: CTk|CTkFrame, Label_Size: str, Font_Size: str) -> CTkLabel:
    Configuration_Text_Main = Configuration["Labels"][f"{Label_Size}"]
    Text_Main = CTkLabel(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size=Font_Size),
        height = Configuration_Text_Main["height"],
        fg_color = Configuration_Text_Main["fg_color"],
        text_color = tuple(Configuration_Text_Main["text_color"]),
        anchor = Configuration_Text_Main["anchor"],
        padx = Configuration_Text_Main["padx"],
        pady = Configuration_Text_Main["pady"],
        wraplength = Configuration_Text_Main["wraplength"])
    return Text_Main

def Get_Label_Icon(Configuration: dict, Frame: CTk|CTkFrame, Label_Size: str, Font_Size: str, Icon_Name: str, Icon_Size: str) -> CTkLabel:
    Frame_Label = Get_Label(Configuration=Configuration, Frame=Frame, Label_Size=Label_Size, Font_Size=Font_Size)
    CTK_Image = Get_CTk_Icon(Configuration=Configuration, Icon_Name=Icon_Name, Icon_Size=Icon_Size)
    Frame_Label.configure(image=CTK_Image, text="", anchor="e")
    return Frame_Label

# ---------------------------------------------- Buttons ----------------------------------------------# 
def Get_Button(Configuration:dict, Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Normal = Configuration["Buttons"][f"{Button_Size}"]

    if Button_Size == "DatePicker_Days":
        fg_color = Configuration_Button_Normal["fg_color"]
        Accent_Color_help = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Button_Normal["Accent_Color_help"])
        hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Button_Normal["hover_color"], Accent_Color=Accent_Color_help)
    else:
        fg_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Button_Normal["fg_color"])
        hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Button_Normal["hover_color"], Accent_Color=fg_color)

    Button_Normal = CTkButton(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Button_Normal["width"],
        height = Configuration_Button_Normal["height"],
        corner_radius = Configuration_Button_Normal["corner_radius"],
        border_width = Configuration_Button_Normal["border_width"],
        border_color = tuple(Configuration_Button_Normal["border_color"]),
        bg_color = Configuration_Button_Normal["bg_color"],
        fg_color = fg_color,
        hover = Configuration_Button_Normal["hover"],
        hover_color = hover_color,
        anchor = Configuration_Button_Normal["anchor"],
        text_color = tuple(Configuration_Button_Normal["text_color"]))
    return Button_Normal

def Get_Button_Icon(Configuration:dict, Frame: CTk|CTkFrame, Icon_Name: str, Icon_Size: str, Button_Size: str) -> CTkFrame:
    Configuration_Button_Icon = Configuration["Buttons"][f"{Button_Size}"]

    if Button_Size == "Picture_SideBar":
        Accent_Color_help = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Button_Icon["Accent_Color_help"])
    else:
        Accent_Color_help = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Button_Icon["fg_color"])
    hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Button_Icon["hover_color"], Accent_Color=Accent_Color_help)

    Frame_Button = CTkButton(
        master = Frame,
        width = Configuration_Button_Icon["width"],
        height = Configuration_Button_Icon["height"],
        corner_radius = Configuration_Button_Icon["corner_radius"],
        border_width = Configuration_Button_Icon["border_width"],
        bg_color = Configuration_Button_Icon["bg_color"],
        fg_color = Configuration_Button_Icon["fg_color"],
        hover = Configuration_Button_Icon["hover"],
        hover_color = hover_color,
        anchor = Configuration_Button_Icon["anchor"],
        text = "")
    CTK_Image = Get_CTk_Icon(Configuration=Configuration, Icon_Name=Icon_Name, Icon_Size=Icon_Size)
    Frame_Button.configure(image=CTK_Image, text="")
    return Frame_Button

def Get_Button_Chart(Configuration:dict, Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Chart = Configuration["Buttons"][f"{Button_Size}"]

    fg_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Button_Chart["fg_color"])
    hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Button_Chart["hover_color"], Accent_Color=fg_color)

    Frame_Button = CTkButton(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Button_Chart["width"],
        height = Configuration_Button_Chart["height"],
        corner_radius = Configuration_Button_Chart["corner_radius"],
        border_width = Configuration_Button_Chart["border_width"],
        border_color = Configuration_Button_Chart["border_color"],
        bg_color = Configuration_Button_Chart["bg_color"],
        fg_color = fg_color,
        hover = Configuration_Button_Chart["hover"],
        hover_color = hover_color,
        anchor = Configuration_Button_Chart["anchor"],
        text_color=tuple(Configuration_Button_Chart["text_color"]))
    return Frame_Button

# ---------------------------------------------- Fields ----------------------------------------------# 
def Get_Entry_Field(Settings: dict, Configuration:dict, Frame: CTk|CTkFrame, Field_Size: str, Validation: str|None = None) -> CTkEntry:
    Configuration_Field = Configuration["Fields"]["Entry"][f"{Field_Size}"]

    Field = CTkEntry(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Field["width"],
        height = Configuration_Field["height"],
        corner_radius = Configuration_Field["corner_radius"],
        border_width = Configuration_Field["border_width"],
        border_color = tuple(Configuration_Field["border_color"]),
        bg_color = Configuration_Field["bg_color"],
        fg_color = tuple(Configuration_Field["fg_color"]),
        text_color = tuple(Configuration_Field["text_color"]),
        placeholder_text_color = tuple(Configuration_Field["placeholder_text_color"]),
        validate="focusout")
    
    if Validation == "Time":
        Field.configure(validatecommand=lambda: Time_Validate(Settings=Settings, Value=Field.get()))
    elif Validation == "Date":
        Field.configure(validatecommand=lambda: Date_Validate(Settings=Settings, Value=Field.get()))
    elif Validation == "Integer":
        Field.configure(validatecommand=lambda: Int_Validate(Settings=Settings, Value=Field.get()))
    elif Validation == "Float":
        Field.configure(validatecommand=lambda: Float_Validate(Settings=Settings, Value=Field.get()))
    else:
        pass

    return Field

def Get_Password_Normal(Configuration:dict, Frame: CTk|CTkFrame) -> CTkEntry:
    Configuration_Password_Normal = Configuration["Fields"]["Entry"]["Normal"]

    Password_Normal = CTkEntry(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Password_Normal["width"],
        height = Configuration_Password_Normal["height"],
        corner_radius = Configuration_Password_Normal["corner_radius"],
        border_width = Configuration_Password_Normal["border_width"],
        border_color = tuple(Configuration_Password_Normal["border_color"]),
        bg_color = Configuration_Password_Normal["bg_color"],
        fg_color = tuple(Configuration_Password_Normal["fg_color"]),
        text_color = tuple(Configuration_Password_Normal["text_color"]),
        placeholder_text_color = tuple(Configuration_Password_Normal["placeholder_text_color"]),
        show="*")
    return Password_Normal

def Get_RadioButton_Normal(Configuration:dict, Frame: CTk|CTkFrame, Var_Value: int|str) -> CTkRadioButton:
    Configuration_RadioButton_Normal = Configuration["Fields"]["RadioButton"]["Normal"]
    
    fg_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_RadioButton_Normal["fg_color"])
    hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_RadioButton_Normal["hover_color"], Accent_Color=fg_color)

    RadioButton_Normal = CTkRadioButton(
        master = Frame,
        width = Configuration_RadioButton_Normal["width"],
        height = Configuration_RadioButton_Normal["height"],
        radiobutton_width = Configuration_RadioButton_Normal["radiobutton_width"],
        radiobutton_height = Configuration_RadioButton_Normal["radiobutton_height"],
        corner_radius = Configuration_RadioButton_Normal["corner_radius"],
        border_width_unchecked = Configuration_RadioButton_Normal["border_width_unchecked"],
        border_width_checked = Configuration_RadioButton_Normal["border_width_checked"],
        fg_color = fg_color,
        border_color = tuple(Configuration_RadioButton_Normal["border_color"]),
        hover_color = hover_color,
        hover = Configuration_RadioButton_Normal["hover"], 
        value=Var_Value)
    return RadioButton_Normal

def Get_Option_Menu(Configuration:dict, Frame: CTk|CTkFrame) -> CTkOptionMenu:
    # Base CTkOptionMenu
    Configuration_Base_Option_Menu = Configuration["Fields"]["OptionMenu"]["BaseCTk"]["Normal"]
    
    button_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Base_Option_Menu["button_color"])
    button_hover_color_base = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Base_Option_Menu["button_hover_color"], Accent_Color=button_color)
    dropdown_hover_color_base = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Base_Option_Menu["dropdown_hover_color"], Accent_Color=button_color)

    Base_Option_Menu = CTkOptionMenu(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Base_Option_Menu["width"],
        height = Configuration_Base_Option_Menu["height"],
        corner_radius = Configuration_Base_Option_Menu["corner_radius"],
        bg_color = Configuration_Base_Option_Menu["bg_color"],
        fg_color = tuple(Configuration_Base_Option_Menu["fg_color"]),
        button_color = button_color,
        button_hover_color = button_hover_color_base,
        text_color = tuple(Configuration_Base_Option_Menu["text_color"]),
        text_color_disabled = tuple(Configuration_Base_Option_Menu["text_color_disabled"]),
        dropdown_fg_color = tuple(Configuration_Base_Option_Menu["dropdown_fg_color"]),
        dropdown_hover_color = dropdown_hover_color_base,
        dropdown_text_color = tuple(Configuration_Base_Option_Menu["dropdown_text_color"]),
        hover = Configuration_Base_Option_Menu["hover"],
        dynamic_resizing = Configuration_Base_Option_Menu["dynamic_resizing"],
        anchor = Configuration_Base_Option_Menu["anchor"])
    
    return Base_Option_Menu

def Get_Option_Menu_Advance(Configuration:dict, attach: CTkOptionMenu|CTkComboBox|CTkLabel|CTkButton, values: list, command: any) -> CTkScrollableDropdown:
    # Advance CTkScrollableDropdown
    Configuration_Advance_Option_Menu = Configuration["Fields"]["OptionMenu"]["AdvancedCTk"]["Normal"]

    Accent_Color_help = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Advance_Option_Menu["fg_color"])
    scrollbar_button_hover_color_advance = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Advance_Option_Menu["scrollbar_button_hover_color"], Accent_Color=Accent_Color_help)
    hover_color_advance = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Advance_Option_Menu["hover_color"], Accent_Color=Accent_Color_help)

    Advance_Option_Menu = CTkScrollableDropdown(
        attach = attach,
        values = values,
        image_values = Configuration_Advance_Option_Menu["image_values"],
        width = Configuration_Advance_Option_Menu["width"],
        height = Configuration_Advance_Option_Menu["height"],
        fg_color = tuple(Configuration_Advance_Option_Menu["fg_color"]),
        button_color = tuple(Configuration_Advance_Option_Menu["button_color"]),
        hover_color = hover_color_advance,
        text_color = tuple(Configuration_Advance_Option_Menu["text_color"]),
        button_height = Configuration_Advance_Option_Menu["button_height"],
        justify = Configuration_Advance_Option_Menu["justify"],
        frame_corner_radius = Configuration_Advance_Option_Menu["frame_corner_radius"],
        frame_border_width = Configuration_Advance_Option_Menu["frame_border_width"],
        frame_border_color = tuple(Configuration_Advance_Option_Menu["frame_border_color"]),
        scrollbar = Configuration_Advance_Option_Menu["scrollbar"],
        scrollbar_button_color = tuple(Configuration_Advance_Option_Menu["scrollbar_button_color"]),
        scrollbar_button_hover_color = scrollbar_button_hover_color_advance,
        resize = Configuration_Advance_Option_Menu["resize"],
        autocomplete = Configuration_Advance_Option_Menu["autocomplete"],
        alpha = Configuration_Advance_Option_Menu["alpha"],
        command = command)

    return Advance_Option_Menu

def Get_CheckBox(Configuration:dict, Frame: CTk|CTkFrame) -> CTkCheckBox:
    Configuration_Check_Box = Configuration["Fields"]["CheckBox"]["Normal"]
    
    fg_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Check_Box["fg_color"])
    hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Check_Box["hover_color"], Accent_Color=fg_color)

    Check_Box = CTkCheckBox(
        master = Frame,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Check_Box["width"],
        height = Configuration_Check_Box["height"],
        checkbox_width = Configuration_Check_Box["checkbox_width"],
        checkbox_height = Configuration_Check_Box["checkbox_height"],
        corner_radius = Configuration_Check_Box["corner_radius"],
        border_width = Configuration_Check_Box["border_width"],
        border_color = tuple(Configuration_Check_Box["border_color"]),
        bg_color = Configuration_Check_Box["bg_color"],
        fg_color = fg_color,
        hover_color = hover_color,
        checkmark_color = tuple(Configuration_Check_Box["checkmark_color"]),
        text_color = tuple(Configuration_Check_Box["text_color"]),
        hover = Configuration_Check_Box["hover"])
    return Check_Box
    


# ---------------------------------------------- Frames ----------------------------------------------# 
# NonScrollable
def Get_Frame(Configuration:dict, Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_NonScrollable = Configuration["Frames"]["Page_Frames"][f"{Frame_Size}"]

    Frame_NonScrollable = CTkFrame(
        master = Frame,
        width = Configuration_NonScrollable["width"],
        height = Configuration_NonScrollable["height"],
        corner_radius = Configuration_NonScrollable["corner_radius"],
        border_width = Configuration_NonScrollable["border_width"],
        border_color = tuple(Configuration_NonScrollable["border_color"]),
        bg_color = Configuration_NonScrollable["bg_color"],
        fg_color = Configuration_NonScrollable["fg_color"])
    return Frame_NonScrollable

def Get_SideBar_Frame(Configuration:dict, Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_SideBar = Configuration["Frames"]["Page_Frames"][f"{Frame_Size}"]

    fg_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_SideBar["fg_color"])

    Frame_NonScrollable = CTkFrame(
        master = Frame,
        width = Configuration_SideBar["width"],
        height = Configuration_SideBar["height"],
        corner_radius = Configuration_SideBar["corner_radius"],
        border_width = Configuration_SideBar["border_width"],
        border_color = tuple(Configuration_SideBar["border_color"]),
        bg_color = Configuration_SideBar["bg_color"],
        fg_color = fg_color)
    return Frame_NonScrollable

def Get_Dashboards_Frame(Configuration:dict, Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_Dashboard = Configuration["Frames"]["Dashboard"]["Background_Frames"][f"{Frame_Size}"]

    Frame_NonScrollable = CTkFrame(
        master = Frame,
        width = Configuration_Dashboard["width"],
        height = Configuration_Dashboard["height"],
        corner_radius = Configuration_Dashboard["corner_radius"],
        border_width = Configuration_Dashboard["border_width"],
        border_color = tuple(Configuration_Dashboard["border_color"]),
        bg_color = Configuration_Dashboard["bg_color"],
        fg_color = Configuration_Dashboard["fg_color"])
    return Frame_NonScrollable

# ------------------------------------------------------------------------------------------------------------ Widgets  ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------ Dashboards Widgets Frames ------------------------------------------#
def Get_Dashboard_Widget_Frame_Body(Configuration:dict, Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Body = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Body"]

    Frame_Body = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Body["width"],
        height = Configuration_Frame_Dash_Body["height"],
        corner_radius = Configuration_Frame_Dash_Body["corner_radius"],
        border_width = Configuration_Frame_Dash_Body["border_width"],
        border_color = tuple(Configuration_Frame_Dash_Body["border_color"]),
        bg_color = Configuration_Frame_Dash_Body["bg_color"],
        fg_color = tuple(Configuration_Frame_Dash_Body["fg_color"]))
    return Frame_Body

def Get_Dashboard_Widget_Frame_Body_Scrollable(Configuration:dict, Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkScrollableFrame:
    Configuration_Frame_Dash_Body_Scroll = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Body_Scrollable"]
    
    Accent_Color_help = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Frame_Dash_Body_Scroll["Accent_Color_help"])
    scrollbar_button_hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Frame_Dash_Body_Scroll["scrollbar_button_hover_color"], Accent_Color=Accent_Color_help)

    Frame_Body_Scroll = CTkScrollableFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Body_Scroll["width"],
        height = Configuration_Frame_Dash_Body_Scroll["height"],
        corner_radius = Configuration_Frame_Dash_Body_Scroll["corner_radius"],
        border_width = Configuration_Frame_Dash_Body_Scroll["border_width"],
        border_color = tuple(Configuration_Frame_Dash_Body_Scroll["border_color"]),
        bg_color = Configuration_Frame_Dash_Body_Scroll["bg_color"],
        fg_color = tuple(Configuration_Frame_Dash_Body_Scroll["fg_color"]),
        scrollbar_fg_color = Configuration_Frame_Dash_Body_Scroll["scrollbar_fg_color"],
        scrollbar_button_color = tuple(Configuration_Frame_Dash_Body_Scroll["scrollbar_button_color"]),
        scrollbar_button_hover_color = scrollbar_button_hover_color)
    return Frame_Body_Scroll

def Get_Dashboard_Widget_Frame_Header(Configuration:dict, Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Header = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Header"]

    Frame_Header = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Header["width"],
        height = Configuration_Frame_Dash_Header["height"],
        corner_radius = Configuration_Frame_Dash_Header["corner_radius"],
        border_width = Configuration_Frame_Dash_Header["border_width"],
        bg_color = Configuration_Frame_Dash_Header["bg_color"],
        fg_color = Configuration_Frame_Dash_Header["fg_color"])
    return Frame_Header

def Get_Dashboard_Widget_Frame_Area(Configuration:dict, Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Data = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Data_Area"]

    Frame_Area = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Data["width"],
        height = Configuration_Frame_Dash_Data["height"],
        corner_radius = Configuration_Frame_Dash_Data["corner_radius"],
        border_width = Configuration_Frame_Dash_Data["border_width"],
        bg_color = Configuration_Frame_Dash_Data["bg_color"],
        fg_color = Configuration_Frame_Dash_Data["bg_color"])
    return Frame_Area

# ------------------------------------------ Widget Frames ------------------------------------------#
# Scrollable --> Frames For tables
def Get_Widget_Scrollable_Frame(Configuration:dict, Frame: CTk|CTkFrame, Frame_Size: str) -> CTkScrollableFrame:
    Configuration_Scrollable = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"][f"{Frame_Size}"]

    Accent_Color_help = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Scrollable["Accent_Color_help"])
    scrollbar_button_hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Scrollable["scrollbar_button_hover_color"], Accent_Color=Accent_Color_help)

    Frame_Scrollable = CTkScrollableFrame(
        master = Frame,
        width = Configuration_Scrollable["width"],
        corner_radius = Configuration_Scrollable["corner_radius"],
        border_width = Configuration_Scrollable["border_width"],
        border_color = tuple(Configuration_Scrollable["border_color"]),
        bg_color = Configuration_Scrollable["bg_color"],
        fg_color = Configuration_Scrollable["fg_color"],
        scrollbar_fg_color = Configuration_Scrollable["scrollbar_fg_color"],
        scrollbar_button_color = tuple(Configuration_Scrollable["scrollbar_button_color"]),
        scrollbar_button_hover_color = scrollbar_button_hover_color)
    return Frame_Scrollable

def Get_Widget_Frame_Body(Configuration:dict, Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Body"]

    Frame_Single_Column = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column["width"],
        corner_radius = Configuration_Frame_Single_Column["corner_radius"],
        border_width = Configuration_Frame_Single_Column["border_width"],
        border_color = Configuration_Frame_Single_Column["border_color"],
        bg_color = Configuration_Frame_Single_Column["bg_color"],
        fg_color = tuple(Configuration_Frame_Single_Column["fg_color"]))
    return Frame_Single_Column

def Get_Widget_Frame_Header(Configuration:dict, Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column_Header = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Header"]

    Frame_Single_Column_Header = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column_Header["width"],
        height = Configuration_Frame_Single_Column_Header["height"],
        corner_radius = Configuration_Frame_Single_Column_Header["corner_radius"],
        border_width = Configuration_Frame_Single_Column_Header["border_width"],
        bg_color = Configuration_Frame_Single_Column_Header["bg_color"],
        fg_color = Configuration_Frame_Single_Column_Header["fg_color"])
    return Frame_Single_Column_Header

def Get_Widget_Frame_Area(Configuration:dict, Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column_Data_Area = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Data_Area"]

    Frame_Single_Column = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column_Data_Area["width"],
        corner_radius = Configuration_Frame_Single_Column_Data_Area["corner_radius"],
        border_width = Configuration_Frame_Single_Column_Data_Area["border_width"],
        bg_color = Configuration_Frame_Single_Column_Data_Area["bg_color"],
        fg_color = Configuration_Frame_Single_Column_Data_Area["fg_color"])
    return Frame_Single_Column

# ------------------------------------------ Widget Field Frames ------------------------------------------#
def Get_Widget_Field_Frame_Area(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Area = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Area"]

    Frame_Field_Single_Area = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Area["width"],
        height = Configuration_Field_Single_Area["height"],
        corner_radius = Configuration_Field_Single_Area["corner_radius"],
        border_width = Configuration_Field_Single_Area["border_width"],
        bg_color = Configuration_Field_Single_Area["bg_color"],
        fg_color = Configuration_Field_Single_Area["fg_color"])
    return Frame_Field_Single_Area

def Get_Widget_Field_Frame_Label(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Label = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Label"]

    Frame_Field_Single_Label = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Label["width"],
        height = Configuration_Field_Single_Label["height"],
        corner_radius = Configuration_Field_Single_Label["corner_radius"],
        border_width = Configuration_Field_Single_Label["border_width"],
        bg_color = Configuration_Field_Single_Label["bg_color"],
        fg_color = Configuration_Field_Single_Label["fg_color"])
    return Frame_Field_Single_Label

def Get_Widget_Field_Frame_Space(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Space = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Space"]

    Frame_Field_Single_Space = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Space["width"],
        height = Configuration_Field_Single_Space["height"],
        corner_radius = Configuration_Field_Single_Space["corner_radius"],
        border_width = Configuration_Field_Single_Space["border_width"],
        bg_color = Configuration_Field_Single_Space["bg_color"],
        fg_color = Configuration_Field_Single_Space["fg_color"])
    return Frame_Field_Single_Space

def Get_Widget_Field_Frame_Value(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Value = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Value"]

    Frame_Field_Single_Value = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Value["width"],
        height = Configuration_Field_Single_Value["height"],
        corner_radius = Configuration_Field_Single_Value["corner_radius"],
        border_width = Configuration_Field_Single_Value["border_width"],
        bg_color = Configuration_Field_Single_Value["bg_color"],
        fg_color = Configuration_Field_Single_Value["fg_color"])
    return Frame_Field_Single_Value

# ------------------------------------------ Tab View ------------------------------------------ 
def Get_Tab_View(Configuration:dict, Frame: CTk|CTkFrame, Tab_size: str) -> CTkTabview:
    Configuration_TabView_Normal = Configuration["TabView"][f"{Tab_size}"]
    
    segmented_button_selected_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_TabView_Normal["segmented_button_selected_color"])
    segmented_button_selected_hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_TabView_Normal["segmented_button_selected_hover_color"], Accent_Color=segmented_button_selected_color)
    segmented_button_unselected_hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_TabView_Normal["segmented_button_unselected_hover_color"], Accent_Color=segmented_button_selected_color)

    TabView_Normal = CTkTabview(
        master = Frame,
        width = Configuration_TabView_Normal["width"],
        height = Configuration_TabView_Normal["height"],
        corner_radius = Configuration_TabView_Normal["corner_radius"],
        border_width = Configuration_TabView_Normal["border_width"],
        border_color = tuple(Configuration_TabView_Normal["border_color"]),
        bg_color = Configuration_TabView_Normal["bg_color"],
        fg_color = Configuration_TabView_Normal["fg_color"],
        segmented_button_fg_color = Configuration_TabView_Normal["segmented_button_fg_color"],
        segmented_button_selected_color = segmented_button_selected_color,
        segmented_button_selected_hover_color = segmented_button_selected_hover_color,
        segmented_button_unselected_color = tuple(Configuration_TabView_Normal["segmented_button_unselected_color"]),
        segmented_button_unselected_hover_color = segmented_button_unselected_hover_color,
        text_color = tuple(Configuration_TabView_Normal["text_color"]),
        text_color_disabled = tuple(Configuration_TabView_Normal["text_color_disabled"]),
        anchor = Configuration_TabView_Normal["anchor"])
    return TabView_Normal

# ---------------------------------------------- Tables ----------------------------------------------# 
def Get_Table(Configuration:dict, Frame: CTk|CTkFrame, Table_size: str, rows: int, columns: int) -> CTkTable:
    def Colors_Theme_change(colors_rows: list) -> tuple:
        # Will be obsolete if Table will implement Light/Dark colors
        Current_Theme = get_appearance_mode()
        if Current_Theme == "Light":
            color1 = colors_rows[0]
            color2 = lighten_hex_color(hex_color=color1, percentage=25)
        elif Current_Theme == "Dark":
            color1 = colors_rows[1]
            color2 = lighten_hex_color(hex_color=color1, percentage=0.05)
        return tuple([color1, color2])
    
    Configuration_Table_Single = Configuration["Tables"][f"{Table_size}"]
    
    colors_rows = Configuration_Table_Single["colors"]
    colors_rows = Colors_Theme_change(colors_rows=colors_rows)
    header_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Table_Single["header_color"])
    hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Table_Single["hover_color"], Accent_Color=header_color)

    Table_Single = CTkTable(
        master = Frame,
        row = rows,
        column = columns,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        width = Configuration_Table_Single["width"],
        colors = colors_rows,
        border_width = Configuration_Table_Single["border_width"],
        border_color = tuple(Configuration_Table_Single["border_color"]),
        color_phase = Configuration_Table_Single["color_phase"],
        orientation = Configuration_Table_Single["orientation"],
        header_color = header_color,
        corner_radius = Configuration_Table_Single["corner_radius"],
        hover_color = hover_color,
        wraplength = Configuration_Table_Single["wraplength"],
        justify = Configuration_Table_Single["justify"],
        anchor = Configuration_Table_Single["anchor"])
    return Table_Single

# ---------------------------------------------- Icons ----------------------------------------------# 
def Create_Icon(Configuration:dict, Icon_Name: str, Icon_Size: str, Theme_index: int) -> Image:
    # Theme_Index: 0 --> light, 1 --> dark
    Configuration_Icon = Configuration["Icons"][f"{Icon_Size}"]
    
    Icon_Fact = IconFactory(
        icon_set = "lucide",
        icon_size = Configuration_Icon["icon_size"],
        font_size = Configuration_Icon["font_size"],
        font_color = Configuration_Icon["font_color"][Theme_index],
        outline_width = Configuration_Icon["outline_width"],
        outline_color = Configuration_Icon["outline_color"][Theme_index],
        background_color = Configuration_Icon["background_color"][Theme_index],
        background_radius = Configuration_Icon["background_radius"])
    Icon_PIL = Icon_Fact.asPil(Icon_Name)
    return Icon_PIL

def Get_CTk_Icon(Configuration:dict, Icon_Name: str, Icon_Size: str) -> CTkImage:
    Configuration_Icon = Configuration["Icons"][f"{Icon_Size}"]
    Icon_Size_px = Configuration_Icon["icon_size"]
    Picture = CTkImage(
        light_image = Create_Icon(Configuration=Configuration, Icon_Name=Icon_Name, Icon_Size=Icon_Size, Theme_index=0),
        dark_image =Create_Icon(Configuration=Configuration, Icon_Name=Icon_Name, Icon_Size=Icon_Size, Theme_index=1),
        size = (Icon_Size_px, Icon_Size_px))
    return Picture

def Get_Custom_Image(Configuration:dict, Frame: CTk|CTkFrame, Image_Name: str, postfix: str, width: int, heigh: int) -> CTkLabel:
    Picture = CTkImage(
        light_image = Image.open(Defaults_Lists.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\{Image_Name}_Light.{postfix}")),
        dark_image = Image.open(Defaults_Lists.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\{Image_Name}_Dark.{postfix}")),
        size = (width, heigh))
    Background_Image_Label = Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Main", Font_Size="Main")
    Background_Image_Label.configure(image=Picture, text="")
    return Background_Image_Label

# ---------------------------------------------- Progress Bar ----------------------------------------------# 
def Get_ProgressBar(Configuration:dict, Frame: CTk|CTkFrame, orientation: str, Progress_Size: str) -> CTkProgressBar:
    Configuration_ProgressBar = Configuration["ProgressBar"][f"{orientation}"][f"{Progress_Size}"]

    Progress_Bar = CTkProgressBar(
        master = Frame,
        width = Configuration_ProgressBar["width"],
        height = Configuration_ProgressBar["height"],
        border_width = Configuration_ProgressBar["border_width"],
        border_color = tuple(Configuration_ProgressBar["border_color"]),
        corner_radius = Configuration_ProgressBar["corner_radius"],
        bg_color = Configuration_ProgressBar["bg_color"],
        fg_color = tuple(Configuration_ProgressBar["fg_color"]),
        progress_color = tuple(Configuration_ProgressBar["progress_color"]),
        orientation = Configuration_ProgressBar["orientation"],
        determinate_speed = Configuration_ProgressBar["determinate_speed"],
        indeterminate_speed = Configuration_ProgressBar["indeterminate_speed"],
        mode = Configuration_ProgressBar["mode"])
    return Progress_Bar


# ---------------------------------------------- InputDialog ----------------------------------------------# 
def Get_DialogWindow(Configuration:dict, text: str, title: str, Dialog_Type: str) -> CTkInputDialog:
    Configuration_Dialog = Configuration["InputDialog"][f"{Dialog_Type}"]
    
    button_fg_color = Define_Accent_Color(Configuration=Configuration, Color_json=Configuration_Dialog["button_fg_color"])
    button_hover_color = Define_Hover_Color(Configuration=Configuration, Color_json=Configuration_Dialog["button_hover_color"], Accent_Color=button_fg_color)

    Dialog = CTkInputDialog(
        text=text,
        title=title,
        font = Get_Font(Configuration=Configuration, Font_Size="Field_Label"),
        fg_color = tuple(Configuration_Dialog["fg_color"]),
        text_color = tuple(Configuration_Dialog["text_color"]),
        button_fg_color = button_fg_color,
        button_hover_color = button_hover_color,
        button_text_color = tuple(Configuration_Dialog["button_text_color"]),
        entry_fg_color = tuple(Configuration_Dialog["entry_fg_color"]),
        entry_border_color = tuple(Configuration_Dialog["entry_border_color"]),
        entry_text_color = tuple(Configuration_Dialog["entry_text_color"]),
        password = Configuration_Dialog["password"])
    return Dialog

# ---------------------------------------------- Color_Picker ----------------------------------------------# 
def Get_Color_Picker(Configuration:dict, Frame: CTk|CTkFrame, Color_Manual_Frame_Var: CTkEntry) -> CTkColorPicker:
    def Change_Entry_Information(color: str) -> None:
        Color_Manual_Frame_Var.delete(first_index=0, last_index=8)
        Color_Manual_Frame_Var.insert(index=0, string=color)

    def Color_Picker_fg_change(fg_color: list|str) -> str:
        # Will be obsolete if CTkColor_Picker will implement Light/Dark colors
        Current_Theme = get_appearance_mode()
        if type(fg_color) is list:
            if Current_Theme == "Light":
                fg_color = fg_color[0]
            elif Current_Theme == "Dark":
                fg_color = fg_color[1]
        else:
            fg_color = fg_color
        return fg_color
            
    Configuration_Color_Picker = Configuration["Color_Picker"]

    fg_color = Configuration_Color_Picker["fg_color"]
    fg_color = Color_Picker_fg_change(fg_color=fg_color)

    Color_Picker = CTkColorPicker(
        master = Frame,
        width = Configuration_Color_Picker["width"],
        initial_color = Configuration_Color_Picker["initial_color"],
        fg_color = fg_color,
        slider_border = Configuration_Color_Picker["slider_border"],
        corner_radius = Configuration_Color_Picker["corner_radius"],
        command = lambda color: Change_Entry_Information(color=color),
        orientation = Configuration_Color_Picker["orientation"])
    return Color_Picker

# ---------------------------------------------- CTkToolTip ----------------------------------------------# 
def Get_ToolTip(Configuration:dict, widget: any, message: str, ToolTip_Size) -> CTkToolTip:
    Configuration_ToolTip = Configuration["Tooltips"][f"{ToolTip_Size}"]

    ToolTip = CTkToolTip(
        widget = widget,
        message = message,
        delay = Configuration_ToolTip["delay"],
        follow = Configuration_ToolTip["follow"],
        x_offset = Configuration_ToolTip["x_offset"],
        y_offset = Configuration_ToolTip["y_offset"],
        bg_color = Configuration_ToolTip["bg_color"],
        corner_radius = Configuration_ToolTip["corner_radius"],
        border_width = Configuration_ToolTip["border_width"],
        border_color = Configuration_ToolTip["border_color"],
        alpha = Configuration_ToolTip["alpha"],
        padding = tuple(Configuration_ToolTip["padding"]))
    return ToolTip