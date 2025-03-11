# Import Libraries
from pandas import DataFrame
from datetime import datetime

from customtkinter import CTk, CTkFrame, StringVar

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

def Generate_PO_CON_Header(Settings: dict, Configuration: dict, window: CTk, Purchase_Order: str, Purchase_Headers_df: DataFrame, Company_Information_df: DataFrame, HQ_Communication_Setup_df: DataFrame, HQ_Item_Transport_Register_df: DataFrame):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    PO_Confirmation_Header = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Confirmation_Header")
    Date_format = Settings["0"]["General"]["Formats"]["Date"]

    PO_Numbers_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Method"]
    PO_Automatic_Prefix = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Automatic_Options"]["Prefix"]
    PO_Fixed_Number = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Number"]["Fixed_Options"]["Number"]
    PO_Number = ""

    PO_Generation_Date_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Method"]
    PO_Gen_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Generation_Date"]["Fixed_Options"]["Fix_Date"]
    PO_Generation_Date = ""

    PO_Currency_Method = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Method"]
    PO_Fixed_Currency = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Currency"]["Fixed_Options"]["Fix_Currency"]
    PO_Currency = ""

    # Filter Dataframes by Purchase Order
    mask_HQ_Item_Tr_Reg = HQ_Item_Transport_Register_df["Document_No"] == Purchase_Order
    HQ_Item_Tr_Reg_Filtered = HQ_Item_Transport_Register_df[mask_HQ_Item_Tr_Reg]

    mask_Purchase_Header = Purchase_Headers_df["No"] == Purchase_Order
    Purchase_Headers_df_Filtered = Purchase_Headers_df[mask_Purchase_Header]

    # --------------------------------------------- Confirmation Number --------------------------------------------- #
    if Can_Continue == True:
        if PO_Numbers_Method == "Fixed":
            PO_Number = PO_Fixed_Number
        elif PO_Numbers_Method == "Automatic":
            Today_dt = datetime.now()
            Today_str = Today_dt.strftime("%Y%m%d%H%M%S")
            PO_Number = PO_Automatic_Prefix + Today_str
        elif PO_Numbers_Method == "Prompt":
            def Select_PO_CON_Number(Prompt_Number_Frame: CTkFrame):
                PO_CON_Number_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
                PO_CON_Number = PO_CON_Number_Var.get()
                PO_CON_Number_Variable.set(value=PO_CON_Number)
                PO_CON_Number_Window.destroy()
                
            # TopUp Window
            PO_CON_Number_Window_geometry = (300, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_CON_Number_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_CON_Number_Window_geometry[1] //2
            PO_CON_Number_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Select Purchase Order Confirmation Number.", width=PO_CON_Number_Window_geometry[0], height=PO_CON_Number_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_CON_Number_Window, Name="Select Purchase Order Confirmation Number.", Additional_Text="", Widget_size="Half_size", Widget_Label_Tooltip="To select number of BEU Confirmation.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            Prompt_Number_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Confirmation Number",  Field_Type="Input_Normal")  
            Prompt_Number_Frame_Var = Prompt_Number_Frame.children["!ctkframe3"].children["!ctkentry"]
            Prompt_Number_Frame_Var.configure(placeholder_text="Insert your Confirmation Number", placeholder_text_color="#949A9F")

            # Buttons
            PO_CON_Number_Variable = StringVar(master=PO_CON_Number_Window, value="", name="PO_CON_Number_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_CON_Number(Prompt_Number_Frame=Prompt_Number_Frame))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm PO Confirmation Number.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_CON_Number_Variable)
            PO_Number = PO_CON_Number_Variable.get()
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Confirmation Number Method selected: {PO_Numbers_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False
        
        # Fill value in template
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["supplier_order_id"] = PO_Number
    else:
        pass

    # --------------------------------------------- Generation Date --------------------------------------------- #
    if Can_Continue == True:
        if PO_Generation_Date_Method == "Fixed":
            PO_Generation_Date = PO_Gen_Fix_Date
        elif PO_Generation_Date_Method == "Today":
            Today_dt = datetime.now()
            PO_Generation_Date = Today_dt.strftime(Date_format)
        elif PO_Generation_Date_Method == "Prompt":
            def Select_PO_Gen_Date_Date(Prompt_Date_Frame: CTkFrame):
                Generation_Date_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
                PO_Gen_Date_Date = Generation_Date_Var.get()
                PO_Gen_Date_Date_Variable.set(value=PO_Gen_Date_Date)
                PO_Gen_Date_Window.destroy()
                
            # TopUp Window
            PO_Gen_Date_Window_geometry = (300, 250)
            Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
            Main_Window_Centre[0] = Main_Window_Centre[0] - PO_Gen_Date_Window_geometry[0] //2
            Main_Window_Centre[1] = Main_Window_Centre[1] - PO_Gen_Date_Window_geometry[1] //2
            PO_Gen_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Select Generation Date for Confirmation.", width=PO_Gen_Date_Window_geometry[0], height=PO_Gen_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=False, Always_on_Top=True)

            # Frame - General
            Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_Gen_Date_Window, Name="Select Generation Date for Confirmation.", Additional_Text="", Widget_size="Half_size", Widget_Label_Tooltip="To select GEneration Date of BEU Confirmation.", GUI_Level_ID=3)
            Frame_Main.configure(bg_color = "#000001")
            Frame_Body = Frame_Main.children["!ctkframe2"]

            Prompt_Date_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Generation Date",  Field_Type="Entry_DropDown")  
            Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkentry"]
            Button_Prompt_Date_Frame_Var = Prompt_Date_Frame.children["!ctkframe3"].children["!ctkbutton"]
            Prompt_Date_Frame_Var.configure(placeholder_text="YYYY-MM-DD", placeholder_text_color="#949A9F")
            Button_Prompt_Date_Frame_Var.configure(command = lambda: Elements_Groups.My_Date_Picker(Settings=Settings, Configuration=Configuration, date_entry=Prompt_Date_Frame_Var, Clicked_on_Button=Button_Prompt_Date_Frame_Var, width=200, height=230, Fixed=True, GUI_Level_ID=3))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Prompt_Date_Frame_Var, message="Entry DropDown", ToolTip_Size="Normal", GUI_Level_ID=3)

            # Buttons
            PO_Gen_Date_Date_Variable = StringVar(master=PO_Gen_Date_Window, value="", name="PO_Gen_Date_Date_Variable")
            Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
            Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_PO_Gen_Date_Date(Prompt_Date_Frame=Prompt_Date_Frame))
            Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Generation Date for Confirmation.", ToolTip_Size="Normal", GUI_Level_ID=3)   
            Button_Confirm_Var.wait_variable(PO_Gen_Date_Date_Variable)
            PO_Generation_Date = PO_Gen_Date_Date_Variable.get()
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Generation Date Method selected: {PO_Generation_Date_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Fill value in template
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["control_info"]["generation_date"] = PO_Generation_Date
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["orderresponse_date"] = PO_Generation_Date
    else:
        pass

    # --------------------------------------------- Currency --------------------------------------------- #
    if Can_Continue == True:
        if PO_Currency_Method == "Fixed":
            PO_Currency = PO_Fixed_Currency
        elif PO_Currency_Method == "Purchase Order":
            PO_Currency = Purchase_Headers_df_Filtered.iloc[0]["Currency_Code"]
        else:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message=f"Currency Method selected: {PO_Currency_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            Can_Continue = False

        # Fill value in template
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["price_currency"] = PO_Currency
    else:
        pass


    # --------------------------------------------- Order Date --------------------------------------------- #
    if Can_Continue == True:
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["order_date"] = HQ_Item_Tr_Reg_Filtered.iloc[0]["Order_Date"]
    else:
        pass

    # --------------------------------------------- Purchase Order--------------------------------------------- #        
    if Can_Continue == True:
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["order_id"] = Purchase_Order
    else:
        pass

    # --------------------------------------------- HQ Identification No --------------------------------------------- #
    if Can_Continue == True:
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["party_id"] = HQ_Communication_Setup_df.iloc[0]["HQ_Identification_No"]
    else:
        pass

    # --------------------------------------------- Company Information --------------------------------------------- #
    if Can_Continue == True:
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["buyer_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["invoice_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]

        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["name"] = Company_Information_df.iloc[0]["English_Name_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["street"] = Company_Information_df.iloc[0]["English_Address_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["zip"] = Company_Information_df.iloc[0]["English_Post_Code_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["city"] = Company_Information_df.iloc[0]["English_City_NUS"]
        PO_Confirmation_Header["orderresponse"]["orderresponse_header"]["orderresponse_info"]["delivery_party"]["party"]["address"]["country"] = Company_Information_df.iloc[0]["English_Country_Reg_Code_NUS"]
    else:
        pass

    return PO_Confirmation_Header