from datetime import datetime
import calendar

from customtkinter import CTk, CTkFrame, CTkToplevel, BooleanVar, StringVar, IntVar

import Libs.GUI.Elements as Elements
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions

# -------------------------------------------------------------------------------- WidgetRow_Input_Entry -------------------------------------------------------------------------------- #
class WidgetRow_Input_Entry:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Field_Size", "Label", "Save_To", "Save_path", "Documents", "placeholder_text", "placeholder_text_color", "Label_ToolTip", "Validation", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Input_Entry", "Time_Format", "Value", "Date_Format", "Local_function_list", "Can_Save"
    """
    Field row for Entry
    """
    def __init__(self, Settings: dict|None, 
                 Configuration: dict|None, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Field_Size: str,
                 Label: str, 
                 Value: str|int|float = "",
                 Save_To: str|None = None,
                 Save_path: list|None = None,
                 Documents: dict|None = None,
                 placeholder_text: str|None = None, 
                 placeholder_text_color: str = "", 
                 Label_ToolTip: list|None = None, 
                 Local_function_list: any = None,
                 Validation: str|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Field_Size = Field_Size
        self.Label = Label
        self.Value = Value
        self.Label_ToolTip = Label_ToolTip
        self.placeholder_text = placeholder_text
        self.placeholder_text_color = placeholder_text_color
        self.Validation = Validation
        self.Save_To = Save_To 
        self.Save_path = Save_path
        self.Local_function_list = Local_function_list

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        if self.Field_Size == "Normal":
            self.Input_Entry = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value, Field_Size="Normal", Validation=self.Validation)
        elif self.Field_Size == "Small":
            self.Input_Entry = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value, Field_Size="Small", Validation=self.Validation)
        elif self.Field_Size == "Tiny":
            self.Input_Entry = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value, Field_Size="Tiny", Validation=self.Validation)
        elif self.Field_Size == "Password":
            self.Input_Entry = Elements.Get_Password_Normal(Configuration=Configuration, Frame=self.Frame_Value)

        # Insert Value
        if type(self.Value) == str:
            if self.Value != "":
                self.Input_Entry.delete(first_index=0, last_index=1000)
                self.Input_Entry.insert(index=0, string=self.Value)
            else:
                pass
        elif type(self.Value) == int:
            self.Input_Entry.delete(first_index=0, last_index=1000)
            self.Input_Entry.insert(index=0, string=self.Value)
        elif type(self.Value) == float:
            self.Input_Entry.delete(first_index=0, last_index=1000)
            self.Input_Entry.insert(index=0, string=self.Value)
        else:
            pass

        # PlaceHolder
        if placeholder_text_color == "":
            self.Input_Entry.configure(placeholder_text=self.placeholder_text)
        else:
            self.Input_Entry.configure(placeholder_text=self.placeholder_text, placeholder_text_color=self.placeholder_text_color)
        self.Input_Entry.bind("<FocusOut>", lambda Value: self.Save(Value=Value))
        
    def Freeze(self):
        self.Input_Entry.configure(state="disabled")

    def UnFreeze(self):
        self.Input_Entry.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="none", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        self.Input_Entry.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    def Get_Value(self):
        return self.Input_Entry.get()

    def Save(self, Value):
        # Default
        self.Can_Save = True
        self.Value = self.Get_Value()
        self.Time_Format = self.Settings["0"]["General"]["Formats"]["Time"]
        self.Date_Format = self.Settings["0"]["General"]["Formats"]["Date"]

        # Test Validation
        if self.Value != "":
            if self.Validation == "Time":
                try:
                    datetime.strptime(self.Value, self.Time_Format)
                except:
                    Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not proper Time format, should be: {self.Time_Format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    self.Input_Entry.delete(first_index=0, last_index=100)
                    self.Input_Entry.focus()
                    self.Can_Save = False
            elif self.Validation == "Date":
                try:
                    datetime.strptime(self.Value, self.Date_Format)
                except:
                    Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not in proper Date format, should be: {self.Date_Format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    self.Input_Entry.delete(first_index=0, last_index=100)
                    self.Input_Entry.focus()
                    self.Can_Save = False
        else:
            pass

        if self.Validation == "Integer":
            try:
                int(self.Value)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not whole number.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry.delete(first_index=0, last_index=100)
                self.Input_Entry.focus()
                self.Can_Save = False
        elif self.Validation == "Percentage":
            try:
                if (int(self.Value) >= 0) and (int(self.Value) <= 100):
                    pass
                else:
                    raise
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not whole percentage belonging to interval 0 .. 100.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry.delete(first_index=0, last_index=100)
                self.Input_Entry.focus()
                self.Can_Save = False
        elif self.Validation == "Float":
            try:
                float(self.Value)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not float number.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry.delete(first_index=0, last_index=100)
                self.Input_Entry.focus()
                self.Can_Save = False
        else:
            pass

        # Save
        if (self.Save_To == None) or (self.Save_path == None) or (self.Can_Save == False):
            pass
        else:
            if (self.Validation == "Integer") or (self.Validation == "Percentage"):
                Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=int(self.Get_Value()))
            elif self.Validation == "Float":
                Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=float(self.Get_Value()))
            elif self.Validation == "list":
                Information_list = [self.Get_Value()]
                Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=Information_list)
            else:
                Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Get_Value())

        # Run Local Function
        if self.Local_function_list != None:
            for Local_Function in self.Local_function_list:
                Local_Function()

