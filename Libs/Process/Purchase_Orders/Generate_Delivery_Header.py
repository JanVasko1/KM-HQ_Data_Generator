# Import Libraries
from pandas import DataFrame
from datetime import datetime
import random
from fastapi import HTTPException

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Pandas_Functions as Pandas_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, StringVar, IntVar

def Generate_Delivery_Header(Settings: dict, Configuration: dict|None, window: CTk|None, Purchase_Order: str, Purchase_Order_index: str, Purchase_Headers_df: DataFrame, Company_Information_df: DataFrame, HQ_Communication_Setup_df: DataFrame, Confirmed_Lines_df: DataFrame, Shipping_Agent_list: list, Shipment_Method_list: list, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    Delivery_Header_Template_List = []
    
    DEL_Count_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Method"]
    Random_Max_count = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Random_Options"]["Random_Max_count"]
    Fixed_Count = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Counts"]["Fixed_Options"]["Count"]
    Delivery_Count = 0

    DEL_Assignment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["Method"]
    DEL_FOCH_with_Main = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Item_Delivery_Assignment"]["FreeOfCharge_with_Main"]

    PO_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Method"]
    PO_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Automatic_Options"]["Prefix"]
    PO_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Number"]["Fixed_Options"]["Number"]
    PO_Delivery_Number_list = []

    Delivery_Dates_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Method"]
    DEL_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Fixed_Options"]["Fix_Date"]
    DEL_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Random_Options"]["From"]
    DEL_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Date"]["Random_Options"]["To"]
    PO_Delivery_Date_list = []

    Carrier_ID_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Method"]
    Carrier_ID_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Carrier_ID"]["Fixed_Options"]["Fix_Carrier"]
    Carrier_ID_List = []

    BOL_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Method"]
    BOL_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Automatic_Options"]["Prefix"]
    BOL_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Delivery_Tracking_Information"]["BillOfLanding"]["Number"]["Fixed_Options"]["Fixed_BOL"]
    BOL_List = []

    Shipment_Method = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Method"]
    Shipment_Method_Fixed = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Shipment_Method"]["Fixed_Options"]["Fixed_Shipment_Method"]
    Shipment_Method_Select_List = []

    # --------------------------------------------- Delivery Count --------------------------------------------- #
    #Complete / Partial Shipments
    CompleteDeliveryFieldNUS = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Purchase_Headers_df, Search_Column="CompleteDeliveryFieldNUS", Filter_Column="No", Filter_Value=Purchase_Order)
    if CompleteDeliveryFieldNUS == "True":
        CompleteDeliveryFieldNUS = True
    else:
        CompleteDeliveryFieldNUS = False

    if CompleteDeliveryFieldNUS == True:
        Delivery_Count = 1
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Count", message=f"Program set Delivery Count = 1 as Purchase Order is marked as Complete Delivery.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
    else:
        if DEL_Count_Method == "Fixed":
            Delivery_Count = Fixed_Count
        elif DEL_Count_Method == "Random":
            if DEL_Assignment_Method == "Full random":
                Sum_Qty = int(Confirmed_Lines_df["quantity"].sum())
                if DEL_FOCH_with_Main == True:
                    # TODO --> Minus FOCH Qty from whole Sum_Qty --> not to separate them on Delivery later 
                    pass 
                else:
                    pass
                Delivery_Count = random.randint(1, Sum_Qty)
            elif DEL_Assignment_Method == "Lines random":
                Sum_Lines = len(Confirmed_Lines_df)
                if DEL_FOCH_with_Main == True:
                    # TODO --> Minus FOCH lines count from whole Sum_Lines --> not to separate them on Delivery later 
                    pass 
                else:
                    pass
                Delivery_Count = random.randint(1, Sum_Lines)
            elif DEL_Assignment_Method == "Prompt":
                # Should define same Delivery Count as in whole Line Random
                Sum_Lines = len(Confirmed_Lines_df)
                if DEL_FOCH_with_Main == True:
                    # TODO --> Minus FOCH lines count from whole Sum_Lines --> not to separate them on Delivery later 
                    pass 
                else:
                    pass
                Delivery_Count = random.randint(1, Sum_Lines)
            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Random Method selected: {DEL_Assignment_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                Can_Continue = False
        elif DEL_Count_Method == "Prompt":
            if GUI == True:
                def Select_PO_DEL_Number(Prompt_Count_Frame: CTkFrame):
                    PO_DEL_Count_Var = Prompt_Count_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PO_DEL_Number = int(PO_DEL_Count_Var.get())
                    PO_DEL_Count_Variable.set(value=PO_DEL_Number)
                    PO_DEL_Count_Window.destroy()
                    
                # TopUp Window
                PO_DEL_Count_Window_geometry = (500, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_DEL_Count_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_DEL_Count_Window_geometry[1] //2
                PO_DEL_Count_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Delivery Count.", max_width=PO_DEL_Count_Window_geometry[0], max_height=PO_DEL_Count_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_DEL_Count_Window, Name="Select Delivery Count.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select number of BEU Deliveries.", GUI_Level_ID=3)
                Frame_Main.configure(bg_color = "#000001")
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Prompt_Count_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Delivery Number",  Field_Type="Input_Normal", Validation="Integer")  
                Prompt_Count_Frame_Var = Prompt_Count_Frame.children["!ctkframe3"].children["!ctkentry"]
                Prompt_Count_Frame_Var.configure(placeholder_text="Insert Delivery Count", placeholder_text_color="#949A9F")

                # Buttons
                PO_DEL_Count_Variable = IntVar(master=PO_DEL_Count_Window, value=0, name="PO_DEL_Count_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_DEL_Number(Prompt_Count_Frame=Prompt_Count_Frame))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm POs Delivery Counts.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_DEL_Count_Variable)
                Delivery_Count = PO_DEL_Count_Variable.get()
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Delivery_Header:Delivery_Count")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Count Method selected: {DEL_Count_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Delivery Count Method selected: {DEL_Count_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False

    # Max Delivery Count is only Random
    if DEL_Count_Method == "Random":
        if Delivery_Count > Random_Max_count:
            Delivery_Count = Random_Max_count
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Count", message=f"Program set Delivery Count = {Random_Max_count} as this is maximal Deliveries set in setup.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Program set Delivery Count = {Random_Max_count} as this is maximal Deliveries set in setup.")
        else:
            pass
    else:
        pass

    Sum_Confirmed_Lines = int(Confirmed_Lines_df["quantity"].sum())
    if Delivery_Count > Sum_Confirmed_Lines:
        Delivery_Count = Sum_Confirmed_Lines
        if GUI == True:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Count", message=f"Program set Delivery Count = {Sum_Confirmed_Lines} as your choice was higher that PO lines quantity.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
        else:
            raise HTTPException(status_code=500, detail=f"Program set Delivery Count = {Sum_Confirmed_Lines} as your choice was higher that PO lines quantity.")
    else:
        pass

    # Load Template into list according to Delivery Count
    for i in range(1, Delivery_Count + 1 ):
        PO_Delivery_Header = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Delivery_Header")
        Delivery_Header_Template_List.append(PO_Delivery_Header)
        del PO_Delivery_Header

    # --------------------------------------------- Delivery Number --------------------------------------------- #
    if Can_Continue == True:
        if Delivery_Count == 1:
            if PO_Numbers_Method == "Fixed":
                PO_Delivery_Number_list.append(PO_Fixed_Number + Purchase_Order_index)
            elif PO_Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                PO_Delivery_Number_list.append(PO_Automatic_Prefix + Today_str + Purchase_Order_index)
            else:
                pass
        elif Delivery_Count > 1:
            if PO_Numbers_Method == "Fixed":
                if GUI == True:
                    PO_Numbers_Method = "Prompt"
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Count", message=f"Combination of Delivery Count = {Delivery_Count} and Number Method Setup: Fixed, do not allow this combination and method is automatically switched to Prompt.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    PO_Numbers_Method = "Automatic"
            else:
                pass

            if PO_Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                for i in range(1, Delivery_Count + 1 ):
                    PO_Delivery_Number_list.append(PO_Automatic_Prefix + Today_str + Purchase_Order_index + "_" + str(i))
            else:
                pass
        
        if PO_Numbers_Method == "Prompt":
            if GUI == True:
                def Select_Delivery_Number(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Delivery_Number_list = []
                    Full_List = True
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkentry"]
                        try:
                            Value_Delivery = Value_CTkEntry.get()
                        except:
                            Value_Delivery = ""
                        if Value_Delivery == "":
                            Full_List = False
                        else:
                            PO_Delivery_Number_list.append(Value_Delivery + Purchase_Order_index)

                    if Full_List == True:
                        PO_Delivery_Number_list_joined = ";".join(PO_Delivery_Number_list)
                        PO_DEL_Number_Variable.set(value=PO_Delivery_Number_list_joined)
                        PO_DEL_Number_Window.destroy()
                    else:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Count", message=f"All Deliveries must have an number, please fill all of them.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)

                # TopUp Window
                PO_DEL_Number_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_DEL_Number_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_DEL_Number_Window_geometry[1] //2
                PO_DEL_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Set Delivery Number/s.", max_width=PO_DEL_Number_Window_geometry[0], max_height=PO_DEL_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_DEL_Number_Window, Name="Set Delivery Number/s.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To set Delivery Number based on Delivery Count.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Numbers
                for i in range(1, Delivery_Count + 1):
                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"Delivery {i}", Field_Type="Input_Normal") 
                    PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PO_Fields_Frame_Var.configure(placeholder_text="Manual Delivery Number", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_DEL_Number_Window_geometry[1]:
                    content_height = PO_DEL_Number_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PO_DEL_Number_Window.maxsize(width=PO_DEL_Number_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_DEL_Number_Variable = StringVar(master=PO_DEL_Number_Window, value="", name="PO_DEL_Number_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Delivery_Number(Frame_Body=Frame_Body, Lines_No=Delivery_Count))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Delivery Number/s selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_DEL_Number_Variable)
                PO_Delivery_Number_list = PO_DEL_Number_Variable.get().split(";")
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Delivery_Header:Delivery_Number")
        else:
            pass
    else:
        pass    

    for i in range(0, Delivery_Count):
        # Fill value in template
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["dispatchnotification_id"] = PO_Delivery_Number_list[i]

    # --------------------------------------------- Delivery Date --------------------------------------------- #
    if Can_Continue == True:
        if Delivery_Count == 1:
            if Delivery_Dates_Method == "Fixed":
                PO_Delivery_Date_list.append(DEL_Fix_Date)
            elif Delivery_Dates_Method == "Random":
                Delivery_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=DEL_Rand_From_Date, To_int=DEL_Rand_To_Date, Format=Date_format)
                PO_Delivery_Date_list.append(Delivery_Date)
            else:
                pass
        elif Delivery_Count > 1:
            if Delivery_Dates_Method == "Fixed":
                if GUI == True:
                    Delivery_Dates_Method = "Prompt"
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Date", message=f"Combination of Delivery Count = {Delivery_Count} and Date Method Setup: Fixed, do not allow this combination and method is automatically switched to Prompt.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    Delivery_Dates_Method = "Random"
            else:
                pass

            if Delivery_Dates_Method == "Random":
                for i in range(1, Delivery_Count + 1):
                    Delivery_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=DEL_Rand_From_Date, To_int=DEL_Rand_To_Date, Format=Date_format)
                    PO_Delivery_Date_list.append(Delivery_Date)
            else:
                pass
        
        if Delivery_Dates_Method == "Prompt":
            if GUI == True:
                def Select_Delivery_Number(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Delivery_Date_list = []
                    Full_List = True
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkentry"]
                        try:
                            Value_Date = Value_CTkEntry.get()
                        except:
                            Value_Date = ""
                        if Value_Date == "":
                            Full_List = False
                        else:
                            PO_Delivery_Date_list.append(Value_Date)

                    if Full_List == True:
                        PO_Delivery_Date_list_joined = ";".join(PO_Delivery_Date_list)
                        PO_DEL_Date_Variable.set(value=PO_Delivery_Date_list_joined)
                        PO_DEL_Date_Window.destroy()
                    else:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Date", message=f"All Deliveries must have an date, please fill all of them.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)

                # TopUp Window
                PO_DEL_Date_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_DEL_Date_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_DEL_Date_Window_geometry[1] //2
                PO_DEL_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Set Delivery Date for Delivery/s.", max_width=PO_DEL_Date_Window_geometry[0], max_height=PO_DEL_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_DEL_Date_Window, Name="Set Delivery Date for Delivery/s.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To set Delivery Date based on Delivery Count.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Delivery Date Fields
                for Delivery in PO_Delivery_Number_list:
                    # Fields
                    Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Delivery}",  Field_Type="Date_Picker", Validation="Date")  
                    Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                    Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
                    Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
                    # BUG --> Date Picker pointing only to last delivery
                    Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
                    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_DEL_Date_Window_geometry[1]:
                    content_height = PO_DEL_Date_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PO_DEL_Date_Window.maxsize(width=PO_DEL_Date_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_DEL_Date_Variable = StringVar(master=PO_DEL_Date_Window, value="", name="PO_DEL_Date_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Delivery_Number(Frame_Body=Frame_Body, Lines_No=Delivery_Count))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Delivery Date/s selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_DEL_Date_Variable)
                PO_Delivery_Date_list = PO_DEL_Date_Variable.get().split(";")
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Delivery_Header:Delivery_Date")
        else:
            pass
    else:
        pass   

    for i in range(0, Delivery_Count):
        delivery_date = PO_Delivery_Date_list[i]
        planned_gi_date = Defaults_Lists.DateString_minus_Number_Day(Date_str=delivery_date, No_Days=-1, Format=Date_format)
        loading_date = Defaults_Lists.DateString_minus_Number_Day(Date_str=delivery_date, No_Days=-1, Format=Date_format)
        trans_planning_date = Defaults_Lists.DateString_minus_Number_Day(Date_str=delivery_date, No_Days=-2, Format=Date_format)
        picking_date = Defaults_Lists.DateString_minus_Number_Day(Date_str=delivery_date, No_Days=-2, Format=Date_format)
        generation_date = Defaults_Lists.DateString_minus_Number_Day(Date_str=delivery_date, No_Days=-2, Format=Date_format)
        
        # Fill value in template
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["generation_date"] = generation_date
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["picking_date"] = picking_date
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["trans_planning_date"] = trans_planning_date
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["loading_date"] = loading_date
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["planned_gi_date"] = planned_gi_date
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["control_info"]["delivery_date"] = delivery_date

    # --------------------------------------------- Carrier ID --------------------------------------------- #
    if Can_Continue == True:
        for i in range(0, Delivery_Count):
            if Carrier_ID_Method == "Fixed":
                Carrier_ID_List.append(Carrier_ID_Fixed)
            elif Carrier_ID_Method == "Random":
                Current_Carrier_ID = random.choice(seq=Shipping_Agent_list)
                Carrier_ID_List.append(Current_Carrier_ID)
            elif Carrier_ID_Method == "Empty":
                Carrier_ID_List.append("")
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Carrier ID Method selected: {Carrier_ID_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    raise HTTPException(status_code=500, detail=f"Delivery Carrier ID Method selected: {Carrier_ID_Method} which is not supporter. Cancel File creation.")
                Can_Continue = False
    
    for i in range(0, Delivery_Count):
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["carrier_id"] = Carrier_ID_List[i]

    # --------------------------------------------- Bill of Landing No --------------------------------------------- #
    if Can_Continue == True:
        for i in range(0, Delivery_Count):
            if BOL_Numbers_Method == "Fixed":
                BOL_List.append(BOL_Fixed_Number)
            elif BOL_Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                BOL_List.append(BOL_Automatic_Prefix + Today_str + "_" + str(i))
            elif BOL_Numbers_Method == "Empty":
                BOL_List.append("")
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery BOL Method selected: {BOL_Numbers_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    raise HTTPException(status_code=500, detail=f"Delivery BOL Method selected: {BOL_Numbers_Method} which is not supporter. Cancel File creation.")
                Can_Continue = False
    
    for i in range(0, Delivery_Count):
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["remarks"]["bolnr"] = BOL_List[i]

    # Footer
    # --------------------------------------------- Shipment Method --------------------------------------------- #
    if Can_Continue == True:
        for i in range(0, Delivery_Count):
            if Shipment_Method == "Fixed":
                Shipment_Method_Select_List.append(Shipment_Method_Fixed)
            elif Shipment_Method == "Random":
                Current_Shipment_Method = random.choice(seq=Shipment_Method_list)
                Shipment_Method_Select_List.append(Current_Shipment_Method)
            elif Shipment_Method == "Empty":
                Shipment_Method_Select_List.append("")
            else:
                if GUI == True:
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Delivery Shipment Method selected: {Shipment_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    raise HTTPException(status_code=500, detail=f"Delivery Shipment Method selected: {Shipment_Method} which is not supporter. Cancel File creation.")
                Can_Continue = False
    
    for i in range(0, Delivery_Count):
        Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_summary"]["incoterms1"] = Shipment_Method_Select_List[i]

    # --------------------------------------------- Company Information --------------------------------------------- #
    if Can_Continue == True:
        HQ_Identification_No_NUS = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Purchase_Headers_df, Search_Column="HQ_Identification_No_NUS", Filter_Column="No", Filter_Value=Purchase_Order)
        for i in range(0, Delivery_Count):
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["buyer_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["buyer_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["buyer_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["buyer_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["buyer_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["shipment_parties"]["delivery_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["shipment_parties"]["delivery_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["shipment_parties"]["delivery_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["shipment_parties"]["delivery_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["shipment_parties"]["delivery_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["buyer_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
            Delivery_Header_Template_List[i]["dispatchnotification"]["dispatchnotification_header"]["dispatchnotification_info"]["shipment_parties"]["delivery_party"]["party"]["party_id"] = HQ_Identification_No_NUS
    else:
        pass

    return Delivery_Header_Template_List, PO_Delivery_Number_list, PO_Delivery_Date_list, Delivery_Count

