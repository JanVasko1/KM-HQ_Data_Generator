# Import Libraries
from pandas import DataFrame
from datetime import datetime
from fastapi import HTTPException

from customtkinter import CTk, CTkFrame, StringVar

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

def Generate_PRO_CON_Header(Settings: dict, Configuration: dict|None, window: CTk|None, Purchase_Return_Order: str, Purchase_Return_Order_index: str, Purchase_Return_Headers_df: DataFrame, Company_Information_df: DataFrame, HQ_Communication_Setup_df: DataFrame, HQ_Item_Transport_Register_df: DataFrame, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    PRO_Confirmation_Header = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PRO_Confirmation_Header")
    Date_format = Settings["0"]["General"]["Formats"]["Date"]
    Numbers_DateTime_format = Settings["0"]["General"]["Formats"]["Numbers_DateTime"]

    PRO_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Number"]["Method"]
    PRO_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Number"]["Automatic_Options"]["Prefix"]
    PRO_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Number"]["Fixed_Options"]["Number"]
    PRO_Confirmation_Number = ""

    PRO_Generation_Date_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Generation_Date"]["Method"]
    PRO_Gen_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Generation_Date"]["Fixed_Options"]["Fix_Date"]
    PRO_Generation_Date = ""

    PRO_Currency_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Currency"]["Method"]
    PRO_Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    PRO_Currency = ""

    # Filter Dataframes by Purchase Order
    mask_HQ_Item_Tr_Reg = HQ_Item_Transport_Register_df["Document_No"] == Purchase_Return_Order
    HQ_Item_Tr_Reg_Filtered = DataFrame(HQ_Item_Transport_Register_df[mask_HQ_Item_Tr_Reg])

    mask_Purchase_Return_Order = Purchase_Return_Headers_df["No"] == Purchase_Return_Order
    Purchase_Headers_df_Filtered = DataFrame(Purchase_Return_Headers_df[mask_Purchase_Return_Order])

    # --------------------------------------------- Confirmation Number --------------------------------------------- #
    if Can_Continue == True:
        if PRO_Numbers_Method == "Fixed":
            PRO_Confirmation_Number = PRO_Fixed_Number + Purchase_Return_Order_index
        elif PRO_Numbers_Method == "Automatic":
            Today_dt = datetime.now()
            Today_str = Today_dt.strftime(Numbers_DateTime_format)
            PRO_Confirmation_Number = PRO_Automatic_Prefix + Today_str + Purchase_Return_Order_index
        elif PRO_Numbers_Method == "Prompt":
            if GUI == True:
                def Select_PRO_CON_Number(Prompt_Number_Frame: CTkFrame):
                    PRO_CON_Number_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PRO_CON_Number = PRO_CON_Number_Var.get()
                    PRO_CON_Number = PRO_CON_Number + Purchase_Return_Order_index
                    PRO_CON_Number_Variable.set(value=PRO_CON_Number)
                    PRO_CON_Number_Window.destroy()
                    
                # TopUp Window
                PRO_CON_Number_Window_geometry = (500, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_CON_Number_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_CON_Number_Window_geometry[1] //2
                PRO_CON_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Purchase Return Order Confirmation Number.", max_width=PRO_CON_Number_Window_geometry[0], max_height=PRO_CON_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PRO_CON_Number_Window, Name="Select Purchase Return Order Confirmation Number.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select number of BEU Return Confirmation.", GUI_Level_ID=3)
                Frame_Main.configure(bg_color = "#000001")
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Prompt_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Confirmation Number",  Field_Type="Input_Normal")  
                Prompt_Number_Frame_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
                Prompt_Number_Frame_Var.configure(placeholder_text="Insert your Confirmation Number", placeholder_text_color="#949A9F")

                # Buttons
                PRO_CON_Number_Variable = StringVar(master=PRO_CON_Number_Window, value="", name="PRO_CON_Number_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_CON_Number(Prompt_Number_Frame=Prompt_Number_Frame))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm PRO Confirmation Number.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_CON_Number_Variable)
                PRO_Confirmation_Number = PRO_CON_Number_Variable.get()
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PRO_CON_Header:Confirmation_Number")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Confirmation Number Method selected: {PRO_Numbers_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Confirmation Number Method selected: {PRO_Numbers_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
        
        # Fill value in template
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["supplier_order_id"] = PRO_Confirmation_Number
    else:
        pass

    # --------------------------------------------- Generation Date --------------------------------------------- #
    if Can_Continue == True:
        if PRO_Generation_Date_Method == "Fixed":
            PRO_Generation_Date = PRO_Gen_Fix_Date
        elif PRO_Generation_Date_Method == "Today":
            Today_dt = datetime.now()
            PRO_Generation_Date = Today_dt.strftime(Date_format)
        elif PRO_Generation_Date_Method == "Prompt":
            if GUI == True:
                def Select_PRO_Gen_Date_Date(Prompt_Date_Frame: CTkFrame):
                    Generation_Date_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                    PRO_Gen_Date_Date = Generation_Date_Var.get()
                    PRO_Gen_Date_Date_Variable.set(value=PRO_Gen_Date_Date)
                    PRO_Gen_Date_Window.destroy()
                    
                # TopUp Window
                PRO_Gen_Date_Window_geometry = (500, 250)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PRO_Gen_Date_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PRO_Gen_Date_Window_geometry[1] //2
                PRO_Gen_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select Generation Date for Confirmation.", max_width=PRO_Gen_Date_Window_geometry[0], max_height=PRO_Gen_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PRO_Gen_Date_Window, Name="Select Generation Date for Confirmation.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select Generation Date of BEU Confirmation.", GUI_Level_ID=3)
                Frame_Main.configure(bg_color = "#000001")
                Frame_Body = Frame_Main.children["!ctkframe2"]

                Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Generation Date",  Field_Type="Date_Picker", Validation="Date")  
                Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
                Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
                Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

                # Buttons
                PRO_Gen_Date_Date_Variable = StringVar(master=PRO_Gen_Date_Window, value="", name="PRO_Gen_Date_Date_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PRO_Gen_Date_Date(Prompt_Date_Frame=Prompt_Date_Frame))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Generation Date for Confirmation.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PRO_Gen_Date_Date_Variable)
                PRO_Generation_Date = PRO_Gen_Date_Date_Variable.get()
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_PRO_CON_Header:Generation_Date")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Generation Date Method selected: {PRO_Generation_Date_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Generation Date Method selected: {PRO_Generation_Date_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False

        # Fill value in template
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["control_info"]["generation_date"] = PRO_Generation_Date
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["orderresponse_date"] = PRO_Generation_Date
    else:
        pass

    # --------------------------------------------- Currency --------------------------------------------- #
    if Can_Continue == True:
        if PRO_Currency_Method == "Fixed":
            PRO_Currency = PRO_Fixed_Currency
        elif PRO_Currency_Method == "Purchase Return Order":
            PRO_Currency = Purchase_Headers_df_Filtered.iloc[0]["Currency_Code"]
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Currency Method selected: {PRO_Currency_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Currency Method selected: {PRO_Currency_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False

        # Fill value in template
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["price_currency"] = PRO_Currency
    else:
        pass


    # --------------------------------------------- Order Date --------------------------------------------- #
    if Can_Continue == True:
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["order_date"] = HQ_Item_Tr_Reg_Filtered.iloc[0]["Order_Date"]
    else:
        pass

    # --------------------------------------------- Purchase Return Order --------------------------------------------- #        
    if Can_Continue == True:
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["order_id"] = Purchase_Return_Order
    else:
        pass

    # --------------------------------------------- HQ Identification No --------------------------------------------- #
    if Can_Continue == True:
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
    else:
        pass

    # --------------------------------------------- Company Information --------------------------------------------- #
    if Can_Continue == True:
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PRO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]
    else:
        pass

    return PRO_Confirmation_Header, PRO_Confirmation_Number