# -------------------------------------------------------------------------------- WidgetRow_Double_Input_Entry -------------------------------------------------------------------------------- #
class WidgetRow_Double_Input_Entry:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Save_To", "Save_path1", "Save_path2", "Documents", "placeholder_text1", "placeholder_text2", "placeholder_text_color", "Label_ToolTip", "Validation1", "Validation2", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value1", "Input_Entry1", "Frame_Space2", "Space_text", "Frame_Value2", "Input_Entry2", "Time_Format", "Value1", "Value2", "Local_function1_list", "Local_function2_list", "Date_Format", "Can_Save1", "Can_Save2"
    """
    Field row for Entry
    """
    def __init__(self, Settings: dict|None, 
                 Configuration: dict|None, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Value1: str|int|float = "",
                 Value2: str|int|float = "",
                 Save_To: str|None = None,
                 Save_path1: list|None = None,
                 Save_path2: list|None = None,
                 Documents: dict|None = None,
                 placeholder_text1: str|None = None, 
                 placeholder_text2: str|None = None, 
                 placeholder_text_color: str = "", 
                 Label_ToolTip: list|None = None,
                 Local_function1_list: any = None,
                 Local_function2_list: any = None, 
                 Validation1: str|None = None,
                 Validation2: str|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Value1 = Value1
        self.Value2 = Value2
        self.Label_ToolTip = Label_ToolTip
        self.placeholder_text1 = placeholder_text1
        self.placeholder_text2 = placeholder_text2
        self.placeholder_text_color = placeholder_text_color
        self.Local_function1_list = Local_function1_list
        self.Local_function2_list = Local_function2_list
        self.Validation1 = Validation1
        self.Validation2 = Validation2
        self.Save_To = Save_To 
        self.Save_path1 = Save_path1
        self.Save_path2 = Save_path2

        # Build one line for two input field
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Frame Label
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        # Frame Space between Label and Value
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)

        # Frame Value1
        self.Frame_Value1 = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Input_Entry1 = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value1, Field_Size="Double_Input", Validation=self.Validation1)

        # Frame Space between Label and Value
        self.Frame_Space2 = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Space_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Space2, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Space_text.configure(text=f"-")

        # Frame Value2
        self.Frame_Value2 = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Input_Entry2 = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value2, Field_Size="Double_Input", Validation=self.Validation2)

        # Insert Value
        if type(self.Value1) == str:
            if self.Value1 != "":
                self.Input_Entry1.delete(first_index=0, last_index=1000)
                self.Input_Entry1.insert(index=0, string=self.Value1)
            else:
                pass
        elif type(self.Value1) == int:
            self.Input_Entry1.delete(first_index=0, last_index=1000)
            self.Input_Entry1.insert(index=0, string=self.Value1)
        elif type(self.Value1) == float:
            self.Input_Entry1.delete(first_index=0, last_index=1000)
            self.Input_Entry1.insert(index=0, string=self.Value)
        else:
            pass

        if type(self.Value2) == str:
            if self.Value2 != "":
                self.Input_Entry2.delete(first_index=0, last_index=1000)
                self.Input_Entry2.insert(index=0, string=self.Value2)
            else:
                pass
        elif type(self.Value2) == int:
            self.Input_Entry2.delete(first_index=0, last_index=1000)
            self.Input_Entry2.insert(index=0, string=self.Value2)
        elif type(self.Value2) == float:
            self.Input_Entry2.delete(first_index=0, last_index=1000)
            self.Input_Entry2.insert(index=0, string=self.Value)
        else:
            pass

        # PlaceHolder
        if placeholder_text_color == "":
            self.Input_Entry1.configure(placeholder_text=self.placeholder_text1)
            self.Input_Entry2.configure(placeholder_text=self.placeholder_text2)
        else:
            self.Input_Entry1.configure(placeholder_text=self.placeholder_text1, placeholder_text_color=self.placeholder_text_color)
            self.Input_Entry2.configure(placeholder_text=self.placeholder_text2, placeholder_text_color=self.placeholder_text_color)

        self.Input_Entry1.bind("<FocusOut>", lambda Value1: self.Save1(Value1=Value1))
        self.Input_Entry2.bind("<FocusOut>", lambda Value2: self.Save2(Value2=Value2))
        

    def Freeze(self):
        self.Input_Entry1.configure(state="disabled")
        self.Input_Entry2.configure(state="disabled")

    def UnFreeze(self):
        self.Input_Entry1.configure(state="normal")
        self.Input_Entry2.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value1.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Input_Entry1.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space2.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Space_text.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value2.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Input_Entry2.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    def Get_Value1(self):
        return self.Input_Entry1.get()

    def Get_Value2(self):
        return self.Input_Entry2.get()

    def Save1(self, Value1):
        # Default
        self.Can_Save1 = True
        self.Value1 = self.Get_Value1()
        self.Time_Format = self.Settings["0"]["General"]["Formats"]["Time"]
        self.Date_Format = self.Settings["0"]["General"]["Formats"]["Date"]
            
        # Test Validation
        if self.Value1 != "":
            if self.Validation1 == "Time":
                try:
                    datetime.strptime(self.Value1, self.Time_Format)
                except:
                    Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value1} in not proper Time format, should be: {self.Time_Format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    self.Input_Entry1.delete(first_index=0, last_index=100)
                    self.Input_Entry1.focus()
                    self.Can_Save1 = False
            elif self.Validation1 == "Date":
                try:
                    datetime.strptime(self.Value1, self.Date_Format)
                except:
                    Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value1} in not in proper Date format, should be: {self.Date_Format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    self.Input_Entry1.delete(first_index=0, last_index=100)
                    self.Input_Entry1.focus()
                    self.Can_Save1 = False
        else:
            pass

        if self.Validation1 == "Integer":
            try:
                int(self.Value1)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value1} in not whole number.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry1.delete(first_index=0, last_index=100)
                self.Input_Entry1.focus()
                self.Can_Save1 = False
        elif self.Validation1 == "Float":
            try:
                float(self.Value1)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value1} in not float number.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry1.delete(first_index=0, last_index=100)
                self.Input_Entry1.focus()
                self.Can_Save1 = False
        else:
            pass

        # Save
        if (self.Save_To == None) or (self.Save_path1 == None) or (self.Can_Save1 == False):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path1, Information=self.Get_Value1())

        # Run Local Function
        if self.Local_function1_list != None:
            for Local_Function1 in self.Local_function1_list:
                Local_Function1()

    def Save2(self, Value2):
        # Default
        self.Can_Save2 = True
        self.Value2 = self.Get_Value2()
        self.Time_Format = self.Settings["0"]["General"]["Formats"]["Time"]
        self.Date_Format = self.Settings["0"]["General"]["Formats"]["Date"]

        # Test Validation
        if self.Value2 != "":
            if self.Validation2 == "Time":
                try:
                    datetime.strptime(self.Value2, self.Time_Format)
                except:
                    Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value2} in not proper Time format, should be: {self.Time_Format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    self.Input_Entry2.delete(first_index=0, last_index=100)
                    self.Input_Entry2.focus()
                    self.Can_Save2 = False
            elif self.Validation2 == "Date":
                try:
                    datetime.strptime(self.Value2, self.Date_Format)
                except:
                    Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value2} in not in proper Date format, should be: {self.Date_Format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                    self.Input_Entry2.delete(first_index=0, last_index=100)
                    self.Input_Entry2.focus()
                    self.Can_Save2 = False
        else:
            pass

        if self.Validation2 == "Integer":
            try:
                int(self.Value2)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value2} in not whole number.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry2.delete(first_index=0, last_index=100)
                self.Input_Entry2.focus()
                self.Can_Save2 = False
        elif self.Validation2 == "Float":
            try:
                float(self.Value2)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value2} in not float number.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Input_Entry2.delete(first_index=0, last_index=100)
                self.Input_Entry2.focus()
                self.Can_Save2 = False
        else:
            pass

        # Save
        if (self.Save_To == None) or (self.Save_path2 == None) or (self.Can_Save2 == False):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path1, Information=self.Get_Value1())

        # Run Local Function
        if self.Local_function2_list != None:
            for Local_Function2 in self.Local_function2_list:
                Local_Function2()

