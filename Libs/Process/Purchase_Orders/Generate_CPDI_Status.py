# Import Libraries
import random
from pandas import DataFrame
from fastapi import HTTPException

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.File_Manipulation as File_Manipulation

from customtkinter import CTk, CTkFrame, StringVar

def Generate_PO_CPDI_Messages(Settings: dict, 
                              Configuration: dict|None, 
                              window: CTk|None, 
                              Export_NAV_Folder: bool, 
                              NVR_FS_Connect_df: DataFrame, 
                              HQ_Communication_Setup_df: DataFrame, 
                              PO_Delivery_Number_list: list, 
                              Purchase_Order: str, 
                              Buy_from_Vendor_No: str, 
                              Purchase_Headers_df: DataFrame, 
                              HQ_CPDI_Level_df: DataFrame, 
                              HQ_CPDI_Status_df: DataFrame,
                              GUI: bool=True) -> None:
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True

    CPDI_Delivery_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Delivery_select"]["Method"]
    Fixed_Delivery = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Delivery_select"]["Fixed_Options"]["Fix_Delivery"]
    CPDI_Delivery_list = []

    CPDI_Level_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Level_Provided"]["Method"]
    Fixed_CPDI_Level = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Level_Provided"]["Fixed_Options"]["Fix_Level"]
    CPDI_Level = ""

    CPDI_Status_Method = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Status"]["Method"]
    Fixed_CPDI_Status = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Status"]["Fixed_Options"]["Fix_Status"]
    CPDI_Status_List = []

    # --------------------------------------------- Delivery --------------------------------------------- #
    if len(PO_Delivery_Number_list) == 0:
        # Must prompt every time
        if CPDI_Delivery_Method == "All Deliveries":
            if GUI == True:
                CPDI_Delivery_Method = "Prompt"   
            else:
                CPDI_Delivery_Method = "Fixed"    
        else:
            pass  

        if CPDI_Delivery_Method == "Fixed":
            CPDI_Delivery_list.append(Fixed_Delivery)
        elif CPDI_Delivery_Method == "Prompt":
            if GUI == True:
                CPDI_Delivery_list = []
                def Select_Delivery(Prompt_Delivery_Frame: CTkFrame):
                    Delivery_Var = Prompt_Delivery_Frame.children["!ctkframe3"].children["!ctkentry"]
                    Delivery_Number = Delivery_Var.get()
                    CPDI_Delivery_Variable.set(value=Delivery_Number)
                    CPDI_Delivery_Window.destroy()
                    
                # TopUp Window
                CPDI_Delivery_Window_geometry = (500, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - CPDI_Delivery_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - CPDI_Delivery_Window_geometry[1] //2
                CPDI_Delivery_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Delivery for CPDI document.", max_width=CPDI_Delivery_Window_geometry[0], max_height=CPDI_Delivery_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=CPDI_Delivery_Window, Name="Select Delivery for CPDI document.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select for which delivery the CPDI statuses should be created.", GUI_Level_ID=3)
                Frame_Main.configure(bg_color = "#000001")
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Prompt_Delivery_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Delivery Number",  Field_Type="Input_Normal")  
                Prompt_Delivery_Frame_Var = Prompt_Delivery_Frame.children["!ctkframe3"].children["!ctkentry"]
                Prompt_Delivery_Frame_Var.configure(placeholder_text="Insert your Delivery Number", placeholder_text_color="#949A9F")

                # Buttons
                CPDI_Delivery_Variable = StringVar(master=CPDI_Delivery_Window, value="", name="CPDI_Delivery_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Delivery(Prompt_Delivery_Frame=Prompt_Delivery_Frame))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Delivery selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(CPDI_Delivery_Variable)
                CPDI_Delivery_list.append(CPDI_Delivery_Variable.get())
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PO_CPDI_Messages:Delivery Number_list = 1.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Method selected: {CPDI_Delivery_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Delivery Method selected: {CPDI_Delivery_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    elif len(PO_Delivery_Number_list) > 0:
        if CPDI_Delivery_Method == "Fixed":
            CPDI_Delivery_list.append(Fixed_Delivery)
        elif CPDI_Delivery_Method == "All Deliveries":
            CPDI_Delivery_list = PO_Delivery_Number_list
        elif CPDI_Delivery_Method == "Prompt":
            if GUI == True:
                def Select_from_Delivery_List(Frame_Body: CTkFrame, Lines_No: int, CPDI_Delivery_list: list):
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkCheck = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkcheckbox"]
                        Value_CTkCheck_Value = Value_CTkCheck.get()
                        if Value_CTkCheck_Value == True:
                            Selected_Delivery_No_label = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe"].children["!ctklabel"]
                            Selected_Delivery_No = str(Selected_Delivery_No_label.cget("text"))
                            Selected_Delivery_No = Selected_Delivery_No.replace(":", "")
                            CPDI_Delivery_list.append(Selected_Delivery_No)
                        else:
                            pass
                    CPDI_Delivery_Variable.set(value="Selected")
                    CPDI_Delivery_Window.destroy()
                
                # TopUp Window
                CPDI_Delivery_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - CPDI_Delivery_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - CPDI_Delivery_Window_geometry[1] //2
                CPDI_Delivery_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Delivery/s for CPDI document.", max_width=CPDI_Delivery_Window_geometry[0], max_height=CPDI_Delivery_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=CPDI_Delivery_Window, Name="Select Delivery/s for CPDI document.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select for which delivery the CPDI statuses should be created.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Delivery list
                Lines_No = len(PO_Delivery_Number_list)
                for Delivery in PO_Delivery_Number_list:
                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Delivery}", Field_Type="Input_CheckBox") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                    Fields_Frame_Var.configure(text="")

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > CPDI_Delivery_Window_geometry [1]:
                    content_height = CPDI_Delivery_Window_geometry [1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                CPDI_Delivery_Variable = StringVar(master=CPDI_Delivery_Window, value="", name="CPDI_Delivery_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_from_Delivery_List(Frame_Body=Frame_Body, Lines_No=Lines_No, CPDI_Delivery_list=CPDI_Delivery_list))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Delivery selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(CPDI_Delivery_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PO_CPDI_Messages:Delivery Number_list > 1.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Method selected: {CPDI_Delivery_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Delivery Method selected: {CPDI_Delivery_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery length is not supported, canceling  CPDI Process.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail=f"Delivery length is not supported, canceling  CPDI Process.")
        Can_Continue = False 
        
    # --------------------------------------------- Level --------------------------------------------- #
    if Can_Continue == True:
        for CPDI_Delivery in CPDI_Delivery_list:
            if CPDI_Level_Method == "Fixed":
                CPDI_Level = Fixed_CPDI_Level
            elif CPDI_Level_Method == "Purchase Order":
                CPDI_Level = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Purchase_Headers_df, Search_Column="HQCPDILevelRequestedFieldNUS", Filter_Column="No", Filter_Value=Purchase_Order)
            elif CPDI_Level_Method == "Random":
                CPDI_Levels_List = HQ_CPDI_Level_df["Level"].to_list()
                CPDI_Level = random.choice(seq=CPDI_Levels_List)
            elif CPDI_Level_Method == "Prompt":
                if GUI == True:
                    CPDI_Levels_List = HQ_CPDI_Level_df["Level"].to_list()
                    def Select_CPDI_Level(Frame_Body: CTkFrame):
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe"].children["!ctkframe3"].children["!ctkoptionmenu"]
                        Value_Level = Value_CTkEntry.get()
                        CPDI_Level_Variable.set(value=Value_Level)
                        CPDI_Level_Window.destroy()
                        
                    # TopUp Window
                    CPDI_Level_Window_geometry = (520, 500)
                    Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                    Main_Window_Centre[0] = Main_Window_Centre[0] - CPDI_Level_Window_geometry[0] //2
                    Main_Window_Centre[1] = Main_Window_Centre[1] - CPDI_Level_Window_geometry[1] //2
                    CPDI_Level_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"CPDI Level provided: {CPDI_Delivery}.", max_width=CPDI_Level_Window_geometry[0], max_height=CPDI_Level_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                    # Frame - General
                    Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=CPDI_Level_Window, Name=f"CPDI Level provided: {CPDI_Delivery}.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select provided CPDI Level for Purchase Order.", GUI_Level_ID=3)
                    Frame_Main.configure(bg_color = "#000001")
                    Frame_Body = Frame_Main.children["!ctkframe2"]

                    # CPDI Level
                    CPDI_Level_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"CPDI Level", Field_Type="Input_OptionMenu") 
                    CPDI_Level_Frame_Var = CPDI_Level_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    CPDI_Level_Frame_Var.set(value="")
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=CPDI_Level_Frame_Var, values=CPDI_Levels_List, command=None, GUI_Level_ID=3)

                    # Buttons
                    CPDI_Level_Variable = StringVar(master=CPDI_Level_Window, value="", name="CPDI_Level_Variable")
                    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                    Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                    Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_CPDI_Level(Frame_Body=Frame_Body))
                    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm CPDI Level.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                    Button_Confirm_Var.wait_variable(CPDI_Level_Variable)
                    CPDI_Level = CPDI_Level_Variable.get()
                else:
                    raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PO_CPDI_Messages:Level")
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"CPDI Level Method selected: {CPDI_Level_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    raise HTTPException(status_code=500, detail=f"CPDI Level Method selected: {CPDI_Level_Method} which is not supporter. Cancel File creation.")
                Can_Continue = False

            # --------------------------------------------- Status --------------------------------------------- #
            if Can_Continue == True:
                CPDI_Status_List = []
                if CPDI_Status_Method == "Fixed":
                    CPDI_Status_List.append(Fixed_CPDI_Status)
                elif CPDI_Status_Method == "All Statuses":
                    CPDI_Status_List = HQ_CPDI_Status_df["Status_Code"].to_list()
                elif CPDI_Status_Method == "Prompt":
                    if GUI == True:
                        Status_List_description = HQ_CPDI_Status_df["Status_Code"].to_list()
                        def Select_CPDI_status(Frame_Body: CTkFrame, Lines_No: int, CPDI_Status_List: list):
                            for i in range(0, Lines_No + 1):
                                if i == 0:
                                    i = ""
                                elif i == 1:
                                    continue
                                else:
                                    pass
                                
                                Value_CTkCheck = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkcheckbox"]
                                Value_CTkCheck_Value = Value_CTkCheck.get()
                                if Value_CTkCheck_Value == True:
                                    Selected_Status_No_label = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe"].children["!ctklabel"]
                                    Selected_Status_No = str(Selected_Status_No_label.cget("text"))
                                    Selected_Status_No = Selected_Status_No.replace(":", "")
                                    CPDI_Status_List.append(Selected_Status_No)
                                else:
                                    pass
                            CPDI_Status_Variable.set(value="Selected")
                            CPDI_Status_Window.destroy()
                        
                        # TopUp Window
                        CPDI_Status_Window_geometry = (520, 500)
                        Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                        Main_Window_Centre[0] = Main_Window_Centre[0] - CPDI_Status_Window_geometry[0] //2
                        Main_Window_Centre[1] = Main_Window_Centre[1] - CPDI_Status_Window_geometry[1] //2
                        CPDI_Status_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title=f"Select CPDI Status/s: {CPDI_Delivery}.", max_width=CPDI_Status_Window_geometry[0], max_height=CPDI_Status_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                        # Frame - General
                        Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=CPDI_Status_Window, Name=f"Select CPDI Status/s: {CPDI_Delivery}.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select which CPDI status be generated within Delivery.", GUI_Level_ID=3)
                        Frame_Body = Frame_Main.children["!ctkframe2"]

                        # Delivery list
                        Lines_No = len(Status_List_description)
                        for Status in Status_List_description:
                            # Fields
                            Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Status}", Field_Type="Input_CheckBox") 
                            Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                            Fields_Frame_Var.configure(text="")

                        # Dynamic Content height
                        content_row_count = len(Frame_Body.winfo_children())
                        content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                        if content_height > CPDI_Status_Window_geometry [1]:
                            content_height = CPDI_Status_Window_geometry [1]
                        Frame_Main.configure(bg_color = "#000001", height=content_height)

                        # Buttons
                        CPDI_Status_Variable = StringVar(master=CPDI_Status_Window, value="", name="CPDI_Status_Variable")
                        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                        Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_CPDI_status(Frame_Body=Frame_Body, Lines_No=Lines_No, CPDI_Status_List=CPDI_Status_List))
                        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm CPDI Status/s selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                        Button_Confirm_Var.wait_variable(CPDI_Status_Variable)
                    else:
                        raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PO_CPDI_Messages:Status")

                # --------------------------------------------- Export --------------------------------------------- #
                for CPDI_Status in CPDI_Status_List:
                    Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_CPDI")

                    # Assign Values
                    Current_line_json["statusinformation"]["delivery_number"] = CPDI_Delivery
                    Current_line_json["statusinformation"]["order_reason"] = CPDI_Level
                    Current_line_json["statusinformation"]["status"] = CPDI_Status
                    Current_line_json["statusinformation"]["purchase_order_number"] = Purchase_Order

                    # Export 
                    PO_CPDI_File_Name = f"CPDI_{CPDI_Delivery}_{CPDI_Level}_{CPDI_Status}"
                    if Export_NAV_Folder == True:
                        File_Manipulation.Export_NAV_Folders(Configuration=Configuration, window=window, NVR_FS_Connect_df=NVR_FS_Connect_df, HQ_Communication_Setup_df=HQ_Communication_Setup_df, Buy_from_Vendor_No=Buy_from_Vendor_No, File_Content=Current_line_json, HQ_File_Type_Path="HQ_CPDI_Import_Path", File_Name=PO_CPDI_File_Name, File_suffix="json", GUI=GUI)
                    else:
                        File_Manipulation.Export_Download_Folders(Configuration=Configuration, window=window, File_Content=Current_line_json, File_Name=PO_CPDI_File_Name, File_suffix="json", GUI=GUI)

                    del Current_line_json
            else:
                pass
    else:
        pass