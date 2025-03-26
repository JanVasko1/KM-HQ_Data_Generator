# Import Libraries
import pyautogui
from customtkinter import CTk, CTkButton, get_appearance_mode, BooleanVar, CTkCheckBox
from CTkTable import CTkTable
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions

# --------------------------------------------- CustomTkinter --------------------------------------------- #
def Dialog_Window_Request(Configuration: dict|None, title: str, text: str, Dialog_Type: str, GUI_Level_ID: int|None = None) -> str|None:
    # Password required
    dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type, GUI_Level_ID=GUI_Level_ID)
    Dialog_Input = dialog.get_input()
    return Dialog_Input

def Get_Current_Theme() -> str:
    Current_Theme = get_appearance_mode()
    return Current_Theme

def Count_coordinate_for_new_window(Clicked_on: CTkButton, New_Window_width: int) -> list:
    # Click_on coordinate
    Clicked_on_X = Clicked_on.winfo_pointerx() - Clicked_on.winfo_rootx()
    Clicked_on_Y = Clicked_on.winfo_pointery() - Clicked_on.winfo_rooty()

    Clicked_on_width = Clicked_on._current_width
    Clicked_on_X_middle = Clicked_on_width // 2
    Clicked_on_height = Clicked_on._current_height

    Clicked_On_X_difference = Clicked_on_X_middle - Clicked_on_X - (New_Window_width // 2)
    Clicked_on_Y_difference = Clicked_on_height - Clicked_on_Y

    # Window coordinate
    Window_X, Window_Y = pyautogui.position()

    # Top middle coordinate for new window
    return [Window_X + Clicked_On_X_difference, Window_Y + Clicked_on_Y_difference + 5]

def Get_coordinate_Main_Window(Main_Window: CTk) -> list:
    Main_Window.update_idletasks()  # Ensure the geometry information is updated
    x = (Main_Window.winfo_width() // 2) + Main_Window.winfo_rootx()
    y = (Main_Window.winfo_height() // 2) + Main_Window.winfo_rooty()
    Coordinate = [x, y]
    return Coordinate

def Insert_Data_to_Table(Settings: dict, Configuration: dict|None, window: CTk|None, Table: CTkTable, JSON_path: list) -> None:
    # Delete data in table just keep header
    Table_rows = Table.cget("row")

    for row_index in range(1, Table_rows):
        Table.delete_row(row_index)

    # Get Data
    Current_Data = Defaults_Lists.Load_Settings_Part(my_dict=Settings, JSON_path=JSON_path)

    if type(Current_Data) is dict:
        row_index = 1
        for key, value in Current_Data.items():
            # Prepare Values into list
            Add_row = list(value.values())

            # Insert
            Table.add_row(index=row_index, values=Add_row)
            row_index += 1

    elif type(Current_Data) is list:
        row_index = 1
        for data in Current_Data:
            Table.add_row(index=row_index, values=[data])
            row_index += 1
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title=f"It is not possible to insert data to table. Data are uploaded, just restart application.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

# ------------------ Blocking Fields Functions ------------------ #

def Field_Block_Bool(Settings: dict, window: CTk|None, Selected_Variable: BooleanVar, Selected_Field: CTkCheckBox, Selected_JSON_path: list, Block_Variable_list: list, Block_Field_list: list, Block_JSON_path_list: list) -> None:
    Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Selected_Variable, File_Name="Settings", JSON_path=Selected_JSON_path, Information=Selected_Variable)
    for i, Block_Variable in enumerate(Block_Variable_list):
        if Selected_Variable.get() == True:
            Block_Field_list[i].configure(state="normal")
        elif Selected_Variable.get() == False:
            Block_Field_list[i].configure(state="disabled")
            Block_Variable_list[i].set(value=False)
        Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Block_Variable_list[i], File_Name="Settings", JSON_path=Block_JSON_path_list[i], Information=Block_Variable_list[i])