# -------------------------------------------------------------------------------- WidgetRow_OptionMenu -------------------------------------------------------------------------------- #
class WidgetRow_OptionMenu:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Variable", "Values", "Label_ToolTip", "Documents", "Save_To", "Save_path", "Field_list", "Field_Blocking_dict", "Local_function_list", "GUI_Level_ID", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Input_OptionMenu", "Block_Fields_list"
    """
    Field row for OptionMenu
    """
    def __init__(self, 
                 Settings: dict, 
                 Configuration:dict, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Variable: StringVar|IntVar, 
                 Values: list,
                 Label_ToolTip: list|None = None, 
                 Documents: dict|None = None,
                 Save_To: str|None = None,
                 Save_path: list|None = None,
                 Field_list: list|None = None,
                 Field_Blocking_dict: dict|None = None,
                 Local_function_list: any = None,
                 GUI_Level_ID: int|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Label_ToolTip = Label_ToolTip
        self.Variable = Variable
        self.Values = Values
        self.Save_To = Save_To 
        self.Save_path = Save_path 
        self.Field_list = Field_list
        self.Field_Blocking_dict = Field_Blocking_dict
        self.Local_function_list = Local_function_list
        self.GUI_Level_ID = GUI_Level_ID

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        self.Input_OptionMenu = Elements.Get_Option_Menu(Configuration=self.Configuration, Frame=self.Frame_Value)
        self.Input_OptionMenu.configure(variable=self.Variable)
        Elements.Get_Option_Menu_Advance(Configuration=self.Configuration, attach=self.Input_OptionMenu, values=self.Values, command = lambda Value: self.Change_Value(Value=Value), GUI_Level_ID=self.GUI_Level_ID)
        self.Change_Value(Value=self.Get_Value())
      
    def Freeze(self):
        self.Input_OptionMenu.configure(state="disabled")

    def UnFreeze(self):
        self.Input_OptionMenu.configure(state="normal")

    def Change_Value(self, Value):
        # Save
        self.Variable.set(value=Value)
        self.Save()

        # Unfreeze all fields belonging to Field
        if self.Field_list != None:
            for UnFreeze_Field in self.Field_list:
                UnFreeze_Field.UnFreeze()
        else:
            pass

        # Freeze only selected
        if self.Field_Blocking_dict != None:
            # Filter Dictionary
            self.Block_Fields_list = self.Field_Blocking_dict[Value]
            for Freeze_Field in self.Block_Fields_list:
                Freeze_Field.Freeze()
        else:
            pass

        # Run Local Function
        if self.Local_function_list != None:
            for Local_Function in self.Local_function_list:
                Local_Function()

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        self.Input_OptionMenu.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    def Get_Value(self):
        return self.Input_OptionMenu.get()

    def Save(self):
        if (self.Save_To == None) or (self.Save_path == None):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Get_Value())


# -------------------------------------------------------------------------------- WidgetRow_CheckBox -------------------------------------------------------------------------------- #
class WidgetRow_CheckBox:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Variable", "Documents", "Label_ToolTip", "Save_To", "Save_path", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Input_Check_Box", "Field_list", "Field_Blocking_dict", "Block_Fields_list", "Local_function_list"
    """
    Field row for Check Box
    """
    def __init__(self, 
                 Settings: dict, 
                 Configuration:dict, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Variable: BooleanVar, 
                 Documents: dict|None = None,
                 Label_ToolTip: list|None = None, 
                 Save_To: str|None = None,
                 Save_path: list|None = None,
                 Field_list: list|None = None,
                 Field_Blocking_dict: dict|None = None,
                 Local_function_list: any = None,):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Label_ToolTip = Label_ToolTip
        self.Variable = Variable
        self.Save_To = Save_To
        self.Save_path = Save_path 
        self.Field_list = Field_list
        self.Field_Blocking_dict = Field_Blocking_dict
        self.Local_function_list = Local_function_list

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        self.Input_Check_Box = Elements.Get_CheckBox(Configuration=self.Configuration, Frame=self.Frame_Value)
        self.Input_Check_Box.configure(variable=self.Variable, text="", command=lambda: self.Change_Value())
        self.Set_Value()
        self.Change_Value()

    def Freeze(self):
        self.Input_Check_Box.configure(state="disabled")

    def UnFreeze(self):
        self.Input_Check_Box.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="none", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=False, padx=0, pady=0)
        self.Input_Check_Box.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    def Change_Value(self):
        # Save
        self.Save()

        # Unfreeze all fields belonging to Field
        if self.Field_list != None:
            for UnFreeze_Field in self.Field_list:
                UnFreeze_Field.UnFreeze()
        else:
            pass

        # Freeze only selected
        if self.Field_Blocking_dict != None:
            # Filter Dictionary
            self.Block_Fields_list = self.Field_Blocking_dict[self.Variable.get()]
            for Freeze_Field in self.Block_Fields_list:
                Freeze_Field.Freeze()
        else:
            pass

        # Run Local Function
        if self.Local_function_list != None:
            for Local_Function in self.Local_function_list:
                Local_Function()

    def Set_Value(self):
        self.Input_Check_Box.configure(variable=self.Variable)

    def Save(self):
        if (self.Save_To == None) or (self.Save_path == None):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Variable.get())


# -------------------------------------------------------------------------------- WidgetRow_RadioButton -------------------------------------------------------------------------------- #
class WidgetRow_RadioButton:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Variable", "Var_Value", "Documents", "Label_ToolTip", "Save_To", "Save_path", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Input_RadioButton"
    """
    Field row for Check Box
    """
    def __init__(self, 
                 Settings: dict, 
                 Configuration:dict, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Variable: BooleanVar, 
                 Var_Value: int|str,
                 Documents: dict|None = None,
                 Label_ToolTip: list|None = None, 
                 Save_To: str|None = None,
                 Save_path: list|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Label_ToolTip = Label_ToolTip
        self.Variable = Variable
        self.Var_Value = Var_Value
        self.Save_To = Save_To
        self.Save_path = Save_path 

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        self.Input_RadioButton = Elements.Get_RadioButton_Normal(Configuration=self.Configuration, Frame=self.Frame_Value, Var_Value=self.Var_Value)
        self.Input_RadioButton.configure(text="")
        self.Input_RadioButton.bind("<FocusOut>", self.Save())
        self.Set_Value()

    def Freeze(self):
        self.Input_RadioButton.configure(state="disabled")

    def UnFreeze(self):
        self.Input_RadioButton.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="none", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=False, padx=0, pady=0)
        self.Input_RadioButton.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    def Set_Value(self):
        self.Input_RadioButton.configure(variable=self.Variable)

    def Save(self):
        if (self.Save_To == None) or (self.Save_path == None):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Variable.get())



