# Import Libraries
from pandas import DataFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta

from customtkinter import CTk, CTkFrame, StringVar

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups


def Generate_BB_Header(Settings: dict, Configuration: dict, window: CTk, Company_Information_df: DataFrame, HQ_Communication_Setup_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    BB_Invoice_Header = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="BB_Invoice_Header")
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    
    BB_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Method"]
    BB_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Automatic_Options"]["Prefix"]
    BB_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Number"]["Fixed_Options"]["Number"]
    BB_Number = ""

    BB_Invoice_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Method"]
    BB_ID_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]
    BB_Invoice_Date = ""

    BB_Order_id_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Method"]
    BB_Fixed_Order_id = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_id"]["Fixed_Options"]["Fixed_Order_ID"]
    BB_Order_ID = ""
    BB_supplier_order_id = ""

    BB_Order_date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Method"]
    BB_OD_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Order_reference"]["Order_date"]["Fixed_Options"]["Fixed_Order_Date"]
    BB_Order_Date = ""

    BB_Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Currency"]["Fix_Currency"]
    BB_Currency = ""

    # --------------------------------------------- Invoice Number --------------------------------------------- #
    if Can_Continue == True:
        if BB_Numbers_Method == "Fixed":
            BB_Number = BB_Fixed_Number
        elif BB_Numbers_Method == "Automatic":
            Today_dt = datetime.now()
            Today_str = Today_dt.strftime(Numbers_DateTime_format)
            BB_Number = BB_Automatic_Prefix + Today_str
        elif BB_Numbers_Method == "Prompt":
            def Select_BB_Number(Prompt_Number_Frame: CTkFrame):
                Invoice_Number_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
                BB_Number = Invoice_Number_Var.get()
                BB_Number_Variable.set(value=BB_Number)
                BB_Number_Window.destroy()
                
            # TopUp Window
            BB_Number_Window_geometry = (500, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Number_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Number_Window_geometry[1] //2
            BB_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Invoice Number.", max_width=BB_Number_Window_geometry[0], max_height=BB_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=BB_Number_Window, Name="Select BackBone Billing Invoice Number.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select number of BackBone Billing Invoice.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            Prompt_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Invoice Number",  Field_Type="Input_Normal")  
            Prompt_Number_Frame_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
            Prompt_Number_Frame_Var.configure(placeholder_text="Insert your Invoice Number", placeholder_text_color="#949A9F")

            # Buttons
            BB_Number_Variable = StringVar(master=BB_Number_Window, value="", name="BB_Number_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Number(Prompt_Number_Frame=Prompt_Number_Frame))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Invoice Number.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(BB_Number_Variable)
            BB_Number = BB_Number_Variable.get()
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Invoice Number Method selected: {BB_Numbers_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
        
        # Fill value in template
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_id"] = BB_Number
    else:
        pass

    # --------------------------------------------- Invoice Date --------------------------------------------- #
    if Can_Continue == True:
        if BB_Invoice_Date_Method == "Fixed":
            BB_Invoice_Date = BB_ID_Fix_Date
        elif BB_Invoice_Date_Method == "Today":
            Today_dt = datetime.now()
            BB_Invoice_Date = Today_dt.strftime(Date_format)
        elif BB_Invoice_Date_Method == "Prompt":
            def Select_BB_Invoice_Date(Prompt_Date_Frame: CTkFrame):
                Invoice_Date_Var =  Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                BB_Invoice_Date = Invoice_Date_Var.get()
                BB_Invoice_Date_Variable.set(value=BB_Invoice_Date)
                BB_Inv_Date_Window.destroy()
                
            # TopUp Window
            BB_Inv_Date_Window_geometry = (500, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Inv_Date_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Inv_Date_Window_geometry[1] //2
            BB_Inv_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Invoice Date.", max_width=BB_Inv_Date_Window_geometry[0], max_height=BB_Inv_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=BB_Inv_Date_Window, Name="Select BackBone Billing Invoice Date.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select date of BackBone Billing Invoice.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Invoice Date",  Field_Type="Date_Picker", Validation="Date")  
            Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
            Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
            Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
            Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

            # Buttons
            BB_Invoice_Date_Variable = StringVar(master=BB_Inv_Date_Window, value="", name="BB_Invoice_Date_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Invoice_Date(Prompt_Date_Frame=Prompt_Date_Frame))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Invoice Date.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(BB_Invoice_Date_Variable)
            BB_Invoice_Date = BB_Invoice_Date_Variable.get()
            
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Invoice Date Method selected: {BB_Invoice_Date_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Fill value in template
        BB_Invoice_Header["invoice"]["invoice_header"]["control_info"]["generation_date"] = BB_Invoice_Date
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_date"] = BB_Invoice_Date
    else:
        pass

    # --------------------------------------------- Order ID --------------------------------------------- #
    if Can_Continue == True:
        if BB_Order_id_Method == "Fixed":
            BB_Order_ID = BB_Fixed_Order_id
        elif BB_Order_id_Method == "Previous Month":
            Today_dt = datetime.now()
            previous_month_date = Today_dt - relativedelta(months=1)
            BB_Order_ID = previous_month_date.strftime("%B_%Y")
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Invoice Order ID Method selected: {BB_Order_id_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Fill value in template
        BB_Invoice_Header["invoice"]["invoice_header"]["order_history"]["order_id"] = BB_Order_ID
    else:
        pass

    # --------------------------------------------- Supplier Order ID --------------------------------------------- #
    BB_supplier_order_id = "CON" + BB_Order_ID
    BB_Invoice_Header["invoice"]["invoice_header"]["order_history"]["supplier_order_id"] = BB_supplier_order_id

    # --------------------------------------------- Order Date --------------------------------------------- #
    if Can_Continue == True:
        if BB_Order_date_Method == "Fixed":
            BB_Order_Date = BB_OD_Fix_Date
        elif BB_Order_date_Method == "Invoice date":
            BB_Order_Date = BB_Invoice_Date
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Invoice Order Date Method selected: {BB_Order_date_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Fill value in template
        BB_Invoice_Header["invoice"]["invoice_header"]["order_history"]["order_date"] = BB_Order_Date
    else:
        pass

    # --------------------------------------------- Currency --------------------------------------------- #
    if Can_Continue == True:
        BB_Currency = BB_Fixed_Currency
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["price_currency"] = BB_Currency
    else:
        pass

    # --------------------------------------------- HQ Identification No --------------------------------------------- #
    if Can_Continue == True:
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
    else:
        pass

    # --------------------------------------------- Company Information --------------------------------------------- #
    if Can_Continue == True:
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        BB_Invoice_Header["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]
    else:
        pass

    return BB_Invoice_Header, BB_Number, BB_Order_ID, BB_supplier_order_id, BB_Order_Date