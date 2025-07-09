# Import Libraries
from pandas import DataFrame
from datetime import datetime
from Libs.Azure.API_Error_Handler import APIError

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

try:
    # Front-End Library
    from customtkinter import CTk, CTkFrame, StringVar
    import Libs.CustomTkinter_Functions as CustomTkinter_Functions
except:
    pass

def Generate_Invoice_Header(Settings: dict, Configuration: dict|None, window: CTk|None, Purchase_Order: str, Purchase_Order_index: str, Purchase_Headers_df: DataFrame, PO_Confirmation_Number: str, PO_Delivery_Number_list: list, PO_Delivery_Date_list: list, Confirmed_Lines_df: DataFrame, Delivery_Lines_df: DataFrame, Company_Information_df: DataFrame, HQ_Communication_Setup_df: DataFrame, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    Invoice_Header_Template_List = []
    
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Method"]
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]
    PO_Invoice_Number_list = []

    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Method"]
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    PO_Currency = ""

    Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Method"]
    INV_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]
    INV_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Random_Options"]["From"]
    INV_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Invoice_Date"]["Random_Options"]["To"]
    PO_Invoice_Date_list = []

    # Filter Dataframes by Purchase Order
    mask_Purchase_Header = Purchase_Headers_df["No"] == Purchase_Order
    Purchase_Headers_df_Filtered = DataFrame(Purchase_Headers_df[mask_Purchase_Header])

    # --------------------------------------------- Preparation based on Delivery --------------------------------------------- #
    Invoice_Count = len(PO_Delivery_Number_list)

    # Load Template into list according to Invoice Count
    for i in range(1, Invoice_Count + 1 ):
        PO_Invoice_Header = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Invoice_Header")
        Invoice_Header_Template_List.append(PO_Invoice_Header)
        del PO_Invoice_Header

    # --------------------------------------------- Invoice Number --------------------------------------------- #
    if Can_Continue == True:
        if Invoice_Count == 1:
            if Numbers_Method == "Fixed":
                PO_Invoice_Number_list.append(Fixed_Number + Purchase_Order_index)
            elif Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                PO_Invoice_Number_list.append(Automatic_Prefix + Today_str + Purchase_Order_index)
            else:
                pass
        elif Invoice_Count > 1:
            if Numbers_Method == "Fixed":
                if GUI == True:
                    Numbers_Method = "Prompt"
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Invoice Number", message=f"Combination of Invoice Count = {Invoice_Count} and Number Method Setup: Fixed, do not allow this combination and method is automatically switched to Prompt.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    Numbers_Method = "Automatic"
            else:
                pass

            if Numbers_Method == "Automatic":
                Today_dt = datetime.now()
                Today_str = Today_dt.strftime(Numbers_DateTime_format)
                for i in range(1, Invoice_Count + 1 ):
                    PO_Invoice_Number_list.append(Automatic_Prefix + Today_str + Purchase_Order_index + "_" + str(i))
            else:
                pass

        if Numbers_Method == "Prompt":
            if GUI == True:
                def Select_Invoice_Number(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Invoice_Number_list = []
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
                            Value_Invoice = Value_CTkEntry.get()
                        except:
                            Value_Invoice = ""
                        if Value_Invoice == "":
                            Full_List = False
                        else:
                            PO_Invoice_Number_list.append(Value_Invoice + Purchase_Order_index)

                    if Full_List == True:
                        PO_Invoice_Number_list_joined = ";".join(PO_Invoice_Number_list)
                        PO_INV_Number_Variable.set(value=PO_Invoice_Number_list_joined)
                        PO_INV_Number_Window.destroy()
                    else:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Invoice Count", message=f"All Invoices must have an number, please fill all of them.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)

                # TopUp Window
                PO_INV_Number_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_INV_Number_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_INV_Number_Window_geometry[1] //2
                PO_INV_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Set Invoice Number/s.", max_width=PO_INV_Number_Window_geometry[0], max_height=PO_INV_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_INV_Number_Window, Name="Set Invoice Number/s.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To set Invoice Number based on Invoice Count.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Invoice Numbers
                for i in range(1, Invoice_Count + 1):
                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"Invoice {i}", Field_Type="Input_Normal") 
                    PO_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PO_Fields_Frame_Var.configure(placeholder_text="Manual Invoice Number", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = (content_row_count + 1) * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_INV_Number_Window_geometry[1]:
                    content_height = PO_INV_Number_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PO_INV_Number_Window.maxsize(width=PO_INV_Number_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_INV_Number_Variable = StringVar(master=PO_INV_Number_Window, value="", name="PO_INV_Number_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Invoice_Number(Frame_Body=Frame_Body, Lines_No=Invoice_Count))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Invoice Number/s selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_INV_Number_Variable)
                PO_Invoice_Number_list = PO_INV_Number_Variable.get().split(";")
            else:
                raise APIError(message="Any Prompt method is not allowed in API calls. Issue in Generate_Invoice_Header:Invoice_Number.", status_code=500, charset="utf-8")
    else:
        pass

    for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
        # Fill value in template
        Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_id"] = Invoice_Number

    # --------------------------------------------- Invoice Date --------------------------------------------- #
    if Can_Continue == True:
        if Invoice_Count == 1:
            if Posting_Date_Method == "Fixed":
                PO_Invoice_Date_list.append(INV_Fix_Date)
            elif Posting_Date_Method == "Random":
                Invoice_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=INV_Rand_From_Date, To_int=INV_Rand_To_Date, Format=Date_format)
                PO_Invoice_Date_list.append(Invoice_Date)
            elif Posting_Date_Method == "Today":
                Today_dt = datetime.now()
                Today = Today_dt.strftime(Date_format)
                PO_Invoice_Date_list.append(Today)
            else:
                pass
        elif Invoice_Count > 1:
            if Posting_Date_Method == "Fixed":
                if GUI == True:
                    Posting_Date_Method = "Prompt"
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Invoice Date", message=f"Combination of Invoice Count = {Invoice_Count} and Invoice Date Method Setup: Fixed, do not allow this combination and method is automatically switched to Prompt.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    Posting_Date_Method = "Random"
            else:
                pass

            if Posting_Date_Method == "Random":
                for i in range(1, Invoice_Count + 1):
                    Invoice_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=INV_Rand_From_Date, To_int=INV_Rand_To_Date, Format=Date_format)
                    PO_Invoice_Date_list.append(Invoice_Date)
            elif Posting_Date_Method == "Today":
                Today_dt = datetime.now()
                Today = Today_dt.strftime(Date_format)
                for i in range(1, Invoice_Count + 1):
                    PO_Invoice_Date_list.append(Today)
            else:
                pass

        if Posting_Date_Method == "Prompt":
            if GUI == True:
                def Select_Invoice_Date(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Invoice_Date_list = []
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
                            PO_Invoice_Date_list.append(Value_Date)

                    if Full_List == True:
                        PO_Invoice_Date_list_joined = ";".join(PO_Invoice_Date_list)
                        PO_INV_Date_Variable.set(value=PO_Invoice_Date_list_joined)
                        PO_INV_Date_Window.destroy()
                    else:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Delivery Date", message=f"All Deliveries must have an date, please fill all of them.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)

                # TopUp Window
                PO_INV_Date_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_INV_Date_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_INV_Date_Window_geometry[1] //2
                PO_INV_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Set Invoice Date for Invoice/s.", max_width=PO_INV_Date_Window_geometry[0], max_height=PO_INV_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_INV_Date_Window, Name="Set Invoice Date for Invoice/s.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To set Invoice Date based on Invoice Count.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Invoice Date Fields
                for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
                    # Fields
                    Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Invoice_Number}",  Field_Type="Date_Picker", Validation="Date")  
                    Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                    Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
                    Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
                    # BUG --> Date Picker pointing only to last Invoice
                    Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
                    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = (content_row_count + 1) * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > PO_INV_Date_Window_geometry[1]:
                    content_height = PO_INV_Date_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PO_INV_Date_Window.maxsize(width=PO_INV_Date_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_INV_Date_Variable = StringVar(master=PO_INV_Date_Window, value="", name="PO_INV_Date_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Invoice_Date(Frame_Body=Frame_Body, Lines_No=Invoice_Count))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Invoice Date/s selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_INV_Date_Variable)
                PO_Invoice_Date_list = PO_INV_Date_Variable.get().split(";")
            else:
                raise APIError(message=f"Any Prompt method is not allowed in API calls. Issue in Generate_Invoice_Header:Invoice_Date.", status_code=500, charset="utf-8")
        else:
            pass
        # Fill value in template
        for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
            # Fill value in template
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["control_info"]["generation_date"] = PO_Invoice_Date_list[Invoice_Index]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_date"] = PO_Invoice_Date_list[Invoice_Index]
    else:
        pass

    # --------------------------------------------- Currency --------------------------------------------- #
    if Can_Continue == True:
        if Currency_Method == "Fixed":
            PO_Currency = Fixed_Currency
        elif Currency_Method == "Purchase Order":
            PO_Currency = Purchase_Headers_df_Filtered.iloc[0]["Currency_Code"]
        elif Currency_Method == "From Confirmation":
            PO_Currency = Confirmed_Lines_df.iloc[0]["price_currency"]
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Currency Method selected: {Currency_Method} which is not supporter. Issue in Generate_Invoice_Header:Currency", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise APIError(message=f"Currency Method selected: {Currency_Method} which is not supporter. Issue in Generate_Invoice_Header:Currency.", status_code=500, charset="utf-8")
            Can_Continue = False

        # Fill value in template
        for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
            # Fill value in template
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["price_currency"] = PO_Currency
    else:
        pass

    # --------------------------------------------- Orders --------------------------------------------- #        
    if Can_Continue == True:
        for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["order_history"]["order_id"] = Purchase_Order
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["order_history"]["supplier_order_id"] = PO_Confirmation_Number
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["order_history"]["order_date"] = Delivery_Lines_df.iloc[0]["order_date"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["order_history"]["delivery_note_id"] = PO_Delivery_Number_list[Invoice_Index]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["order_history"]["delivery_note_date"] = PO_Delivery_Date_list[Invoice_Index]
    else:
        pass

    # --------------------------------------------- Order Date --------------------------------------------- #
    if Can_Continue == True:
        for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["delivery_date"]["delivery_start_date"] = PO_Delivery_Date_list[Invoice_Index]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["delivery_date"]["delivery_end_date"] = PO_Delivery_Date_list[Invoice_Index]
    else:
        pass

    # --------------------------------------------- HQ Identification No --------------------------------------------- #
    if Can_Continue == True:
        for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
    else:
        pass

    # --------------------------------------------- Company Information --------------------------------------------- #
    if Can_Continue == True:
        for Invoice_Index, Invoice_Number in enumerate(PO_Invoice_Number_list):
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
            Invoice_Header_Template_List[Invoice_Index]["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]
    else:
        pass

    return Invoice_Header_Template_List, PO_Invoice_Number_list