# -------------------------------------------------------------------------------- WidgetRow_Date_Picker -------------------------------------------------------------------------------- #
class WidgetRow_Date_Picker:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Date_format", "Save_To", "Save_path", "Documents", "Value", "placeholder_text_color", "Label_ToolTip", "Button_ToolTip", "Picker_Always_on_Top", "Picker_Fixed_position", "Validation", "GUI_Level_ID", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Date_Entry", "Button_Drop_Down", "Date_Picker_window", "Frame_Picker", "Value", "DatePicker_opened"
    """
    Field row for DatePicker
    """
    def __init__(self, 
                 Settings: dict|None, 
                 Configuration: dict|None, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Date_format: str,
                 Save_To: str|None = None,
                 Save_path: list|None = None,
                 Documents: dict|None = None,
                 Value: str|None = "",
                 placeholder_text_color: str = "",
                 Label_ToolTip: list|None = None, 
                 Button_ToolTip: list|None = None, 
                 Picker_Always_on_Top: bool = False,
                 Picker_Fixed_position: bool = False,
                 Validation: str|None = None,
                 GUI_Level_ID: int|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Date_format = Date_format
        self.Label_ToolTip = Label_ToolTip
        self.Value = Value
        self.placeholder_text_color = placeholder_text_color
        self.Validation = Validation
        self.Button_ToolTip = Button_ToolTip
        self.Picker_Always_on_Top = Picker_Always_on_Top
        self.Picker_Fixed_position = Picker_Fixed_position
        self.Save_To = Save_To 
        self.Save_path = Save_path
        self.GUI_Level_ID = GUI_Level_ID

        # DatePicker Variable Open
        self.DatePicker_opened = False

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        self.Date_Entry = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value, Field_Size="Pickers", Validation=self.Validation)
        if placeholder_text_color == "":
            self.Date_Entry.configure(placeholder_text=self.Date_format, placeholder_text_color=self.Date_Entry._placeholder_text_color)
        else:
            self.Date_Entry.configure(placeholder_text=self.Date_format, placeholder_text_color=self.placeholder_text_color)
        # Insert Value
        if self.Value != "":
            self.Date_Entry.delete(first_index=0, last_index=12)
            self.Date_Entry.insert(index=0, string=self.Value)
        else:
            pass
        self.Date_Entry.bind("<FocusOut>", lambda Value: self.Save(Value=Value))

        self.Button_Drop_Down = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Frame_Value, Icon_Name="calendar-days", Icon_Size="Entry_DropDown", Button_Size="Tiny")
        self.Button_Drop_Down.configure(command= lambda: self.Chose_date())

        Elements.Get_ToolTip(Configuration=Configuration, widget=self.Button_Drop_Down, message=self.Button_ToolTip, ToolTip_Size="Normal", GUI_Level_ID=self.GUI_Level_ID)

    def Chose_date(self):
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

        def select_date(Selected_year: int, Selected_month: int, Selected_day: int):
            selected_date = datetime(Selected_year, Selected_month, Selected_day)
            # Temporarily enable the entry to set the date
            self.Date_Entry.configure(state='normal')
            self.Date_Entry.delete(0, 30)
            self.Date_Entry.insert(0, selected_date.strftime(self.Date_format))
            self.Date_Picker_window.Pop_Up_Window.destroy()
            self.Save(Value=selected_date)
            self.DatePicker_opened = False

        def build_calendar(Shown_Month: int, Shown_Year: int) -> None:
            calendar_frame = Elements.Get_Frame(Configuration=self.Configuration, Frame=self.Frame_Picker.Body_Frame, Frame_Size="DatePicker", GUI_Level_ID=self.GUI_Level_ID)
            calendar_frame.grid(row=0, column=0)

            # Month and Year Selector
            month_label = Elements.Get_Label(Configuration=self.Configuration, Frame=calendar_frame, Label_Size="Field_Label", Font_Size="Field_Label")
            month_label.configure(text=f"{calendar.month_name[Shown_Month]}, {Shown_Year}")
            month_label.grid(row=0, column=1, columnspan=5)

            prev_month_button = Elements.Get_Button_Text(Configuration=self.Configuration, Frame=calendar_frame, Button_Size="Tiny")
            prev_month_button.configure(text="<", command=lambda: prev_month(Shown_Month=Shown_Month, Shown_Year=Shown_Year))
            prev_month_button.grid(row=0, column=0)

            next_month_button = Elements.Get_Button_Text(Configuration=self.Configuration, Frame=calendar_frame, Button_Size="Tiny")
            next_month_button.configure(text=">", command=lambda: next_month(Shown_Month=Shown_Month, Shown_Year=Shown_Year))
            next_month_button.grid(row=0, column=6)

            # Days of the week header
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for i, day in enumerate(days):
                lbl = Elements.Get_Label(Configuration=self.Configuration, Frame=calendar_frame, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
                lbl.configure(text=day)
                lbl.grid(row=1, column=i)

            # Days in month
            month_days = calendar.monthrange(Shown_Year, Shown_Month)[1]
            start_day = calendar.monthrange(Shown_Year, Shown_Month)[0]
            day = 1
            for week in range(2, 8):
                for day_col in range(7):
                    if week == 2 and day_col < start_day:
                        lbl = Elements.Get_Label(Configuration=self.Configuration, Frame=calendar_frame, Label_Size="Field_Label", Font_Size="Field_Label")
                        lbl.configure(text=f"")
                        lbl.grid(row=week, column=day_col)
                    elif day > month_days:
                        lbl = Elements.Get_Label(Configuration=self.Configuration, Frame=calendar_frame, Label_Size="Field_Label", Font_Size="Field_Label")
                        lbl.configure(text=f"")
                        lbl.grid(row=week, column=day_col)
                    else:
                        btn = Elements.Get_Button_Text(Configuration=self.Configuration, Frame=calendar_frame, Button_Size="DatePicker_Days")
                        # Today with red color
                        if (Shown_Year==Current_Year) and (Shown_Month==Current_Month) and (day==Current_Day):
                            btn.configure(text_color="#FF9797")
                        else:
                            pass
                        btn.configure(text=str(day), command=lambda day=day: select_date(Selected_year=Shown_Year, Selected_month=Shown_Month, Selected_day=day))
                        btn.grid(row=week, column=day_col)
                        day += 1

        if self.DatePicker_opened == False:
            self.DatePicker_opened = True
            # CTkToplevel window
            Import_window_geometry = (320, 320)
            Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=self.Button_Drop_Down, New_Window_width=Import_window_geometry[0])
            self.Date_Picker_window = PopUp_window(Configuration=self.Configuration, max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=self.Picker_Fixed_position, Always_on_Top=self.Picker_Always_on_Top)
            self.Date_Picker_window.Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: self.Date_Picker_window.Pop_Up_Window.destroy())

            # Frame - Date Picker
            self.Frame_Picker = WidgetFrame(Configuration=self.Configuration, Frame=self.Date_Picker_window.Pop_Up_Window, Name="Date picker", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Use to select date.", GUI_Level_ID=self.GUI_Level_ID)
            self.Frame_Picker.Widget_Frame.configure(bg_color = "#000001")

            Current_Year = datetime.now().year
            Current_Month = datetime.now().month
            Current_Day = datetime.now().day
            build_calendar(Shown_Month=Current_Month, Shown_Year=Current_Year)

            # Build look of Widget --> must be before inset
            self.Frame_Picker.Show()
        else:
            pass
    
    def Freeze(self):
        self.Date_Entry.configure(state="disabled")
        self.Button_Drop_Down.configure(state="disabled")

    def UnFreeze(self):
        self.Date_Entry.configure(state="normal")
        self.Button_Drop_Down.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="none", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        self.Date_Entry.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Button_Drop_Down.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=0)

    def Get_Value(self):
        return self.Date_Entry.get()

    def Save(self, Value):
        # Default
        self.Value = self.Get_Value()

        # Date Check
        if self.Value != "":
            try:
                datetime.strptime(self.Value, self.Date_format)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not in proper Date format, should be: {self.Date_format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Date_Entry.delete(first_index=0, last_index=100)
                self.Date_Entry.focus()
        else:
            pass

        # Save
        if (self.Save_To == None) or (self.Save_path == None):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Get_Value())

