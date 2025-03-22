# Import Libraries
from datetime import datetime
import calendar

import pyautogui

from customtkinter import CTk, CTkFrame, CTkToplevel, CTkEntry, CTkButton, BooleanVar

import Libs.GUI.Elements as Elements
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Data_Functions as Data_Functions


def Get_Widget_Frame(Configuration:dict, Frame: CTkFrame, Name: str, Additional_Text: str, Widget_size: str, Widget_Label_Tooltip: str, GUI_Level_ID: int|None = None) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Frame_Body(Configuration=Configuration, Frame=Frame, Widget_size=Widget_size, GUI_Level_ID=GUI_Level_ID)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Name}")

    Header_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
    Header_text_Additional.configure(text=f"{Additional_Text}")

    if Widget_Label_Tooltip == "":
        pass
    else:
        Icon_Label_text = Elements.Get_Label_Icon(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Name="circle-help", Icon_Size="Question")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)

    # Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    Header_text.pack(side="left", fill="x")
    if Widget_Label_Tooltip == "":
        pass
    else:
        Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    Header_text_Additional.pack(side="right", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body

def Get_Widget_Scrollable_Frame(Configuration:dict, Frame: CTkFrame, Name: str, Additional_Text: str, Widget_size: str, Widget_Label_Tooltip: str, GUI_Level_ID: int|None = None) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size=Widget_size, GUI_Level_ID=GUI_Level_ID)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Name}")

    Header_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
    Header_text_Additional.configure(text=f"{Additional_Text}")

    if Widget_Label_Tooltip == "":
        pass
    else:
        Icon_Label_text = Elements.Get_Label_Icon(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Name="circle-help", Icon_Size="Question")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)

    # Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    Header_text.pack(side="left", fill="x")
    if Widget_Label_Tooltip == "":
        pass
    else:
        Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    Header_text_Additional.pack(side="right", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body


def Get_Widget_Section_row(Configuration:dict, Frame: CTkFrame, Field_Frame_Type: str, Label: str, Label_Size: str, Font_Size: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Area, Label_Size=Label_Size, Font_Size=Font_Size)
    Label_text.configure(text=f"{Label}")
    # TODO --> dodělat tak aby měl stejný rozložení jako normální pole a 
    Label_text.pack(side="right", fill="none", expand=False, padx=(50, 0), pady=5)

    return Frame_Area

def Get_Widget_Input_row(Settings: dict, Configuration:dict, window: CTk, Frame: CTkFrame, Field_Frame_Type: str, Label: str, Field_Type: str, Var_Value: int|str|None = None,  Validation: str|None = None, Field_ToolTip: list|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")
    if type(Field_ToolTip) == list:
        Elements.Get_ToolTip(Configuration=Configuration, widget=Label_text, message=Field_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=Field_ToolTip[1])
    else:
        pass

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    if Field_Type == "Input_Normal":
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Normal", Validation=Validation)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Password_Normal":
        Field_Normal = Elements.Get_Password_Normal(Configuration=Configuration, Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_Small":
        Field_Small = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Small", Validation=Validation)
        Frame_Area.configure(width=300)
        Field_Small.pack(side="left", fill="none")
    elif Field_Type == "Input_RadioButton":
        RadioButton = Elements.Get_RadioButton_Normal(Configuration=Configuration, Frame=Frame_Value, Var_Value=Var_Value)
        RadioButton.pack(side="left", fill="none")
    elif Field_Type == "Input_OptionMenu":
        Input_OptionMenu = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Value)
        Input_OptionMenu.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_CheckBox":
        Input_Check_Box = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
        Input_Check_Box.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Entry_DropDown":
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Normal", Validation=Validation)
        Button_Drop_Down = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Value, Icon_Name="chevron-down", Icon_Size="Entry_DropDown", Button_Size="Tiny")
        Field_Normal.configure(width = Field_Normal._current_width - Button_Drop_Down._current_width)
        Field_Normal.pack(side="left", fill="x", expand=True)
        Button_Drop_Down.pack(side="left", fill="none", expand=True)
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Field type: {Field_Type} not supported.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    return Frame_Area

def Get_Widget_Button_row(Configuration:dict, Frame: CTkFrame, Field_Frame_Type: str, Buttons_count: int, Button_Size: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Value
    Frame_Buttons = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Buttons.pack_propagate(flag=False)
    Frame_Buttons.pack(side="right", fill="x", expand=True, padx=0, pady=0)

    for Button in range(Buttons_count): 
        Button_Normal = Elements.Get_Button_Text(Configuration=Configuration, Frame=Frame_Buttons, Button_Size=Button_Size)
        Button_Normal.pack(side="right", fill="none", expand=False, padx=(10,0))

    return Frame_Area

def Get_Pop_up_window(Configuration:dict, title: str, max_width: int, max_height: int, Top_middle_point: list, Fixed: bool, Always_on_Top: bool) -> CTkToplevel:
    def drag_win():
        x = Pop_Up_Window.winfo_pointerx() - Pop_Up_Window._offsetx
        y = Pop_Up_Window.winfo_pointery() - Pop_Up_Window._offsety
        Pop_Up_Window.geometry(f"+{x}+{y}")

    def click_win():
        Pop_Up_Window._offsetx = Pop_Up_Window.winfo_pointerx() - Pop_Up_Window.winfo_rootx()
        Pop_Up_Window._offsety = Pop_Up_Window.winfo_pointery() - Pop_Up_Window.winfo_rooty()

    # TopUp Window
    Pop_Up_Window = CTkToplevel()
    Pop_Up_Window.configure(fg_color="#000001")
    Pop_Up_Window.title(title)

    left_position = Top_middle_point[0]
    top_position = Top_middle_point[1]
    Pop_Up_Window.geometry("+%d+%d" % (left_position, top_position))
    Pop_Up_Window.maxsize(width=max_width, height=max_height)

    #Pop_Up_Window.geometry(f"{width}x{height}")
    Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: Pop_Up_Window.destroy())
    Pop_Up_Window.attributes("-topmost", Always_on_Top)
    if Fixed == False:
        Pop_Up_Window.bind(sequence="<Button-1>", func=lambda event:click_win())
        Pop_Up_Window.bind(sequence="<B1-Motion>", func=lambda event:drag_win())
    else:
        pass
    Pop_Up_Window.overrideredirect(boolean=True)
    Pop_Up_Window.iconbitmap(bitmap=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\HQ_Data_Generator.ico"))
    Pop_Up_Window.resizable(width=False, height=False)

    # Rounded corners 
    Pop_Up_Window.config(background="#000001")
    Pop_Up_Window.attributes("-transparentcolor", "#000001")

    return Pop_Up_Window

def My_Dialog_Window(Settings: dict, Configuration:dict, window: CTk, Clicked_on_Button: CTkButton, title: str, text: str, Password: bool, width: int, height: int, Fixed: bool, tooltip: str, GUI_Level_ID: int|None = None) -> CTkFrame:
    def Confirm_Choice(Field_Normal: CTkEntry) -> str:
        Dialog_Window.destroy()
        return Field_Normal.get()

    def Reject_Choice(Field_Normal: CTkEntry) -> str:
        Dialog_Window.destroy()
        return ""
    
    def Build_Dialog_Window(text: str, Password: bool) -> None:
        Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
        Label_text.configure(text=f"{text}:")
        Label_text.pack(side="top", fill="none", expand=True, padx=10, pady=5)

        if Password == False:
            Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Size="Normal")
            Field_Normal.pack(side="top", fill="none", expand=True, padx=10, pady=5)
        elif Password == True:
            Field_Normal = Elements.Get_Password_Normal(Configuration=Configuration, Frame=Frame_Body)
            Field_Normal.pack(side="top", fill="none", expand=True, padx=10, pady=5)

        # Buttons
        Button_Frame = Get_Widget_Button_row(Frame=Frame_Body, Configuration=Configuration, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Normal") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda Field_Normal=Field_Normal:Confirm_Choice(Field_Normal=Field_Normal))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)
        Button_Confirm_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)

        Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
        Button_Reject_Var.configure(text="Reject", command = lambda Field_Normal=Field_Normal:Reject_Choice(Field_Normal=Field_Normal))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Reject.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)
        Button_Reject_Var.pack(side="right", fill="none", expand=True, padx=5, pady=5)

    Dialog_Window_geometry = (width, height)
    Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on_Button, New_Window_width=Dialog_Window_geometry[0])
    Dialog_Window =  Get_Pop_up_window(Configuration=Configuration, title=title, max_width=Dialog_Window_geometry[0], max_height=Dialog_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=Fixed, Always_on_Top=False)

    # Frame - General
    Frame_Main = Get_Widget_Frame(Configuration=Configuration, Frame=Dialog_Window, Name=title, Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip=tooltip, GUI_Level_ID=GUI_Level_ID)
    Frame_Main.configure(bg_color = "#000001")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Build_Dialog_Window(text=text, Password=Password)

    
