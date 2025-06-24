# Import Libraries
from pandas import DataFrame
from datetime import datetime
from fastapi import HTTPException

import Libs.Defaults_Lists as Defaults_Lists
import Libs.Pandas_Functions as Pandas_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, StringVar

def Generate_Exchange_Header_BHN(Settings: dict, Configuration: dict|None, window: CTk|None, PO_Invoices: dict, Invoice_Lines_df: DataFrame, GUI: bool=True):
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True

    Exchange_Rate_columns = ["Invoice_No", "Exchange_From", "Exchange_To", "Valid_From", "Rate"]
    Exchange_Rate_columns_df = DataFrame(columns=Exchange_Rate_columns)

    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    BHN_Exchange_Currency_From = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Currency"]["Currency_From"]
    BHN_Exchange_Currency_To = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Currency"]["Currency_To"]
    BHN_Exchange_Date_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Valid_Date"]["Method"]
    BHN_Exchange_Date_Fix_Date = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Valid_Date"]["Fixed_Options"]["Fix_Date"]

    BHN_Exchange_Exchange_Rate = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Local_Development"]["BHN"]["Exchange_Rate"]["Exchange_Rate"]


    # --------------------------------------------- Exchange Rate --------------------------------------------- #
    # Analyze lines
    Invoice_List = Invoice_Lines_df["Invoice_No"].to_list()
    Invoice_List = list(set(Invoice_List))
    Invoice_List.sort()

    Plant_List = []
    for Invoice in Invoice_List:
        Invoice_Plant = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Invoice_Lines_df, Search_Column="plant", Filter_Column="Invoice_No", Filter_Value=Invoice)
        Plant_List.append(Invoice_Plant)

    Used_Indexes = []
    for Plant_index, Plant_No in enumerate(Plant_List):
        if Plant_No == "1004":
            Used_Indexes.append(Plant_index)

    Selected_Invoices_list = []
    for Index in Used_Indexes:
        Selected_Invoices_list.append(Invoice_List[Index])

    Exchange_Rate_columns_df["Invoice_No"] = Selected_Invoices_list
    Exchange_Rate_columns_df["Exchange_From"] = BHN_Exchange_Currency_From
    Exchange_Rate_columns_df["Exchange_To"] = BHN_Exchange_Currency_To
    Exchange_Rate_columns_df["Rate"] = BHN_Exchange_Exchange_Rate

    # Apply Exchange Rate
    if Can_Continue == True:
        if BHN_Exchange_Date_Method == "Fixed":
            Exchange_Rate_columns_df["Valid_From"] = BHN_Exchange_Date_Fix_Date
        elif BHN_Exchange_Date_Method == "Today":
            Today_dt = datetime.now()
            Today_str = Today_dt.strftime(Date_Format)
            Exchange_Rate_columns_df["Valid_From"] = Today_str
        elif BHN_Exchange_Date_Method == "Prompt":
            if GUI == True:
                def Select_Exchange_Date(Frame_Body: CTkFrame, Lines_No: int):
                    PO_Exchange_Date_list = []
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
                            PO_Exchange_Date_list.append(Value_Date)

                    if Full_List == True:
                        PO_Exchange_Date_list_joined = ";".join(PO_Exchange_Date_list)
                        PO_EXCH_Date_Variable.set(value=PO_Exchange_Date_list_joined)
                        PO_EXCH_Date_Window.destroy()
                    else:
                        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Exchange Date", message=f"Fill exchange date for all Invoices which should have to have it as are from Plant = 1004.", icon="question", option_1="Confirm", fade_in_duration=1, GUI_Level_ID=1)

                # TopUp Window
                PO_EXCH_Date_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - PO_EXCH_Date_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - PO_EXCH_Date_Window_geometry[1] //2
                PO_EXCH_Date_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Set Exchange Date for Invoice/s.", max_width=PO_EXCH_Date_Window_geometry[0], max_height=PO_EXCH_Date_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_EXCH_Date_Window, Name="Set Exchange Date for Invoice/s.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To set Invoice Date based on Invoice Count.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Invoice Date Fields
                Lines_No = len(Selected_Invoices_list)
                for Invoice_Index, Invoice_Number in enumerate(Selected_Invoices_list):
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
                if content_height > PO_EXCH_Date_Window_geometry[1]:
                    content_height = PO_EXCH_Date_Window_geometry[1]
                else:
                    # Update height of TopUp when content is smaller than max_height
                    PO_EXCH_Date_Window.maxsize(width=PO_EXCH_Date_Window_geometry[0], height=content_height)
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                PO_EXCH_Date_Variable = StringVar(master=PO_EXCH_Date_Window, value="", name="PO_EXCH_Date_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_Exchange_Date(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm Exchange Date/s selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(PO_EXCH_Date_Variable)
                PO_Exchange_Date_list = PO_EXCH_Date_Variable.get().split(";")
                Exchange_Rate_columns_df["Valid_From"] = PO_Exchange_Date_list
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_Exchange_Header_BHN:Exchange_Rate.")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Exchange Date Method selected: {BHN_Exchange_Date_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Exchange Date Method selected: {BHN_Exchange_Date_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    print(Exchange_Rate_columns_df)

    # PO_Invoices Update -> only to those which has 
    for PO_Invoice_Key, PO_Invoice_Value in enumerate(PO_Invoices):
        Invoice_Number = PO_Invoice_Value["invoice"]["invoice_header"]["invoice_info"]["invoice_id"]

        if Invoice_Number in Selected_Invoices_list:
            # Load template
            Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="PO_Invoice_BHN")

            # Read data from DataFrame
            exchange_currency_from = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Exchange_Rate_columns_df, Search_Column="Exchange_From", Filter_Column="Invoice_No", Filter_Value=Invoice_Number)
            exchange_currency_to = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Exchange_Rate_columns_df, Search_Column="Exchange_To", Filter_Column="Invoice_No", Filter_Value=Invoice_Number)
            exchange_currency_valid_from = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Exchange_Rate_columns_df, Search_Column="Valid_From", Filter_Column="Invoice_No", Filter_Value=Invoice_Number)
            exchange_currency_rate = Pandas_Functions.DataFrame_Get_One_Value(Search_df=Exchange_Rate_columns_df, Search_Column="Rate", Filter_Column="Invoice_No", Filter_Value=Invoice_Number)

            # Update to template
            Current_line_json["from"] = exchange_currency_from
            Current_line_json["to"] = exchange_currency_to
            Current_line_json["valid_from"] = exchange_currency_valid_from
            Current_line_json["rate"] = exchange_currency_rate

            # Upload to correct PO_Invoices
            PO_Invoices[PO_Invoice_Key]["invoice"]["invoice_header"]["invoice_info"]["exchange_currency"] = Current_line_json

        else:
            pass

    return PO_Invoices