# -------------------------------------------------------------------------------- WidgetRow_Time_Picker -------------------------------------------------------------------------------- #
class WidgetRow_Time_Picker:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Time_format", "Save_To", "Save_path", "Documents", "Value", "placeholder_text_color", "Label_ToolTip", "Button_ToolTip", "Picker_Always_on_Top", "Picker_Fixed_position", "Validation", "GUI_Level_ID", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Time_Entry", "Button_Drop_Down", "Time_Picker_window", "Frame_Picker", "Value", "Hour_Variable", "Minute_Variable", "Frame_Picker", "Frame_Label_Row", "Hour_text", "Comma_text", "Minute_text", "Frame_Hour_Row", "Hour_text_0", "Hour_Slider", "Hour_text_23", "Frame_Minute_Row", "Minute_text_0", "Minutes_Slider", "Minute_text_59", "Time_Picker_opened", "Current_Hour", "Current_Minutes"
    """
    Field row for DatePicker
    """
    def __init__(self, 
                 Settings: dict|None, 
                 Configuration: dict|None, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Time_format: str,
                 Save_To: str|None = None,
                 Save_path: list|None = None,
                 Documents: dict|None = None,
                 Value: str|None = "",
                 placeholder_text_color: str = "",
                 Label_ToolTip: list|None = None, 
                 Button_ToolTip: list|None = None, 
                 Picker_Always_on_Top: bool = False,
                 Picker_Fixed_position: bool = False,
                 Validation: str|None = None,
                 GUI_Level_ID: int|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Time_format = Time_format
        self.Label_ToolTip = Label_ToolTip
        self.Value = Value
        self.placeholder_text_color = placeholder_text_color
        self.Validation = Validation
        self.Button_ToolTip = Button_ToolTip
        self.Picker_Always_on_Top = Picker_Always_on_Top
        self.Picker_Fixed_position = Picker_Fixed_position
        self.Save_To = Save_To 
        self.Save_path = Save_path
        self.GUI_Level_ID = GUI_Level_ID

        # TimePicker Variable Open
        self.Time_Picker_opened = False

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        self.Time_Entry = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value, Field_Size="Pickers", Validation=self.Validation)
        if placeholder_text_color == "":
            self.Time_Entry.configure(placeholder_text=self.Time_format, placeholder_text_color=self.Time_Entry._placeholder_text_color)
        else:
            self.Time_Entry.configure(placeholder_text=self.Time_format, placeholder_text_color=self.placeholder_text_color)
        # Insert Value
        if self.Value != "":
            self.Time_Entry.delete(first_index=0, last_index=12)
            self.Time_Entry.insert(index=0, string=self.Value)
        else:
            pass
        self.Time_Entry.bind("<FocusOut>", lambda Value: self.Save())

        self.Button_Drop_Down = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Frame_Value, Icon_Name="clock-10", Icon_Size="Entry_DropDown", Button_Size="Tiny")
        self.Button_Drop_Down.configure(command= lambda: self.Chose_time())

        Elements.Get_ToolTip(Configuration=Configuration, widget=self.Button_Drop_Down, message=self.Button_ToolTip, ToolTip_Size="Normal", GUI_Level_ID=self.GUI_Level_ID)

    def Chose_time(self):
        def Quit_Save():
            self.Set_Value()
            self.Time_Picker_window.Pop_Up_Window.destroy()
            self.Save()
            self.Time_Picker_opened = False

        def Sliding_Hours(value):
            if self.Hour_Variable.get() < 10:
                Hour_str = f"0{int(self.Hour_Variable.get())}"
            else:
                Hour_str = f"{int(self.Hour_Variable.get())}"

            self.Hour_text.configure(text=f"{Hour_str}")

        def Sliding_Minutes(value):
            if self.Minute_Variable.get() < 10:
                Minutes_str = f"0{int(self.Minute_Variable.get())}"
            else:
                Minutes_str = f"{int(self.Minute_Variable.get())}"

            self.Minute_text.configure(text=f"{Minutes_str}")

        if self.Time_Picker_opened == False:
            self.Time_Picker_opened = True

            # CTkToplevel window
            Import_window_geometry = (500, 250)
            Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=self.Button_Drop_Down, New_Window_width=Import_window_geometry[0])
            self.Time_Picker_window = PopUp_window(Configuration=self.Configuration, max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=self.Picker_Fixed_position, Always_on_Top=self.Picker_Always_on_Top)
            self.Time_Picker_window.Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: Quit_Save())

            # Time 
            Current_time = self.Get_Value()
            Current_time_list = Current_time.split(":")
            self.Hour_Variable = IntVar(master=self.Time_Picker_window.Pop_Up_Window, value=int(Current_time_list[0]))
            self.Minute_Variable = IntVar(master=self.Time_Picker_window.Pop_Up_Window, value=int(Current_time_list[1]))

            # Frame - Time Picker
            self.Frame_Picker = WidgetFrame(Configuration=self.Configuration, Frame=self.Time_Picker_window.Pop_Up_Window, Name="Time picker", Additional_Text="<ESC> to confirm.", Widget_size="Single_size", Widget_Label_Tooltip="Use to select time.", GUI_Level_ID=self.GUI_Level_ID)
            self.Frame_Picker.Widget_Frame.configure(bg_color = "#000001")

            # Time label 
            self.Frame_Label_Row = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.Frame_Picker.Body_Frame, Field_Frame_Type="Single_Column")
            self.Frame_Label_Row.pack(side="top", fill="y", expand=False, padx=10, pady=(0,5))

            self.Hour_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label_Row, Label_Size="Main", Font_Size="Main")
            if self.Hour_Variable.get() < 10:
                Hour_str = f"0{int(self.Hour_Variable.get())}"
            else:
                Hour_str = f"{int(self.Hour_Variable.get())}"
            self.Hour_text.configure(text=f"{Hour_str}")
            self.Hour_text.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))
            self.Comma_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label_Row, Label_Size="Main", Font_Size="Main")
            self.Comma_text.configure(text=":")
            self.Comma_text.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))
            self.Minute_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label_Row, Label_Size="Main", Font_Size="Main")
            if self.Minute_Variable.get() < 10:
                Minutes_str = f"0{int(self.Minute_Variable.get())}"
            else:
                Minutes_str = f"{int(self.Minute_Variable.get())}"
            self.Minute_text.configure(text=f"{Minutes_str}")
            self.Minute_text.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))

            # Hour
            self.Frame_Hour_Row = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.Frame_Picker.Body_Frame, Field_Frame_Type="Single_Column")
            self.Frame_Hour_Row.pack_propagate(flag=False)
            self.Frame_Hour_Row.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

            self.Hour_text_0 = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Hour_Row, Label_Size="Field_Label", Font_Size="Field_Label")
            self.Hour_text_0.configure(text="0")
            self.Hour_text_0.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))

            self.Hour_Slider = Elements.Get_Slider(Configuration=self.Configuration, Frame=self.Frame_Hour_Row, orientation="Horizontal", Slider_Size="TimePicker_Hours", GUI_Level_ID=self.GUI_Level_ID)
            self.Hour_Slider.configure(variable=self.Hour_Variable, command=lambda value: Sliding_Hours(value))
            self.Hour_Slider.pack(side="left", fill="x", expand=True, padx=0, pady=(0,5))

            self.Hour_text_23 = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Hour_Row, Label_Size="Field_Label", Font_Size="Field_Label")
            self.Hour_text_23.configure(text="23")
            self.Hour_text_23.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))

            # Minute
            self.Frame_Minute_Row = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.Frame_Picker.Body_Frame, Field_Frame_Type="Single_Column")
            self.Frame_Minute_Row.pack_propagate(flag=False)
            self.Frame_Minute_Row.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

            self.Minute_text_0 = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Minute_Row, Label_Size="Field_Label", Font_Size="Field_Label")
            self.Minute_text_0.configure(text="0")
            self.Minute_text_0.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))

            self.Minutes_Slider = Elements.Get_Slider(Configuration=self.Configuration, Frame=self.Frame_Minute_Row, orientation="Horizontal", Slider_Size="TimePicker_Minutes", GUI_Level_ID=self.GUI_Level_ID)
            self.Minutes_Slider.configure(variable=self.Minute_Variable, command=lambda value: Sliding_Minutes(value))
            self.Minutes_Slider.pack(side="left", fill="x", expand=True, padx=0, pady=(0,5))

            self.Minute_text_59 = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Minute_Row, Label_Size="Field_Label", Font_Size="Field_Label")
            self.Minute_text_59.configure(text="59")
            self.Minute_text_59.pack(side="left", fill="none", expand=False, padx=0, pady=(0,5))

            # Build look of Widget --> must be before inset
            self.Frame_Picker.Show()
        else:
            pass

    def Freeze(self):
        self.Time_Entry.configure(state="disabled")
        self.Button_Drop_Down.configure(state="disabled")

    def UnFreeze(self):
        self.Time_Entry.configure(state="normal")
        self.Button_Drop_Down.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="none", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        self.Time_Entry.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Button_Drop_Down.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=0)

    def Get_Value(self):
        return self.Time_Entry.get()
    
    def Set_Value(self):
        # Check hours
        if self.Hour_Variable.get() < 10:
            self.Current_Hour = f"0{self.Hour_Variable.get()}"
        else:
            self.Current_Hour = self.Hour_Variable.get()

        # Check minutes 
        if self.Minute_Variable.get() < 10:
            self.Current_Minutes = f"0{self.Minute_Variable.get()}"
        else:
            self.Current_Minutes = self.Minute_Variable.get()

        self.Time_Entry.delete(first_index=0, last_index=8)
        self.Time_Entry.insert(index=0, string=f"{self.Current_Hour}:{self.Current_Minutes}")

    def Save(self):
        # Default
        self.Value = self.Get_Value()

        # Time Check
        if self.Value != "":
            try:
                datetime.strptime(self.Value, self.Time_format)
            except:
                Elements.Get_MessageBox(Configuration=self.Configuration, window=self.window, title="Error", message=f"Value: {self.Value} in not in proper Time format, should be: {self.Time_format}.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                self.Time_Entry.delete(first_index=0, last_index=100)
                self.Time_Entry.focus()
        else:
            pass

        # Save
        if (self.Save_To == None) or (self.Save_path == None):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Get_Value())

