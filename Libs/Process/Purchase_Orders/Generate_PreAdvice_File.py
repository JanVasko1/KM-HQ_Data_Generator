# Import Libraries
from datetime import datetime, timedelta

from customtkinter import CTk, CTkFrame, StringVar

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups


def Generate_PreAdvice_from_Delivery_dict(Settings: dict, Configuration: dict, window: CTk, PO_Deliveries: list):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    PO_PreAdvices = []

    PreAdvice_Dates_Method = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Method"]
    Pre_Fix_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Fixed_Options"]["Fix_Date"]
    Pre_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Random_Options"]["From"]
    Pre_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Random_Options"]["To"]
    Pre_Gen_Date_Shift = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Shift_Options"]["Generation_Date_Shift_by"]
    Pre_Delivery_Shift = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Delivery_Date"]["Shift_Options"]["Delivery_Date_Shift_by"]
    PreAdvice_Date = ""


    # --------------------------------------------- PreAdvice Date --------------------------------------------- #
    for Delivery_index, Delivery in enumerate(PO_Deliveries):
        PO_PreAdvice = dict(Delivery)

        if PreAdvice_Dates_Method == "Fixed":
            PreAdvice_Date = Pre_Fix_Date
        elif PreAdvice_Dates_Method == "Random":
            PreAdvice_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=Pre_Rand_From_Date, To_int=Pre_Rand_To_Date, Format=Date_format)
        elif PreAdvice_Dates_Method == "Delivery Date Shift":
            Delivery_Date = PO_PreAdvice["dispatchnotification"]["dispatchnotification_header"]["control_info"]["delivery_date"]
            Delivery_Date_dt = datetime.strptime(Delivery_Date, Date_format)
            PreAdvice_Date_dt = Delivery_Date_dt + timedelta(days=Pre_Delivery_Shift)
            PreAdvice_Date = PreAdvice_Date_dt.strftime(Date_format)
        elif PreAdvice_Dates_Method == "Prompt":
            def Select_PO_Pre_Date_Date(Prompt_Date_Frame: CTkFrame):
                Generation_Date_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                PO_Pre_Date_Date = Generation_Date_Var.get()
                PO_Pre_Date_Date_Variable.set(value=PO_Pre_Date_Date)
                PO_Pre_Date_Window.destroy()
                
            # TopUp Window
            PO_Pre_Date_Window_geometry = (500, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Pre_Date_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Pre_Date_Window_geometry[1] //2
            PO_Pre_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Delivery Date for PreAdvice.", max_width=PO_Pre_Date_Window_geometry[0], max_height=PO_Pre_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_Pre_Date_Window, Name="Select Delivery Date for PreAdvice.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select GEneration Date of BEU Confirmation.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="PreAdvice Delivery Date",  Field_Type="Entry_DropDown")  
            Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
            Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
            Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
            Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

            # Buttons
            PO_Pre_Date_Date_Variable = StringVar(master=PO_Pre_Date_Window, value="", name="PO_Pre_Date_Date_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_Pre_Date_Date(Prompt_Date_Frame=Prompt_Date_Frame))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Delivery Date for PreAdvice.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_Pre_Date_Date_Variable)
            PreAdvice_Date = PO_Pre_Date_Date_Variable.get()
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"PreAdvice Number Method selected: {PreAdvice_Dates_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Assign new value
        PreAdvice_Date_dt = datetime.strptime(PreAdvice_Date, Date_format)
        Generation_Date_dt = PreAdvice_Date_dt + timedelta(days=Pre_Gen_Date_Shift)
        Generation_Date = Generation_Date_dt.strftime(Date_format)
        PO_PreAdvice["dispatchnotification"]["dispatchnotification_header"]["control_info"]["generation_date"] = Generation_Date
        PO_PreAdvice["dispatchnotification"]["dispatchnotification_header"]["control_info"]["delivery_date"] = PreAdvice_Date

        # Add to Preadvice List
        PO_PreAdvices.append(PO_PreAdvice)


    # --------------------------------------------- Delete unnecessary Keys --------------------------------------------- #
    for PreAdvice_index, PreAdvice in enumerate(PO_PreAdvices):
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["picking_date"]
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["trans_planning_date"]
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["loading_date"]
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["planned_gi_date"]
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["carrier_id"]
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["packages_info"]

        bolnr = PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["remarks"]["bolnr"]
        PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["remarks"]["exidv2"] = ""
        del PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["remarks"]["bolnr"]
        PO_PreAdvices[PreAdvice_index]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["remarks"]["bolnr"] = bolnr

        # Rename main header key dispatchnotification --> preadvice
        PO_PreAdvices[PreAdvice_index]["preadvice"] = PO_PreAdvices[PreAdvice_index].pop("dispatchnotification")

    return PO_PreAdvices