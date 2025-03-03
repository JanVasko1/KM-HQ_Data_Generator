# Import Libraries
import pyautogui
from customtkinter import CTkButton, get_appearance_mode
from CTkTable import CTkTable
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

# --------------------------------------------- CustomTkinter --------------------------------------------- #
def Dialog_Window_Request(Configuration: dict, title: str, text: str, Dialog_Type: str) -> str|None:
    # Password required
    dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type)
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

def Insert_Data_to_Table(Settings: dict, Configuration: dict, Table: CTkTable, JSON_path: list) -> None:
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
        Elements.Get_MessageBox(Configuration=Configuration, title=f"It is not possible to insert data to table. Data are uploaded, just restart application.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