# -------------------------------------------------------------------------------- WidgetRow_Color_Picker -------------------------------------------------------------------------------- #
class WidgetRow_Color_Picker:
    __slots__ = "Settings", "Configuration", "master", "window", "Field_Frame_Type", "Label", "Save_To", "Save_path", "Documents", "Value", "placeholder_text_color", "Label_ToolTip", "Button_ToolTip", "Picker_Always_on_Top", "Picker_Fixed_position", "Validation", "GUI_Level_ID", "Row_Frame", "Frame_Label", "Label_text", "Frame_Space", "Frame_Value", "Color_Entry", "Button_Drop_Down", "Color_Picker_window", "Frame_Picker", "Color_Picker", "ColorPicker_opened"
    """
    Field row for ColorPicker
    """
    def __init__(self, 
                 Settings: dict|None, 
                 Configuration: dict|None, 
                 master: CTkFrame, 
                 window: CTk, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Save_To: str,
                 Save_path: list|None = None,
                 Documents: dict|None = None,
                 Value: str|None = None,
                 placeholder_text_color: str = "",
                 Label_ToolTip: list|None = None, 
                 Button_ToolTip: list|None = None, 
                 Picker_Always_on_Top: bool = False,
                 Picker_Fixed_position: bool = False,
                 Validation: str|None = None,
                 GUI_Level_ID: int|None = None):
        self.Settings = Settings
        self.Configuration = Configuration
        self.Documents = Documents
        self.master = master
        self.window = window
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Label_ToolTip = Label_ToolTip
        self.Value = Value
        self.placeholder_text_color = placeholder_text_color
        self.Validation = Validation
        self.Button_ToolTip = Button_ToolTip
        self.Picker_Always_on_Top = Picker_Always_on_Top
        self.Picker_Fixed_position = Picker_Fixed_position
        self.Save_To = Save_To 
        self.Save_path = Save_path
        self.GUI_Level_ID = GUI_Level_ID

        # ColorPicker Variable Open
        self.ColorPicker_opened = False

        # Whole Row Frame
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Field Description
        self.Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Label.pack_propagate(flag=False)

        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
        self.Label_text.configure(text=f"{self.Label}:")

        if type(self.Label_ToolTip) == list:
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Label_text, message=self.Label_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=self.Label_ToolTip[1])
        else:
            pass

        # Row indent
        self.Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        
        # Field Value
        self.Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Value.pack_propagate(flag=False)
        
        self.Color_Entry = Elements.Get_Entry_Field(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Value, Field_Size="Pickers", Validation=self.Validation)
        if self.placeholder_text_color == "":
            self.Color_Entry.configure(placeholder_text="#NNNNNN", placeholder_text_color=self.Color_Entry._placeholder_text_color)
        else:
            self.Color_Entry.configure(placeholder_text="#NNNNNN", placeholder_text_color=self.placeholder_text_color)
        # Insert Value
        if self.Value != "":
            self.Color_Entry.delete(first_index=0, last_index=12)
            self.Color_Entry.insert(index=0, string=self.Value)
        else:
            pass
        self.Color_Entry.bind("<FocusOut>", self.Save())

        self.Button_Drop_Down = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Frame_Value, Icon_Name="paintbrush", Icon_Size="Entry_DropDown", Button_Size="Tiny")
        self.Button_Drop_Down.configure(command= lambda: self.Chose_color())

        Elements.Get_ToolTip(Configuration=Configuration, widget=self.Button_Drop_Down, message=self.Button_ToolTip, ToolTip_Size="Normal", GUI_Level_ID=self.GUI_Level_ID)

    def Chose_color(self):
        def Quit_Save():
            self.Set_Value()
            self.Color_Picker_window.Pop_Up_Window.destroy()
            self.Save()
            self.ColorPicker_opened = False

        if self.ColorPicker_opened == False:
            self.ColorPicker_opened = True
            # CTkToplevel window
            Import_window_geometry = (320, 320)
            Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=self.Button_Drop_Down, New_Window_width=Import_window_geometry[0])
            self.Color_Picker_window = PopUp_window(Configuration=self.Configuration, max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=self.Picker_Fixed_position, Always_on_Top=self.Picker_Always_on_Top)
            self.Color_Picker_window.Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: Quit_Save())

            # Frame - Color Picker
            self.Frame_Picker = WidgetFrame(Configuration=self.Configuration, Frame=self.Color_Picker_window.Pop_Up_Window, Name="Color picker", Additional_Text="<ESC> to confirm.", Widget_size="Single_size", Widget_Label_Tooltip="Use to select color.", GUI_Level_ID=self.GUI_Level_ID)
            self.Frame_Picker.Widget_Frame.configure(bg_color = "#000001")
            self.Color_Picker = Elements.Get_Color_Picker(Configuration=self.Configuration, Frame=self.Frame_Picker.Body_Frame, GUI_Level_ID=self.GUI_Level_ID)

            # Build look of Widget --> must be before inset
            self.Frame_Picker.Show()
            self.Color_Picker.pack(padx=0, pady=0) 
        else:
            pass
    
    def Freeze(self):
        self.Color_Entry.configure(state="disabled")
        self.Button_Drop_Down.configure(state="disabled")

    def UnFreeze(self):
        self.Color_Entry.configure(state="normal")
        self.Button_Drop_Down.configure(state="normal")

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))
        self.Frame_Label.pack(side="left", fill="none", expand=False, padx=0, pady=7)
        self.Label_text.pack(side="right", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Space.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        self.Color_Entry.pack(side="left", fill="none", expand=False, padx=0, pady=0)
        self.Button_Drop_Down.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=0)

    def Get_Value(self):
        return self.Color_Entry.get()

    def Set_Value(self):
        self.Color_Entry.delete(first_index=0, last_index=8)
        self.Color_Entry.insert(index=0, string=self.Color_Picker.get())

    def Save(self):
        if (self.Save_To == None) or (self.Save_path == None):
            pass
        else:
            Data_Functions.Save_Value(Settings=self.Settings, Configuration=self.Configuration, Documents=self.Documents, window=self.window, Variable=None, File_Name=self.Save_To, JSON_path=self.Save_path, Information=self.Get_Value())

