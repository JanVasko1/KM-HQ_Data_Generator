# Import Libraries
from customtkinter import CTk, CTkFrame
from tkhtmlview import HTMLLabel
from markdown import markdown

import Libs.GUI.Elements as Elements
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Data_Functions as Data_Functions

def Page_Information(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTk|CTkFrame):
    Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]
    Work_Area_Detail_Background = list(Configuration["Global_Appearance"]["GUI_Level_ID"]["1"]["fg_color"])

    # ------------------------- Main Functions -------------------------#
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

    # ------------------------- Info Text Area -------------------------#
    # Description
    Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Triple_size", GUI_Level_ID=1)

    with open(Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Information.md"), "r", encoding="UTF-8") as file:
        html_markdown=markdown(text=file.read())
    file.close()

    Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"""<p style="color: {HTML_Font_Color};">{html_markdown}</p>""", background=HTML_Background_Color, font="Roboto")
    Information_html.configure(height=700)

    # Build look of Widget
    Frame_Information_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Information_html.pack(side="top", fill="both", expand=True, padx=10, pady=10)
