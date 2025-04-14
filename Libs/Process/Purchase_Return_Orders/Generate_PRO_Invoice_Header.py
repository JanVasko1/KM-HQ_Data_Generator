# Import Libraries
from pandas import DataFrame
from datetime import datetime
from fastapi import HTTPException

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, StringVar

def Generate_Credit_Memo_Header(Settings: dict, Configuration: dict|None, window: CTk|None, Purchase_Return_Order: str, Purchase_Return_Headers_df: DataFrame, PRO_Confirmation_Number: str, PRO_Return_Shipment_list: list, PRO_Confirmed_Lines_df: DataFrame, Company_Information_df: DataFrame, HQ_Communication_Setup_df: DataFrame, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]
    PRO_Credit_Memos = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PRO_Credit_Memo_Header")
    PRO_Return_Shipment_Number = ""
    
    Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Method"]
    Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Automatic_Options"]["Prefix"]
    Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Number"]["Fixed_Options"]["Number"]
    PRO_Credit_Number = ""

    Currency_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Currency"]["Method"]
    Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    PRO_Currency = ""

    Posting_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Method"]
    INV_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Fixed_Options"]["Fix_Date"]
    INV_Rand_From_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Random_Options"]["From"]
    INV_Rand_To_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Invoice_Date"]["Random_Options"]["To"]
    PRO_Invoice_Date = []

    # Filter Dataframes by Purchase Return Order
    mask_Purchase_Return_Header = Purchase_Return_Headers_df["No"] == Purchase_Return_Order
    Purchase_Ret_Headers_df_Filtered = DataFrame(Purchase_Return_Headers_df[mask_Purchase_Return_Header])

    # --------------------------------------------- Preparation based on Return Shipment --------------------------------------------- #
    if GUI == False:
        def Select_PRO_Shipment(Frame_Body: CTkFrame):
            Value_CTkEntry = Frame_Body.children[f"!ctkframe"].children["!ctkframe3"].children["!ctkoptionmenu"]
            Value_PRO_Shipment = Value_CTkEntry.get()
            PRO_Return_Shipment_Variable.set(value=Value_PRO_Shipment)
            PRO_Shipment_Window.destroy()
            
        # TopUp Window
        PRO_Shipment_geometry = (500, 250)
        Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
        Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_Shipment_geometry[0] //2
        Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_Shipment_geometry[1] //2
        PRO_Shipment_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Posted Return Shipment.", max_width=PRO_Shipment_geometry[0], max_height=PRO_Shipment_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PRO_Shipment_Window, Name="Select Posted Return Shipment.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select Posted Return Shipment for Credit Memo creation.", GUI_Level_ID=3)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"Posted Return Shipment", Field_Type="Input_OptionMenu") 
        Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
        Fields_Frame_Var.set(value="")
        Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Fields_Frame_Var, values=PRO_Return_Shipment_list, command=None, GUI_Level_ID=3)

        # Buttons
        PRO_Return_Shipment_Variable = StringVar(master=PRO_Shipment_Window, value="", name="PRO_Return_Shipment_Variable")
        Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
        Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
        Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_Shipment(Frame_Body=Frame_Body))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Posted Return Shipment.", ToolTip_Size="Normal", GUI_Level_ID=3)   
        Button_Confirm_Var.wait_variable(PRO_Return_Shipment_Variable)
        PRO_Return_Shipment_Number = PRO_Return_Shipment_Variable.get()
    else:
        PRO_Return_Shipment_Number = PRO_Return_Shipment_list[1]
        
    # --------------------------------------------- Invoice Number --------------------------------------------- #
    if Can_Continue == True:
        if Numbers_Method == "Fixed":
            PRO_Credit_Number = Fixed_Number
        elif Numbers_Method == "Automatic":
            Today_dt = datetime.now()
            Today_str = Today_dt.strftime(Numbers_DateTime_format)
            PRO_Credit_Number = Automatic_Prefix + Today_str
        elif Numbers_Method == "Prompt":
            if GUI == True:
                def Select_CR_Number(Prompt_Number_Frame: CTkFrame):
                    Invoice_Number_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
                    CR_Number = Invoice_Number_Var.get()
                    CR_Number_Variable.set(value=CR_Number)
                    CR_Number_Window.destroy()
                    
                # TopUp Window
                CR_Number_Window_geometry = (500, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - CR_Number_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - CR_Number_Window_geometry[1] //2
                CR_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Credit Memo Number.", max_width=CR_Number_Window_geometry[0], max_height=CR_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=CR_Number_Window, Name="Select Credit Memo Number.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select number of Credit Memo.", GUI_Level_ID=3)
                Frame_Main.configure(bg_color = "#000001")
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Prompt_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Credit Memo Number",  Field_Type="Input_Normal")  
                Prompt_Number_Frame_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
                Prompt_Number_Frame_Var.configure(placeholder_text="Insert your Credit Memo Number", placeholder_text_color="#949A9F")

                # Buttons
                CR_Number_Variable = StringVar(master=CR_Number_Window, value="", name="CR_Number_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_CR_Number(Prompt_Number_Frame=Prompt_Number_Frame))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Credit Memo Number.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(CR_Number_Variable)
                PRO_Credit_Number = CR_Number_Variable.get()
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Credit_Memo_Header:Invoice_Number")
    else:
        pass

    PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_id"] = PRO_Credit_Number

    # --------------------------------------------- Invoice Date --------------------------------------------- #
    if Can_Continue == True:
        if Posting_Date_Method == "Fixed":
            PRO_Invoice_Date = INV_Fix_Date
        elif Posting_Date_Method == "Random":
            Invoice_Date = Defaults_Lists.Date_Random_from_CurrentDay_plus_Interval(From_int=INV_Rand_From_Date, To_int=INV_Rand_To_Date, Format=Date_format)
            PRO_Invoice_Date = Invoice_Date
        elif Posting_Date_Method == "Today":
            Today_dt = datetime.now()
            Today = Today_dt.strftime(Date_format)
            PRO_Invoice_Date = Today
        elif Posting_Date_Method == "Prompt":
            if GUI == True:
                def Select_PRO_iNV_Date_Date(Prompt_Date_Frame: CTkFrame):
                    Invoice_Date_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PRO_Inv_Date = Invoice_Date_Var.get()
                    PRO_Inv_Date_Variable.set(value=PRO_Inv_Date)
                    PRO_Inv_Date_Window.destroy()
                    
                # TopUp Window
                PRO_Inv_Date_Window_geometry = (500, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_Inv_Date_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_Inv_Date_Window_geometry[1] //2
                PRO_Inv_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Invoice Date for Credit Memo.", max_width=PRO_Inv_Date_Window_geometry[0], max_height=PRO_Inv_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PRO_Inv_Date_Window, Name="Select Invoice Date for Credit Memo.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select Invoice Date of BEU Credit Memo.", GUI_Level_ID=3)
                Frame_Main.configure(bg_color = "#000001")
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Invoice Date",  Field_Type="Date_Picker", Validation="Date")  
                Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
                Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
                Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

                # Buttons
                PRO_Inv_Date_Variable = StringVar(master=PRO_Inv_Date_Window, value="", name="PRO_Inv_Date_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_iNV_Date_Date(Prompt_Date_Frame=Prompt_Date_Frame))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Generation Date for Confirmation.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_Inv_Date_Variable)
                PRO_Invoice_Date = PRO_Inv_Date_Variable.get()
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Credit_Memo_Header:Generation_Date")
        else:
            pass
        # Fill value in template
        PRO_Credit_Memos["invoice"]["invoice_header"]["control_info"]["generation_date"] = PRO_Invoice_Date
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_date"] = PRO_Invoice_Date
    else:
        pass

    # --------------------------------------------- Currency --------------------------------------------- #
    if Can_Continue == True:
        if Currency_Method == "Fixed":
            PRO_Currency = Fixed_Currency
        elif Currency_Method == "Purchase Order":
            PRO_Currency = Purchase_Ret_Headers_df_Filtered.iloc[0]["Currency_Code"]
        elif Currency_Method == "From Confirmation":
            PRO_Currency = PRO_Confirmed_Lines_df.iloc[0]["price_currency"]
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Currency Method selected: {Currency_Method} which is not supporter. Issue in Generate_Credit_Memo_Header:Currency", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Currency Method selected: {Currency_Method} which is not supporter. Issue in Generate_Credit_Memo_Header:Currency")
            Can_Continue = False

        # Fill value in template
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["price_currency"] = PRO_Currency
    else:
        pass

    # --------------------------------------------- Orders --------------------------------------------- #        
    if Can_Continue == True:
        PRO_Credit_Memos["invoice"]["invoice_header"]["order_history"]["order_id"] = Purchase_Return_Order
        PRO_Credit_Memos["invoice"]["invoice_header"]["order_history"]["supplier_order_id"] = PRO_Confirmation_Number
        PRO_Credit_Memos["invoice"]["invoice_header"]["order_history"]["order_date"] = PRO_Confirmed_Lines_df.iloc[0]["delivery_start_date"] # There was no other choice 
        PRO_Credit_Memos["invoice"]["invoice_header"]["order_history"]["delivery_note_id"] = PRO_Return_Shipment_Number
        PRO_Credit_Memos["invoice"]["invoice_header"]["order_history"]["delivery_note_date"] = PRO_Invoice_Date
    else:
        pass

    # --------------------------------------------- Order Date --------------------------------------------- #
    if Can_Continue == True:
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["delivery_date"]["delivery_start_date"] = PRO_Invoice_Date
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["delivery_date"]["delivery_end_date"] = PRO_Invoice_Date
    else:
        pass

    # --------------------------------------------- HQ Identification No --------------------------------------------- #
    if Can_Continue == True:
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
    else:
        pass

    # --------------------------------------------- Company Information --------------------------------------------- #
    if Can_Continue == True:
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["buyer_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PRO_Credit_Memos["invoice"]["invoice_header"]["invoice_info"]["invoice_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]
    else:
        pass

    return PRO_Credit_Memos, PRO_Credit_Number, PRO_Return_Shipment_Number