def My_Date_Picker(Settings: dict, Configuration:dict, date_entry: CTkEntry, Clicked_on_Button: CTkButton, width: int, height: int, Fixed: bool, GUI_Level_ID: int|None = None) -> None:
    # Based on https://github.com/maxverwiebe/CTkDatePicker

    Current_Year = datetime.now().year
    Current_Month = datetime.now().month
    Current_Day = datetime.now().day
    Date_format = Settings["0"]["General"]["Formats"]["Date"]

    def prev_month(Shown_Month: int, Shown_Year: int):
        if Shown_Month == 1:
            Shown_Month = 12
            Shown_Year -= 1
        else:
            Shown_Month -= 1
        build_calendar(Shown_Month=Shown_Month, Shown_Year=Shown_Year)

    def next_month(Shown_Month: int, Shown_Year: int):
        if Shown_Month == 12:
            Shown_Month = 1
            Shown_Year += 1
        else:
            Shown_Month += 1
        build_calendar(Shown_Month=Shown_Month, Shown_Year=Shown_Year)

    def select_date(date_entry: CTkEntry, Selected_year: int, Selected_month: int, Selected_day: int):
        selected_date = datetime(Selected_year, Selected_month, Selected_day)
        # Temporarily enable the entry to set the date
        date_entry.configure(state='normal')
        date_entry.delete(0, 30)
        date_entry.insert(0, selected_date.strftime(Date_format))
        date_entry.focus_force()
        pyautogui.press("tab") 
        Picker_window.destroy()

    def build_calendar(Shown_Month: int, Shown_Year: int) -> None:
        calendar_frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="DatePicker", GUI_Level_ID=GUI_Level_ID + 1)
        calendar_frame.grid(row=0, column=0)

        # Month and Year Selector
        month_label = Elements.Get_Label(Configuration=Configuration, Frame=calendar_frame, Label_Size="Field_Label", Font_Size="Field_Label")
        month_label.configure(text=f"{calendar.month_name[Shown_Month]}, {Shown_Year}")
        month_label.grid(row=0, column=1, columnspan=5)

        prev_month_button = Elements.Get_Button_Text(Configuration=Configuration, Frame=calendar_frame, Button_Size="Tiny")
        prev_month_button.configure(text="<", command=lambda: prev_month(Shown_Month=Shown_Month, Shown_Year=Shown_Year))
        prev_month_button.grid(row=0, column=0)

        next_month_button = Elements.Get_Button_Text(Configuration=Configuration, Frame=calendar_frame, Button_Size="Tiny")
        next_month_button.configure(text=">", command=lambda: next_month(Shown_Month=Shown_Month, Shown_Year=Shown_Year))
        next_month_button.grid(row=0, column=6)

        # Days of the week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            lbl = Elements.Get_Label(Configuration=Configuration, Frame=calendar_frame, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
            lbl.configure(text=day)
            lbl.grid(row=1, column=i)

        # Days in month
        month_days = calendar.monthrange(Shown_Year, Shown_Month)[1]
        start_day = calendar.monthrange(Shown_Year, Shown_Month)[0]
        day = 1
        for week in range(2, 8):
            for day_col in range(7):
                if week == 2 and day_col < start_day:
                    lbl = Elements.Get_Label(Configuration=Configuration, Frame=calendar_frame, Label_Size="Field_Label", Font_Size="Field_Label")
                    lbl.configure(text=f"")
                    lbl.grid(row=week, column=day_col)
                elif day > month_days:
                    lbl = Elements.Get_Label(Configuration=Configuration, Frame=calendar_frame, Label_Size="Field_Label", Font_Size="Field_Label")
                    lbl.configure(text=f"")
                    lbl.grid(row=week, column=day_col)
                else:
                    btn = Elements.Get_Button_Text(Configuration=Configuration, Frame=calendar_frame, Button_Size="DatePicker_Days")
                    # Today with red color
                    if (Shown_Year==Current_Year) and (Shown_Month==Current_Month) and (day==Current_Day):
                        btn.configure(text_color="#FF9797")
                    else:
                        pass
                    btn.configure(text=str(day), command=lambda day=day: select_date(date_entry=date_entry, Selected_year=Shown_Year, Selected_month=Shown_Month, Selected_day=day))
                    btn.grid(row=week, column=day_col)
                    day += 1

    Picker_window_geometry = (width, height)
    Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on_Button, New_Window_width=Picker_window_geometry[0])
    Picker_window = Get_Pop_up_window(Configuration=Configuration, title="Date Picker", max_width=Picker_window_geometry[0], max_height=Picker_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=Fixed, Always_on_Top=True)

    # Frame - General
    Frame_Main = Get_Widget_Frame(Configuration=Configuration, Frame=Picker_window, Name="Date Picker", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Select date from calendar", GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Main.configure(bg_color = "#000001")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    build_calendar(Shown_Month=Current_Month, Shown_Year=Current_Year)

# ------------------------------------- Only HQ Data Testing Tool ------------------------------------- #
def Get_Prompt_Free_Of_Charge_Description_row(Settings: dict, Configuration:dict, Frame: CTkFrame, Field_Frame_Type: str, Validation: str|None = None, Field_ToolTip: list|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.configure(width=100)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"")
    Label_text.pack(side="right", fill="none")
    if type(Field_ToolTip) == list:
        Elements.Get_ToolTip(Configuration=Configuration, widget=Label_text, message=Field_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=Field_ToolTip[1])
    else:
        pass

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Item_No_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Item_No_text.configure(text="Item No")

    Item_Description_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Item_Description_text.configure(text="Description")

    Item_Qty_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Item_Qty_text.configure(text="Qty")

    Item_Price_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Item_Price_text.configure(text="Price")
    
    Item_No_text.pack(side="left", fill="x", expand=False, padx=(15, 0), pady=0)
    Item_Description_text.pack(side="left", fill="x", expand=False, padx=(47, 0), pady=0)
    Item_Qty_text.pack(side="left", fill="x", expand=False, padx=(46, 0), pady=0)
    Item_Price_text.pack(side="left", fill="x", expand=False, padx=(28, 0), pady=0)

    return Frame_Area

def Get_Prompt_Free_Of_Charge_row(Settings: dict, Configuration:dict, window: CTk, Frame: CTkFrame, Field_Frame_Type: str, Label: str, Validation: str|None = None, Field_ToolTip: list|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.configure(width=100)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")
    if type(Field_ToolTip) == list:
        Elements.Get_ToolTip(Configuration=Configuration, widget=Label_text, message=Field_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=Field_ToolTip[1])
    else:
        pass

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Item_Number = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Tiny")
    Item_Number.configure(width=50)
    Item_Description = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Tiny", Validation=Validation)
    Item_Description.configure(width=100)
    Item_Qty_per_Machine = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Tiny", Validation="Integer")
    Item_Qty_per_Machine.configure(width=10)
    Item_Price = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Tiny", Validation="Float")
    Item_Price.configure(width=20)
    
    Item_Number.pack(side="left", fill="x", expand=True, padx=5, pady=0)
    Item_Description.pack(side="left", fill="x", expand=True, padx=5, pady=0)
    Item_Qty_per_Machine.pack(side="left", fill="x", expand=True, padx=5, pady=0)
    Item_Price.pack(side="left", fill="x", expand=True, padx=5, pady=0)

    return Frame_Area

def Get_Prompt_Line_Flags_Description_row(Settings: dict, Configuration:dict, Frame: CTkFrame, Field_Frame_Type: str, Validation: str|None = None, Field_ToolTip: list|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.configure(width=130)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"")
    Label_text.pack(side="right", fill="none")
    if type(Field_ToolTip) == list:
        Elements.Get_ToolTip(Configuration=Configuration, widget=Label_text, message=Field_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=Field_ToolTip[1])
    else:
        pass

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Substitution_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Substitution_text.configure(text="Substitution")

    Substitution_Item_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Substitution_Item_text.configure(text="Sub. Item")

    Cancel_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Cancel_text.configure(text="Cancel")

    Finished_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Finished_text.configure(text="Finished")
    
    Substitution_text.pack(side="left", fill="x", expand=True, padx=5, pady=0)
    Substitution_Item_text.pack(side="left", fill="x", expand=True, padx=5, pady=0)
    Cancel_text.pack(side="left", fill="x", expand=True, padx=5, pady=0)
    Finished_text.pack(side="left", fill="x", expand=True, padx=5, pady=0)

    return Frame_Area


def Get_Prompt_Line_Flags_row(Settings: dict, Configuration:dict, window: CTk, Frame: CTkFrame, Field_Frame_Type: str, Label: str, Item_Substituted: bool, Item_No_Substituted: str, Item_Finished: bool, Validation: str|None = None, Field_ToolTip: list|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.configure(width=130)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")
    if type(Field_ToolTip) == list:
        Elements.Get_ToolTip(Configuration=Configuration, widget=Label_text, message=Field_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=Field_ToolTip[1])
    else:
        pass

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Use_Substitution = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
    Use_Substitution.configure(width=30, text="")  
    Sub_Item_No = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Tiny", Validation=Validation)
    Sub_Item_No.configure(width=90)
    if Item_Substituted == True:
        Use_Substitution.select()
        Sub_Item_No.insert(index=0, string=Item_No_Substituted)
    else:
        Use_Substitution.deselect()
    Use_Cancel = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
    Use_Cancel.configure(width=30, text="")
    Use_Finished = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
    Use_Finished.configure(width=30, text="")
    if Item_Finished == True:
        Use_Finished.select()
    else:
        Use_Finished.deselect()

    Use_Substitution.pack(side="left", fill="x", expand=False, padx=(45, 0), pady=0)
    Sub_Item_No.pack(side="left", fill="x", expand=False, padx=(22, 0), pady=0)
    Use_Cancel.pack(side="left", fill="x", expand=False, padx=(24, 0), pady=0)
    Use_Finished.pack(side="left", fill="x", expand=False, padx=(45, 0), pady=0)

    return Frame_Area

def Get_Prompt_Delivery_Assignment(Settings: dict, Configuration:dict, Frame: CTkFrame, Line_Item_No: str, Line_Item_Desc: str, Line_Qty: int, PO_Delivery_Number_list: list, Validation: str|None = None, Field_ToolTip: list|None = None, GUI_Level_ID: int|None = None) -> CTkFrame: 
    Frame_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Frame_Area.configure(width=700, height=28)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    Item_text_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Area, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Item_text_Frame.pack_propagate(flag=False)
    Item_text_Frame.configure(width=200, height=28)
    Item_text = Elements.Get_Label(Configuration=Configuration, Frame=Item_text_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
    Item_text.configure(text=f"{Line_Item_No}")

    Item_Desc_text_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Area, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Item_Desc_text_Frame.pack_propagate(flag=False)
    Item_Desc_text_Frame.configure(width=300, height=28)
    Item_Desc_text = Elements.Get_Label(Configuration=Configuration, Frame=Item_Desc_text_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
    Item_Desc_text.configure(text=f"{Line_Item_Desc}")

    Line_Qty_Text_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Area, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Line_Qty_Text_Frame.pack_propagate(flag=False)
    Line_Qty_Text_Frame.configure(width=20, height=28)
    Line_Qty_Text = Elements.Get_Label(Configuration=Configuration, Frame=Line_Qty_Text_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
    Line_Qty_Text.configure(text=f"{Line_Qty}")

    Input_OptionMenu_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Area, Frame_Size="Work_Area_Columns", GUI_Level_ID=GUI_Level_ID)
    Input_OptionMenu_Frame.pack_propagate(flag=False)
    Input_OptionMenu_Frame.configure(width=200, height=28)
    Input_OptionMenu = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Input_OptionMenu_Frame)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Input_OptionMenu, values=PO_Delivery_Number_list, command=None, GUI_Level_ID=3)

    Item_text_Frame.pack(side="left", fill="none", expand=False, padx=5, pady=0)
    Item_Desc_text_Frame.pack(side="left", fill="none", expand=False, padx=5, pady=0)
    Line_Qty_Text_Frame.pack(side="left", fill="none", expand=False, padx=5, pady=0)
    Input_OptionMenu_Frame.pack(side="left", fill="none", expand=False, padx=5, pady=0)

    Item_text.pack(side="left", fill="x", expand=False, padx=0, pady=0)
    Item_Desc_text.pack(side="left", fill="x", expand=False, padx=0, pady=0)
    Line_Qty_Text.pack(side="left", fill="x", expand=False, padx=0, pady=0)
    Input_OptionMenu.pack(side="left", fill="x", expand=False, padx=0, pady=0)

    return Frame_Area