# -------------------------------------------------------------------------------- Widget_Buttons_Row -------------------------------------------------------------------------------- #
class Widget_Buttons_Row:
    __slots__ = "Configuration", "master", "Field_Frame_Type", "Buttons_count", "Button_Size", "Button_Text", "Button_ToolTips", "Button_Functions", "GUI_Level_ID", "Row_Frame", "Frame_Buttons", "Button_Normal"
    """
    Field row for Widget_Buttons_Row
    """
    def __init__(self, 
                 Configuration:dict, 
                 master: CTkFrame, 
                 Field_Frame_Type: str, 
                 Buttons_count: int,
                 Button_Size: str,
                 Button_Text: list,
                 Button_Functions: list|None = None,
                 Button_ToolTips: list|None = None, 
                 GUI_Level_ID: int|None = None):
        
        self.Configuration = Configuration
        self.master = master
        self.Field_Frame_Type = Field_Frame_Type
        self.Buttons_count = Buttons_count
        self.Button_Size = Button_Size
        self.Button_Text = Button_Text
        self.Button_ToolTips = Button_ToolTips
        self.Button_Functions = Button_Functions
        self.GUI_Level_ID = GUI_Level_ID

        # Build one line for one input field
        self.Row_Frame = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Row_Frame.pack_propagate(flag=False)

        # Frame Value
        self.Frame_Buttons = Elements.Get_Widget_Field_Frame_Value(Configuration=self.Configuration, Frame=self.Row_Frame, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Buttons.pack_propagate(flag=False)
        
        for Button in range(self.Buttons_count): 
            self.Button_Normal = Elements.Get_Button_Text(Configuration=self.Configuration, Frame=self.Frame_Buttons, Button_Size=self.Button_Size)
            self.Button_Normal.configure(text=self.Button_Text[Button])
            if self.Button_Functions != None:
                self.Button_Normal.configure(command = self.Button_Functions[Button])
            else:
                pass
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Button_Normal, message=self.Button_ToolTips[Button], ToolTip_Size="Normal", GUI_Level_ID=self.GUI_Level_ID + 1)
            self.Button_Normal.pack(side="right", fill="none", expand=False, padx=(10,0))

    def Add_Function(self, Button_Functions: list):
        Counter = 0
        for Button in self.Frame_Buttons.winfo_children():
            self.Button_Normal.configure(command = Button_Functions[Counter])
            Counter += 1

    def Show(self):
        self.Row_Frame.pack(side="top", fill="none", expand=True, padx=10, pady=(5,5))
        self.Frame_Buttons.pack(side="right", fill="x", expand=True, padx=0, pady=0)

    def Freeze(self):
        for Button in self.Frame_Buttons.winfo_children():
            Button.configure(state="disabled")

    def UnFreeze(self):
        for Button in self.Frame_Buttons.winfo_children():
            Button.configure(state="normal")

# -------------------------------------------------------------------------------- Widget_Section_Row -------------------------------------------------------------------------------- #
class Widget_Section_Row:
    __slots__ = "Configuration", "master", "Field_Frame_Type", "Label", "Label_Size", "Font_Size", "Frame_Area", "Label_text"
    """
    Field row for Section row
    """
    def __init__(self, 
                 Configuration:dict, 
                 master: CTkFrame, 
                 Field_Frame_Type: str, 
                 Label: str, 
                 Label_Size: str,
                 Font_Size: str):
        self.Configuration = Configuration
        self.master = master
        self.Field_Frame_Type = Field_Frame_Type
        self.Label = Label
        self.Label_Size = Label_Size
        self.Font_Size = Font_Size

        # Whole Row Frame
        self.Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=self.Configuration, Frame=self.master, Field_Frame_Type=self.Field_Frame_Type)
        self.Frame_Area.pack_propagate(flag=False)
        
        # Section Sext
        self.Label_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Frame_Area, Label_Size=self.Label_Size, Font_Size=self.Font_Size)
        self.Label_text.configure(text=f"{Label}")
        
    def Show(self):
        self.Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(10,5))
        self.Label_text.pack(side="left", fill="none", expand=False, padx=(50, 0), pady=5)

# -------------------------------------------------------------------------------- WidgetFrame -------------------------------------------------------------------------------- #
class WidgetFrame:
    __slots__ = "Configuration", "Frame", "Name", "Additional_Text", "Widget_size", "Widget_Label_Tooltip", "GUI_Level_ID", "Widget_Frame", "Header_Frame", "Header_text", "Header_Icon", "Header_text_Additional", "Body_Frame", "Scrollable", "TopUp_Frame", "content_row_count", "content_height"
    """
    Widget for Pages
    """
    def __init__(self, 
                 Configuration:dict, 
                 Frame: CTkFrame|CTkToplevel, 
                 Name: str, 
                 Additional_Text: str, 
                 Widget_size: str, 
                 Widget_Label_Tooltip: str, 
                 Scrollable: bool = False,
                 TopUp_Frame: bool = False,
                 GUI_Level_ID: int|None = None):
        self.Configuration = Configuration
        self.Frame = Frame
        self.Name = Name
        self.Additional_Text = Additional_Text
        self.Widget_size = Widget_size
        self.Widget_Label_Tooltip = Widget_Label_Tooltip
        self.Scrollable = Scrollable
        self.TopUp_Frame = TopUp_Frame
        self.GUI_Level_ID = GUI_Level_ID

        # Widget Main Frame
        if self.Scrollable == True:
            self.Widget_Frame = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=self.Frame, Frame_Size=self.Widget_size, GUI_Level_ID=self.GUI_Level_ID)
        else:
            self.Widget_Frame = Elements.Get_Widget_Frame_Body(Configuration=self.Configuration, Frame=self.Frame, Widget_size=self.Widget_size, GUI_Level_ID=self.GUI_Level_ID)
        if self.TopUp_Frame == True:
            self.Widget_Frame.configure(bg_color="#000001")
        else:
            pass

        # Widget Header line
        self.Header_Frame = Elements.Get_Widget_Frame_Header(Configuration=self.Configuration, Frame=self.Widget_Frame, Widget_size=self.Widget_size)
        
        self.Header_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Header_Frame, Label_Size="Column_Header", Font_Size="Column_Header")
        self.Header_text.configure(text=f"{self.Name}")
        
        if self.Widget_Label_Tooltip == "":
            pass
        else:
            self.Header_Icon = Elements.Get_Label_Icon(Configuration=self.Configuration, Frame=self.Header_Frame, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Name="circle-help", Icon_Size="Question")
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Header_Icon, message=self.Widget_Label_Tooltip, ToolTip_Size="Normal", GUI_Level_ID=self.GUI_Level_ID)

        self.Header_text_Additional = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Header_Frame, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
        self.Header_text_Additional.configure(text=f"{self.Additional_Text}")
        
        # Widget Body
        self.Body_Frame = Elements.Get_Widget_Frame_Area(Configuration=self.Configuration, Frame=self.Widget_Frame, Widget_size=self.Widget_size)

    def Show(self):
        self.Widget_Frame.pack(side="top", fill="none", expand=False, padx=10, pady=10)
        self.Header_Frame.pack(side="top", fill="x", expand=False, padx=4, pady=4)
        self.Header_text.pack(side="left", fill="none", expand=False, padx=(7, 0), pady=5)
        if self.Widget_Label_Tooltip == "":
            pass
        else:
            self.Header_Icon.pack(side="left", fill="none", expand=False, padx=1, pady=0)
        self.Header_text_Additional.pack(side="right", fill="x", expand=False, padx=(7, 0), pady=5)
        self.Body_Frame.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    def Add_row(self, Rows: list):
        for Row in Rows:
            Row.Show()
    
    def Update_height(self, Max_Height: int):
        self.content_row_count = len(self.Body_Frame.winfo_children())
        self.content_height = self.content_row_count * 35 + 30 + (self.Header_Frame.winfo_height())    # Lines multiplied + button + Header if needed (50)
        if self.content_height > Max_Height:
            self.content_height = Max_Height
        self.Widget_Frame.configure(height=self.content_height)

# -------------------------------------------------------------------------------- Widget_Table_Frame -------------------------------------------------------------------------------- #
class WidgetTableFrame:
    __slots__ = "Configuration", "Frame", "Table_Size", "Table_Values", "Table_Columns", "Table_Rows", "wraplength", "GUI_Level_ID", "Frame_Scrollable_Area", "Table", "Table_Values"
    """
    Widget for Pages
    """
    def __init__(self, 
                 Configuration:dict, 
                 Frame: CTkFrame, 
                 Table_Size: str, 
                 Table_Values: list|None, 
                 Table_Columns: int, 
                 Table_Rows: int, 
                 wraplength: int|None = None,
                 GUI_Level_ID: int|None = None):
        self.Configuration = Configuration
        self.Frame = Frame
        self.Table_Size = Table_Size
        self.Table_Values = Table_Values
        self.Table_Columns = Table_Columns
        self.Table_Rows = Table_Rows
        self.wraplength = wraplength
        self.GUI_Level_ID = GUI_Level_ID

        # Build only one frame which contain whole Table
        self.Frame_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=self.Configuration, Frame=self.Frame, Frame_Size=self.Table_Size, GUI_Level_ID=self.GUI_Level_ID)
        
        # Table
        self.Table = Elements.Get_Table(Configuration=self.Configuration, Frame=self.Frame_Scrollable_Area, Table_size=self.Table_Size, columns=self.Table_Columns, rows=self.Table_Rows, GUI_Level_ID=self.GUI_Level_ID)
        self.Table.configure(wraplength=self.wraplength)
        if self.Table_Values == None:
            pass
        else:
            self.Table.configure(values=self.Table_Values)

    def Show(self):
        self.Frame_Scrollable_Area.pack(side="top", fill="y", expand=True, padx=10, pady=(0,5))
        self.Table.pack(side="top", fill="y", expand=True, padx=10, pady=10)


# -------------------------------------------------------------------------------- PopUp_window -------------------------------------------------------------------------------- #
class PopUp_window:
    __slots__ = "Configuration", "max_width", "max_height", "Top_middle_point", "Fixed", "Always_on_Top", "Pop_Up_Window", "left_position", "top_position", "Pop_Up_Window"
    """
    Widget for PopUp_window
    """
    def __init__(self, 
                 Configuration: dict, 
                 max_width: int, 
                 max_height: int,
                 Top_middle_point: list,
                 Fixed: bool = False, 
                 Always_on_Top: bool = True):
        self.Configuration = Configuration
        self.max_width = max_width
        self.max_height = max_height
        self.Top_middle_point = Top_middle_point
        self.Fixed = Fixed
        self.Always_on_Top = Always_on_Top

        # TopUp Window
        self.Pop_Up_Window = CTkToplevel()
        self.Pop_Up_Window.configure(fg_color="#000001")

        self.left_position = self.Top_middle_point[0]
        self.top_position = self.Top_middle_point[1]
        self.Pop_Up_Window.geometry("+%d+%d" % (self.left_position, self.top_position))
        self.Pop_Up_Window.maxsize(width=self.max_width, height=self.max_height)

        #Pop_Up_Window.geometry(f"{width}x{height}")
        self.Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: self.Pop_Up_Window.destroy())
        self.Pop_Up_Window.attributes("-topmost", self.Always_on_Top)
        if Fixed == False:
            self.Pop_Up_Window.bind(sequence="<Button-1>", func=lambda event:self.click_win())
            self.Pop_Up_Window.bind(sequence="<B1-Motion>", func=lambda event:self.drag_win())
        else:
            pass
        self.Pop_Up_Window.overrideredirect(boolean=True)
        self.Pop_Up_Window.iconbitmap(bitmap=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\HQ_Data_Generator.ico"))
        self.Pop_Up_Window.resizable(width=False, height=False)

        # Rounded corners 
        self.Pop_Up_Window.config(background="#000001")
        self.Pop_Up_Window.attributes("-transparentcolor", "#000001")

    def drag_win(self):
        x = self.Pop_Up_Window.winfo_pointerx() - self.Pop_Up_Window._offsetx
        y = self.Pop_Up_Window.winfo_pointery() - self.Pop_Up_Window._offsety
        self.Pop_Up_Window.geometry(f"+{x}+{y}")

    def click_win(self):
        self.Pop_Up_Window._offsetx = self.Pop_Up_Window.winfo_pointerx() - self.Pop_Up_Window.winfo_rootx()
        self.Pop_Up_Window._offsety = self.Pop_Up_Window.winfo_pointery() - self.Pop_Up_Window.winfo_rooty()

    def Destroy(self):
        self.Pop_Up_Window.destroy()