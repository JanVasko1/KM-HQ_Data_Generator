# Import Libraries
import threading

from customtkinter import CTk, CTkFrame, CTkButton, CTkScrollableFrame, StringVar, BooleanVar

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Downloader.Downloader as Downloader
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

def Page_Download(Settings: dict, Configuration: dict, window: CTk, Documents: dict, Frame: CTkFrame):
    NUS_Version_List = list(Settings["0"]["Connection"]["NUS_Version_List"])
    Environment_List = list(Settings["0"]["Connection"]["Environment_List"])
    try:
        Environment_List.remove("PRD")
    except:
        pass
    NOC_List = list(Settings["0"]["Connection"]["NOC_List"])
    Companies_List = []
    Log_Process_List = []
    Vendor_Lists = []

    NUS_Version_Variable = StringVar(master=Frame, value="Cloud", name="NUS_Version_Variable")
    Environment_Variable = StringVar(master=Frame, value="QA", name="Environment_Variable")
    NOC_Variable = StringVar(master=Frame, value="Core", name="NOC_Variable")
    Company_Variable = StringVar(master=Frame, value="-", name="Company_Variable")
    Logistic_Process_Variable = StringVar(master=Frame, value="-", name="Logistic_Process_Variable")

    # ------------------------- Local Functions ------------------------#
    def Download_Companies(Companies_Frame_Var: CTkScrollableDropdown) -> None:
        Companies_thread = threading.Thread(target=Downloader.Get_Companies_List, args=(Configuration, window, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Companies_Frame_Var))
        Companies_thread.start()
        Companies_thread.join(timeout=0.1) 

    def Get_Logistic_Process(PO_MUL_LOG_PROC_Frame: CTkFrame, BB_Vendor_Used_Frame: CTkFrame, Selected_Company: str) -> list:
        # Delete Operational data from Settings to clear lists
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Used"], Information="")
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Logistic_Process", "Process_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Used"], Information="")
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["BackBone_Billing", "Vendors_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Order", "Purchase_Order_List"], Information=[])
        Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=[])

        Company_Variable.set(value=Selected_Company)       
        NUS_Version = NUS_Version_Variable.get()
        NOC = NOC_Variable.get()
        Environment = Environment_Variable.get()

        # Logistic Process
        Log_Proc_thread = threading.Thread(target=Downloader.Get_Logistic_Process_List, args=(Configuration, window, Documents, NUS_Version, NOC, Environment, Selected_Company, Log_Proc_Used_Variable, PO_MUL_LOG_PROC_Frame))
        Log_Proc_thread.start()
        Log_Proc_thread.join(timeout=0.1) 

        # Vendor List
        Vendors_thread = threading.Thread(target=Downloader.Get_HQ_Vendors_List, args=(Configuration, window, Documents, NUS_Version, NOC, Environment, Selected_Company, BB_Vendor_Used_Variable, BB_Vendor_Used_Frame))
        Vendors_thread.start()
        Vendors_thread.join(timeout=0.1) 
        
    def Generate_Purchase_Orders() -> None:
        Purchase_Order_list = Documents["Purchase_Order"]["Purchase_Order_List"]
        if len(Purchase_Order_list) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no Purchase Order selected, you have to put one or select multiple to Download and Process.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Generate_PO_thread = threading.Thread(target=Downloader.Download_Data_Purchase_Orders, args=(Settings, Configuration, window, Progress_Bar, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Company_Variable.get(), Purchase_Order_list))
            Generate_PO_thread.start()
            Generate_PO_thread.join(timeout=0.1) 

    def Start_Order_Show_Thread(Button: CTkButton, PO_MUL_LOG_PROC_Frame_Var: CTkScrollableDropdown|None, Document_Type: str) -> None:
        Show_PO_List_thread = threading.Thread(target=Purchase_Orders_Show, args=(Button, PO_MUL_LOG_PROC_Frame_Var, Document_Type))
        Show_PO_List_thread.start()
        Show_PO_List_thread.join(timeout=0.1) 

    def Purchase_Orders_Show(Button: CTkButton, PO_MUL_LOG_PROC_Frame_Var: CTkScrollableDropdown|None, Document_Type: str) -> None:
        def Confirm_Choice(PO_Select_Scrollable_Body: CTkScrollableFrame) -> None:
            Selected_POs_List = []
            def Find_if_Marked(PO_Frame_row: CTkFrame, Selected_POs_List: list) -> list:
                # check if marked 
                Marked_Value = PO_Frame_row.children["!ctkframe3"].children["!ctkcheckbox"].get()

                if Marked_Value == True:
                    Purchase_Label = PO_Frame_row.children["!ctkframe"].children["!ctklabel"]
                    Purchase_Order = str(Purchase_Label.cget("text"))
                    Purchase_Order = Purchase_Order.replace(":", "")
                    Selected_POs_List.append(Purchase_Order)
                else:
                    pass

                return Selected_POs_List

            Column_A_Children = PO_Select_Scrollable_Body.children["!ctkframe"]
            Column_B_Children = PO_Select_Scrollable_Body.children["!ctkframe2"]
            Column_C_Children = PO_Select_Scrollable_Body.children["!ctkframe3"]

            # Column A
            Frame_A_len = len(Column_A_Children.children)
            for Counter in range(0, Frame_A_len - 1):
                if Counter == 0:
                    frame = ""
                elif Counter > 0:
                    frame = str(Counter + 1)
                else:
                    pass
                
                Selected_POs_List = Find_if_Marked(PO_Frame_row=Column_A_Children.children[f"!ctkframe{frame}"] ,Selected_POs_List=Selected_POs_List)
                
            # Column B
            Frame_B_len = len(Column_B_Children.children)
            for Counter in range(0, Frame_B_len - 1):
                if Counter == 0:
                    frame = ""
                elif Counter > 0:
                    frame = str(Counter + 1)
                else:
                    pass
                
                Selected_POs_List = Find_if_Marked(PO_Frame_row=Column_B_Children.children[f"!ctkframe{frame}"] ,Selected_POs_List=Selected_POs_List)

            # Column C
            Frame_C_len = len(Column_C_Children.children)
            for Counter in range(0, Frame_C_len - 1):
                if Counter == 0:
                    frame = ""
                elif Counter > 0:
                    frame = str(Counter + 1)
                else:
                    pass
                
                Selected_POs_List = Find_if_Marked(PO_Frame_row=Column_C_Children.children[f"!ctkframe{frame}"] ,Selected_POs_List=Selected_POs_List)
                
            # Save Purchase Orders to Documents.json
            Selected_POs_List.sort()
            Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Order", "Purchase_Order_List"], Information=Selected_POs_List)
            PO_Select_window.destroy()

        def Reject_Choice() -> None:
            Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Order", "Purchase_Order_List"], Information=[])
            PO_Select_window.destroy()


        Logistic_Process_Variable.set(value=PO_MUL_LOG_PROC_Frame_Var.get())

        Selected_Company = Company_Variable.get()
        Selected_Company = Selected_Company.replace(" ", "%20")

        Purchase_Orders_List = []
        Purchase_Orders_List = Downloader.Get_Orders_List(Configuration=Configuration, window=window, NUS_version=NUS_Version_Variable.get(), NOC=NOC_Variable.get(), Environment=Environment_Variable.get(), Company=Selected_Company, Document_Type=Document_Type, Logistic_Process_Filter=PO_MUL_LOG_PROC_Frame_Var.get())

        if len(Purchase_Orders_List) == 0:
            pass
        else:
            PO_Select_window_geometry = (1020, 400)
            Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button, New_Window_width=PO_Select_window_geometry[0])
            PO_Select_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Recalculate", max_width=PO_Select_window_geometry[0], max_height=PO_Select_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)

            # Frame - General
            PO_Select_Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PO_Select_window, Name="Multiple Purchase Order Select", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Helps to select more Purchase Orders.", GUI_Level_ID=3)
            PO_Select_Frame_Body = PO_Select_Frame_Main.children["!ctkframe2"]

            PO_Select_Scrollable_Body = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PO_Select_Frame_Body, Frame_Size="PO_List", GUI_Level_ID=4)

            # Input Field + button in one line
            PO_Select_Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=PO_Select_Scrollable_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=4)
            PO_Select_Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=PO_Select_Scrollable_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=4)
            PO_Select_Frame_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=PO_Select_Scrollable_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=4)

            Counter = 0
            POs_Columns_Frame_List = [PO_Select_Frame_Column_A, PO_Select_Frame_Column_B, PO_Select_Frame_Column_C]
            for Purchase_Order in Purchase_Orders_List:
                # Field - Monday
                PO_Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=POs_Columns_Frame_List[Counter], Field_Frame_Type="Half_size" , Label=f"{Purchase_Order}",  Field_Type="Input_CheckBox")  
                PO_Fields_Frame_Var = PO_Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                PO_Fields_Frame_Var.configure(text="")
                
                Counter += 1
                if Counter == 3:
                    Counter = 0

            # Dynamic PopUp Content height
            content_row_count = len(PO_Select_Frame_Body.winfo_children())
            content_height = content_row_count * 35 + 30    # Lines multiplied + button
            if content_height > PO_Select_window_geometry[1]:
                content_height = PO_Select_window_geometry[1]
            PO_Select_Frame_Main.configure(bg_color = "#000001", height=content_height)

            # Buttons
            PO_Select_Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=PO_Select_Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
            PO_Select_Button_Confirm_Var = PO_Select_Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            PO_Select_Button_Confirm_Var.configure(text="Confirm", command = lambda: Confirm_Choice(PO_Select_Scrollable_Body=PO_Select_Scrollable_Body))
            Elements.Get_ToolTip(Configuration=Configuration, widget=PO_Select_Button_Confirm_Var, message="Confirm Purchases Order selection.", ToolTip_Size="Normal", GUI_Level_ID=4)

            PO_Reject_Button_Confirm_Var = PO_Select_Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
            PO_Reject_Button_Confirm_Var.configure(text="Reject", command = lambda: Reject_Choice())
            Elements.Get_ToolTip(Configuration=Configuration, widget=PO_Reject_Button_Confirm_Var, message="Reject Purchases Order selection.", ToolTip_Size="Normal", GUI_Level_ID=4)

            PO_Select_Scrollable_Body.pack(side="top", fill="both", expand=False, padx=10, pady=10)
            PO_Select_Frame_Column_A.pack(side="left", fill="none", expand=False, padx=5, pady=5)
            PO_Select_Frame_Column_B.pack(side="left", fill="none", expand=False, padx=5, pady=5)
            PO_Select_Frame_Column_C.pack(side="left", fill="none", expand=False, padx=5, pady=5)

        
    def Generate_BackBone_Billing() -> None:
        Buy_from_Vendor_No = Documents["BackBone_Billing"]["Used"]
        if len(Buy_from_Vendor_No) == "":
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no BEU Vendor selected, you have to select one before Download and Process.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Generate_BB_Invoice_thread = threading.Thread(target=Downloader.Download_Data_BackBoneBilling, args=(Settings, Configuration, window, Progress_Bar, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Company_Variable.get(), Buy_from_Vendor_No))
            Generate_BB_Invoice_thread.start()
            Generate_BB_Invoice_thread.join(timeout=0.1) 

    def Start_Order_Return_Show_Thread(Button: CTkButton, Document_Type: str) -> None:
        Show_PRO_List_thread = threading.Thread(target=Purchase_Return_Orders_Show, args=(Button, Document_Type))
        Show_PRO_List_thread.start()
        Show_PRO_List_thread.join(timeout=0.1) 

    def Purchase_Return_Orders_Show(Button: CTkButton, Document_Type: str) -> None:
        def Confirm_Choice(PRO_Select_Scrollable_Body: CTkScrollableFrame) -> None:
            Selected_PROs_List = []
            def Find_if_Marked(PRO_Frame_row: CTkFrame, Selected_PROs_List: list) -> list:
                # check if marked 
                Marked_Value = PRO_Frame_row.children["!ctkframe3"].children["!ctkcheckbox"].get()
                if Marked_Value == True:
                    Purchase_Ret_Label = PRO_Frame_row.children["!ctkframe"].children["!ctklabel"]
                    Purchase_Ret_Order = str(Purchase_Ret_Label.cget("text"))
                    Purchase_Ret_Order = Purchase_Ret_Order.replace(":", "")
                    Selected_PROs_List.append(Purchase_Ret_Order)
                else:
                    pass
                return Selected_PROs_List

            Column_PRO_A_Children = PRO_Select_Scrollable_Body.children["!ctkframe"]
            Column_PRO_B_Children = PRO_Select_Scrollable_Body.children["!ctkframe2"]
            Column_PRO_C_Children = PRO_Select_Scrollable_Body.children["!ctkframe3"]

            # Column A
            Frame_PRO_A_len = len(Column_PRO_A_Children.children)
            for Counter in range(0, Frame_PRO_A_len - 1):
                if Counter == 0:
                    frame = ""
                elif Counter > 0:
                    frame = str(Counter + 1)
                else:
                    pass
                
                Selected_PROs_List = Find_if_Marked(PRO_Frame_row=Column_PRO_A_Children.children[f"!ctkframe{frame}"] ,Selected_PROs_List=Selected_PROs_List)
                
            # Column B
            Frame_PRO_B_len = len(Column_PRO_B_Children.children)
            for Counter in range(0, Frame_PRO_B_len - 1):
                if Counter == 0:
                    frame = ""
                elif Counter > 0:
                    frame = str(Counter + 1)
                else:
                    pass
                
                Selected_PROs_List = Find_if_Marked(PRO_Frame_row=Column_PRO_B_Children.children[f"!ctkframe{frame}"] ,Selected_PROs_List=Selected_PROs_List)

            # Column C
            Frame_PRO_C_len = len(Column_PRO_C_Children.children)
            for Counter in range(0, Frame_PRO_C_len - 1):
                if Counter == 0:
                    frame = ""
                elif Counter > 0:
                    frame = str(Counter + 1)
                else:
                    pass
                
                Selected_PROs_List = Find_if_Marked(PRO_Frame_row=Column_PRO_C_Children.children[f"!ctkframe{frame}"] ,Selected_PROs_List=Selected_PROs_List)
                
            # Save Purchase Orders to Documents.json
            Selected_PROs_List.sort()
            Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=Selected_PROs_List)
            PRO_Select_window.destroy()

        def Reject_Choice() -> None:
            Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=[])
            PRO_Select_window.destroy()

        Selected_Company = Company_Variable.get()
        Selected_Company = Selected_Company.replace(" ", "%20")

        Purchase_Return_Orders_List = []
        Purchase_Return_Orders_List = Downloader.Get_Orders_List(Configuration=Configuration, window=window, NUS_version=NUS_Version_Variable.get(), NOC=NOC_Variable.get(), Environment=Environment_Variable.get(), Company=Selected_Company, Document_Type=Document_Type, Logistic_Process_Filter="")

        if len(Purchase_Return_Orders_List) == 0:
            pass
        else:
            PRO_Select_window_geometry = (500, 0)
            Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button, New_Window_width=PRO_Select_window_geometry[0])
            PRO_Select_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Recalculate", max_width=PRO_Select_window_geometry[0], max_height=PRO_Select_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)

            # Frame - General
            PRO_Select_Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=PRO_Select_window, Name="Multiple Purchase Return Order Select", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Helps to select more Purchase Return Orders.", GUI_Level_ID=3)
            PRO_Select_Frame_Body = PRO_Select_Frame_Main.children["!ctkframe2"]

            PRO_Select_Scrollable_Body = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=PRO_Select_Frame_Body, Frame_Size="PRO_List", GUI_Level_ID=4)

            # Input Field + button in one line
            PRO_Select_Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=PRO_Select_Scrollable_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=4)
            PRO_Select_Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=PRO_Select_Scrollable_Body, Frame_Size="Work_Area_Columns", GUI_Level_ID=4)

            Counter = 0
            PROs_Columns_Frame_List = [PRO_Select_Frame_Column_A, PRO_Select_Frame_Column_B]
            for Purchase_Ret_Order in Purchase_Return_Orders_List:
                # Field - Monday
                PRO_Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=PROs_Columns_Frame_List[Counter], Field_Frame_Type="Half_size" , Label=f"{Purchase_Ret_Order}",  Field_Type="Input_CheckBox")  
                PRO_Fields_Frame_Var = PRO_Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                PRO_Fields_Frame_Var.configure(text="")
                
                Counter += 1
                if Counter == 2:
                    Counter = 0

            # Dynamic PopUp Content height
            content_row_count = len(PRO_Select_Frame_Body.winfo_children())
            content_height = content_row_count * 35 + 30    # Lines multiplied + button
            if content_height > PRO_Select_window_geometry[1]:
                content_height = PRO_Select_window_geometry[1]
            PRO_Select_Frame_Main.configure(bg_color = "#000001", height=content_height)

            # Buttons
            PRO_Select_Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=PRO_Select_Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Small") 
            PRO_Select_Button_Confirm_Var = PRO_Select_Button_Frame.children["!ctkframe"].children["!ctkbutton"]
            PRO_Select_Button_Confirm_Var.configure(text="Confirm", command = lambda: Confirm_Choice(PRO_Select_Scrollable_Body=PRO_Select_Scrollable_Body))
            Elements.Get_ToolTip(Configuration=Configuration, widget=PRO_Select_Button_Confirm_Var, message="Confirm Purchases Return Order selection.", ToolTip_Size="Normal", GUI_Level_ID=4)

            PRO_Reject_Button_Confirm_Var = PRO_Select_Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
            PRO_Reject_Button_Confirm_Var.configure(text="Reject", command = lambda: Reject_Choice())
            Elements.Get_ToolTip(Configuration=Configuration, widget=PRO_Reject_Button_Confirm_Var, message="Reject Purchases Return Order selection.", ToolTip_Size="Normal", GUI_Level_ID=4)

            PRO_Select_Scrollable_Body.pack(side="top", fill="both", expand=False, padx=10, pady=10)
            PRO_Select_Frame_Column_A.pack(side="left", fill="x", expand=False, padx=5, pady=5)
            PRO_Select_Frame_Column_B.pack(side="left", fill="x", expand=False, padx=5, pady=5)

    def Generate_Purchase_Return_Orders() -> None:
        Purchase_Return_Orders_List = Documents["Purchase_Return_Order"]["Purchase_Return_Order_List"]
        if len(Purchase_Return_Orders_List) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no Purchase Order selected, you have to put one or select multiple to Download and Process.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Generate_PRO_thread = threading.Thread(target=Downloader.Download_Data_Return_Order, args=(Settings, Configuration, window, Progress_Bar, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Company_Variable.get(), Purchase_Return_Orders_List))
            Generate_PRO_thread.start()
            Generate_PRO_thread.join(timeout=0.1) 

    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line", GUI_Level_ID=1)
    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail", GUI_Level_ID=1)

    # ------------------------- State Area -------------------------#
    # NUS Version
    NUS_Version_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    NUS_Version_Text.configure(text="NUS Version: ")

    NUS_Version_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    NUS_Version_Frame.configure(width=140)
    NUS_Version_Frame.configure(variable=NUS_Version_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=NUS_Version_Frame, values=NUS_Version_List, command=None, GUI_Level_ID=1)

    # Environment
    Environment_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Environment_Text.configure(text="Environment: ")

    Environment_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    Environment_Frame.configure(width=140)
    Environment_Frame.configure(variable=Environment_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Environment_Frame, values=Environment_List, command=None, GUI_Level_ID=1)

    # NOCs
    NOC_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    NOC_Text.configure(text="NOC: ")

    NOC_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    NOC_Frame.configure(width=140)
    NOC_Frame.configure(variable=NOC_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=NOC_Frame, values=NOC_List, command=None, GUI_Level_ID=1)

    # Button - Download Company
    Button_Download_Company = Elements.Get_Button_Text(Configuration=Configuration, Frame=Frame_Download_State_Area, Button_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download_Company, message="Download Companies list based on selected NUS Version, Environment and NOC.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # Companies List
    Companies_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Companies_Text.configure(text="Companies: ")

    Companies_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    Companies_Frame.configure(width=200)
    Companies_Frame.configure(variable=Company_Variable)
    
    # ------------------------- Work Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, orientation="Horizontal", Progress_Size="Download_Process", GUI_Level_ID=1)
    Progress_Bar.set(value=0)

    Frame_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # ---------------- Purchase Order Tab ---------------- #
    Generate_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Use"]
    Generate_CPDI = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Use"]
    Generate_PreAdvice = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Use"]
    Generate_Delivery = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Use"]
    Generate_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Use"]
    Generate_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["PDF"]["Generate"]

    Generate_CON_Variable = BooleanVar(master=Frame, value=Generate_Confirmation, name="Generate_CON_Variable")
    Generate_CPD_Variable = BooleanVar(master=Frame, value=Generate_CPDI, name="Generate_CPD_Variable")
    Generate_PRA_Variable = BooleanVar(master=Frame, value=Generate_PreAdvice, name="Generate_PRA_Variable")
    Generate_DEL_Variable = BooleanVar(master=Frame, value=Generate_Delivery, name="Generate_DEL_Variable")
    Generate_INV_Variable = BooleanVar(master=Frame, value=Generate_Invoice, name="Generate_INV_Variable")
    Generate_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_Invoice_PDF, name="Generate_INV_PDF_Variable")

    # Tab View - Purchase Order
    TabView_PO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Column_A, Tab_size="Download", GUI_Level_ID=2)
    TabView_PO.pack_propagate(flag=False)
    Tab_PO = TabView_PO.add("Purchase Order")
    TabView_PO.set("Purchase Order")
    Tab_PO_ToolTip_But = TabView_PO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Purchase Order .json generator.", ToolTip_Size="Normal", GUI_Level_ID=2)
    
    # Field - Use Confirmation
    Generate_Conf_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Confirmation",  Field_Type="Input_CheckBox")  
    Generate_Conf_Frame_Var = Generate_Conf_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_Conf_Frame_Var.configure(variable=Generate_CON_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_CON_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Use"], Information=Generate_CON_Variable))

    # Field - Use CPDI
    Generate_CPDI_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="CPDI",  Field_Type="Input_CheckBox", Field_ToolTip=["Generate only when Purchase Order is marked PDI Center = BEU", 3])  
    Generate_CPDI_Frame_Var = Generate_CPDI_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_CPDI_Frame_Var.configure(variable=Generate_CPD_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_CPD_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Use"], Information=Generate_CPD_Variable))

    # Field - Use PreAdvice
    Generate_PREA_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="PreAdvice",  Field_Type="Input_CheckBox")  
    Generate_PREA_Frame_Var = Generate_PREA_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PREA_Frame_Var.configure(variable=Generate_PRA_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_PRA_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Use"], Information=Generate_PRA_Variable))

    # Field - Use Delivery
    Generate_DEL_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Delivery",  Field_Type="Input_CheckBox")  
    Generate_DEL_Frame_Var = Generate_DEL_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_DEL_Frame_Var.configure(variable=Generate_DEL_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_DEL_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Use"], Information=Generate_DEL_Variable))

    # Field - Use Invoice
    Generate_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Invoice",  Field_Type="Input_CheckBox")  
    Generate_INV_Frame_Var = Generate_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_INV_Frame_Var.configure(variable=Generate_INV_Variable, text="")

    if Generate_INV_Variable.get() == True:
        pass
    elif Generate_INV_Variable.get() == False:
        Generate_INV_PDF_Variable.set(value=False)
    else:
        pass

    # Field - Use Invoice PDF
    Generate_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Invoice PDF",  Field_Type="Input_CheckBox")  
    Generate_INV_PDF_Frame_Var = Generate_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_INV_PDF_Frame_Var.configure(variable=Generate_INV_PDF_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "PDF", "Generate"], Information=Generate_INV_PDF_Variable))

    if Generate_INV_Variable.get() == True:
        Generate_INV_PDF_Frame_Var.configure(state="normal")
    elif Generate_INV_Variable.get() == False:
        Generate_INV_PDF_Frame_Var.configure(state="disabled")
    else:
        pass

    PO_Block_Variable_list = [Generate_INV_PDF_Variable]
    PO_Block_Field_list = [Generate_INV_PDF_Frame_Var]
    PO_Block_JSON_path_list =[["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "PDF", "Generate"]]
    Generate_INV_Frame_Var.configure(command = lambda: CustomTkinter_Functions.Field_Block_Bool(Settings=Settings, window=window, Selected_Variable=Generate_INV_Variable, Selected_Field=Generate_INV_Frame_Var, Selected_JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Use"], Block_Variable_list=PO_Block_Variable_list, Block_Field_list=PO_Block_Field_list, Block_JSON_path_list=PO_Block_JSON_path_list))
    
    # -------- Select One -------- #
    TabView_One_PO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Tab_PO, Tab_size="Download", GUI_Level_ID=3)
    TabView_One_PO.pack_propagate(flag=False)
    Tab_One_PO = TabView_One_PO.add("One Purchase Order")
    TabView_One_PO.set("One Purchase Order")
    Tab_One_PO_ToolTip_But = TabView_One_PO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_One_PO_ToolTip_But, message="Use to generate file only for one inserted Order.", ToolTip_Size="Normal", GUI_Level_ID=3)
    
    # Selected Purchase Orders List
    PO_Selected_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_One_PO, Field_Frame_Type="Half_size" , Label="Purchase Order", Field_Type="Input_Normal")  
    PO_Selected_Frame_Var = PO_Selected_Frame.children["!ctkframe3"].children["!ctkentry"]
    PO_Selected_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Order", "Purchase_Order_List"], Information=[str(PO_Selected_Frame_Var.get()).replace(" ", "")]))
    PO_Selected_Frame_Var.configure(placeholder_text="Purchase Order Number", placeholder_text_color="#949A9F")

    # Buttons - Generate
    Button_PO_One_Generate_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_One_PO, Button_Size="Normal")
    Button_PO_One_Generate_Var.configure(text="Generate", command = lambda: Generate_Purchase_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_One_Generate_Var, message="Generate selected documents for one Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # -------- Select Multiple -------- #
    TabView_Multi_PO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Tab_PO, Tab_size="Download", GUI_Level_ID=3)
    TabView_Multi_PO.pack_propagate(flag=False)
    Tab_Multi_PO = TabView_Multi_PO.add("Multi POs")
    TabView_Multi_PO.set("Multi POs")
    Tab_Multi_PO_ToolTip_But = TabView_Multi_PO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Multi_PO_ToolTip_But, message="Select More Purchase Orders from list, which can be pre-filtered by Logistic Process.", ToolTip_Size="Normal", GUI_Level_ID=3)

    Log_Proc_Used = Documents["Logistic_Process"]["Used"]
    Log_Proc_Used_Variable = StringVar(master=Frame, value=Log_Proc_Used, name="Log_Proc_Used_Variable")

    # Field - Logistic Process Filter
    PO_MUL_LOG_PROC_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_Multi_PO, Field_Frame_Type="Half_size" , Label="Log. Process", Field_Type="Input_OptionMenu")  
    PO_MUL_LOG_PROC_Frame_Var = PO_MUL_LOG_PROC_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    PO_MUL_LOG_PROC_Frame_Var.configure(variable=Log_Proc_Used_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=PO_MUL_LOG_PROC_Frame_Var, values=Log_Process_List, command=lambda Selected_Value: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=Log_Proc_Used_Variable, File_Name="Documents", JSON_path=["Logistic_Process", "Used"], Information=Selected_Value), GUI_Level_ID=3)

    # Buttons
    Button_PO_Show_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_Multi_PO, Button_Size="Normal")
    Button_PO_Show_Var.configure(text="List", command = lambda: Start_Order_Show_Thread(Button=Button_PO_Show_Var, PO_MUL_LOG_PROC_Frame_Var=PO_MUL_LOG_PROC_Frame_Var, Document_Type="Order"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_Show_Var, message="Show Listbox with all available Purchase Orders for selection.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # Buttons - Generate
    Button_PO_Multi_Generate_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_Multi_PO, Button_Size="Normal")
    Button_PO_Multi_Generate_Var.configure(text="Generate", command = lambda: Generate_Purchase_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_Multi_Generate_Var, message="Process selected files for filtered Purchase Orders.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # ---------------- BackBone Billing Tab -------- #
    Generate_BB_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Use"]
    Generate_BB_Invoice_PDF =  Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["PDF"]["Generate"]
    Generate_BB_IAL = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["IAL"]["Use"]

    Generate_BB_INV_Variable = BooleanVar(master=Frame, value=Generate_BB_Invoice, name="Generate_BB_INV_Variable")
    Generate_BB_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_BB_Invoice_PDF, name="Generate_BB_INV_PDF_Variable")
    Generate_BB_IAL_Variable = BooleanVar(master=Frame, value=Generate_BB_IAL, name="Generate_BB_IAL_Variable")

    # Tab View - BackBone Billing
    TabView_BB = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Column_B, Tab_size="Download", GUI_Level_ID=2)
    TabView_BB.pack_propagate(flag=False)
    Tab_BB = TabView_BB.add("BackBone Billing")
    TabView_BB.set("BackBone Billing")
    Tab_BB_ToolTip_But = TabView_BB.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_ToolTip_But, message="BackBone Billing invoice .json generator.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # Field - Use BackBone Billing Invoice
    Generate_BB_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Invoice",  Field_Type="Input_CheckBox")  
    Generate_BB_INV_Frame_Var = Generate_BB_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_BB_INV_Frame_Var.configure(variable=Generate_BB_INV_Variable, text="")

    if Generate_BB_INV_Variable.get() == True:
        pass
    elif Generate_BB_INV_Variable.get() == False:
        Generate_BB_INV_PDF_Variable.set(value=False)
        Generate_BB_IAL_Variable.set(value=False)
    else:
        pass

    # Field - Use Invoice PDF
    Generate_BB_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Invoice .pdf",  Field_Type="Input_CheckBox")  
    Generate_BB_INV_PDF_Frame_Var = Generate_BB_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_BB_INV_PDF_Frame_Var.configure(variable=Generate_BB_INV_PDF_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_BB_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "PDF", "Generate"], Information=Generate_BB_INV_PDF_Variable))

    # Field - Use IAL
    Generate_IAL_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="IAL",  Field_Type="Input_CheckBox")  
    Generate_IAL_Frame_Var = Generate_IAL_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_IAL_Frame_Var.configure(variable=Generate_BB_IAL_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_BB_IAL_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "IAL", "Use"], Information=Generate_BB_IAL_Variable))

    if Generate_BB_INV_Variable.get() == True:
        Generate_BB_INV_PDF_Frame_Var.configure(state="normal")
        Generate_IAL_Frame_Var.configure(state="normal")
    elif Generate_BB_INV_Variable.get() == False:
        Generate_BB_INV_PDF_Frame_Var.configure(state="disabled")
        Generate_IAL_Frame_Var.configure(state="disabled")
    else:
        pass

    BB_Block_Variable_list = [Generate_BB_INV_PDF_Variable, Generate_BB_IAL_Variable]
    BB_Block_Field_list = [Generate_BB_INV_PDF_Frame_Var, Generate_IAL_Frame_Var]
    BB_Block_JSON_path_list = [["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "PDF", "Generate"], ["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "IAL", "Use"]]
    Generate_BB_INV_Frame_Var.configure(command = lambda: CustomTkinter_Functions.Field_Block_Bool(Settings=Settings, window=window, Selected_Variable=Generate_BB_INV_Variable, Selected_Field=Generate_BB_INV_Frame_Var, Selected_JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Use"], Block_Variable_list=BB_Block_Variable_list, Block_Field_list=BB_Block_Field_list, Block_JSON_path_list=BB_Block_JSON_path_list))

    # Vendor
    BB_Vendor_Used = Documents["BackBone_Billing"]["Vendors_List"]
    BB_Vendor_Used_Variable = StringVar(master=Frame, value=BB_Vendor_Used, name="BB_Vendor_Used_Variable")

    # Field - Vendor Filter
    BB_Vendor_Used_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Vendor", Field_Type="Input_OptionMenu")  
    BB_Vendor_Used_Frame_Var = BB_Vendor_Used_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    BB_Vendor_Used_Frame_Var.configure(variable=BB_Vendor_Used_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Vendor_Used_Frame_Var, values=Vendor_Lists, command=lambda Selected_Value: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=BB_Vendor_Used_Variable, File_Name="Documents", JSON_path=["BackBone_Billing", "Used"], Information=Selected_Value), GUI_Level_ID=3)


    # Button - Generate BackBone Billing Invoice
    Button_Generate_BB = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_BB, Button_Size="Normal")
    Button_Generate_BB.configure(text="Generate", command = lambda:Generate_BackBone_Billing())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Generate_BB, message="Generate marked documents for selected BackBoneBilling Invoice.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # ---------------- Purchase Return Order Tab ---------------- #
    Generate_PRO_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Use"]
    Generate_PRO_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["Use"]
    Generate_PRO_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["PDF"]["Generate"]

    Generate_PRO_CON_Variable = BooleanVar(master=Frame, value=Generate_PRO_Confirmation, name="Generate_PRO_CON_Variable")
    Generate_PRO_INV_Variable = BooleanVar(master=Frame, value=Generate_PRO_Invoice, name="Generate_PRO_INV_Variable")
    Generate_PRO_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_PRO_Invoice_PDF, name="Generate_PRO_INV_PDF_Variable")

    # Tab View - Purchase Return Order
    TabView_PRO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Column_B, Tab_size="Download", GUI_Level_ID=2)
    TabView_PRO.pack_propagate(flag=False)
    Tab_PRO = TabView_PRO.add("Return Order")
    TabView_PRO.set("Return Order")
    Tab_PRO_ToolTip_But = TabView_PRO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PRO_ToolTip_But, message="Purchase Return Order .json generator.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # Field - Use Confirmation
    Generate_PRO_Conf_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Confirmation",  Field_Type="Input_CheckBox")  
    Generate_PRO_Conf_Frame_Var = Generate_PRO_Conf_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_Conf_Frame_Var.configure(variable=Generate_PRO_CON_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_PRO_CON_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Return_Order", "Use"], Information=Generate_PRO_CON_Variable))

    # Field - Use Credit Memo
    Generate_PRO_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Credit Memo",  Field_Type="Input_CheckBox")  
    Generate_PRO_INV_Frame_Var = Generate_PRO_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_INV_Frame_Var.configure(variable=Generate_PRO_INV_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_PRO_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "Use"], Information=Generate_PRO_INV_Variable))

    if Generate_PRO_INV_Variable.get() == True:
        pass
    elif Generate_PRO_INV_Variable.get() == False:
        Generate_PRO_INV_PDF_Variable.set(value=False)
    else:
        pass

    # Field - Use Invoice PDF
    Generate_PRO_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Invoice .pdf",  Field_Type="Input_CheckBox")  
    Generate_PRO_INV_PDF_Frame_Var = Generate_PRO_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_INV_PDF_Frame_Var.configure(variable=Generate_PRO_INV_PDF_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Generate_PRO_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "PDF", "Generate"], Information=Generate_PRO_INV_PDF_Variable))

    if Generate_PRO_INV_Variable.get() == True:
        Generate_PRO_INV_PDF_Frame_Var.configure(state="normal")
    elif Generate_PRO_INV_Variable.get() == False:
        Generate_PRO_INV_PDF_Frame_Var.configure(state="disabled")
    else:
        pass

    PRO_Block_Variable_list = [Generate_PRO_INV_PDF_Variable]
    PRO_Block_Field_list = [Generate_PRO_INV_PDF_Frame_Var]
    PRO_Block_JSON_path_list =[["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "PDF", "Generate"]]
    Generate_PRO_INV_Frame_Var.configure(command = lambda: CustomTkinter_Functions.Field_Block_Bool(Settings=Settings, window=window, Selected_Variable=Generate_PRO_INV_Variable, Selected_Field=Generate_PRO_INV_Frame_Var, Selected_JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "Use"], Block_Variable_list=PRO_Block_Variable_list, Block_Field_list=PRO_Block_Field_list, Block_JSON_path_list=PRO_Block_JSON_path_list))

    # Selected Purchase Orders List
    PRO_Selected_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Selected PROs", Field_Type="Input_Normal")  
    PRO_Selected_Frame_Var = PRO_Selected_Frame.children["!ctkframe3"].children["!ctkentry"]
    PRO_Selected_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=[str(PRO_Selected_Frame_Var.get()).replace(" ", "")]))
    PRO_Selected_Frame_Var.configure(placeholder_text="Purchase Ret. Orders", placeholder_text_color="#949A9F")

    # Buttons
    Button_PRO_Generate_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_PRO, Button_Size="Small")
    Button_PRO_Generate_Var.configure(text="List", command = lambda: Start_Order_Return_Show_Thread(Button=Button_PRO_Generate_Var, Document_Type="Return Order"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PRO_Generate_Var, message="Show Listbox with all available Purchase Return Orders for selection.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # Buttons - Generate
    Button_PRO_Show_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_PRO, Button_Size="Small")
    Button_PRO_Show_Var.configure(text="Generate", command = lambda: Generate_Purchase_Return_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PRO_Show_Var, message="Generate marked documents for selected PROs.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # Must be at the end !!!
    Companies_Frame_Var = Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Companies_Frame, values=Companies_List, command = lambda Selected_Company: Get_Logistic_Process(PO_MUL_LOG_PROC_Frame=PO_MUL_LOG_PROC_Frame, BB_Vendor_Used_Frame=BB_Vendor_Used_Frame, Selected_Company=Selected_Company) , GUI_Level_ID=1)
    Button_Download_Company.configure(text="Get Companies", command = lambda: Download_Companies(Companies_Frame_Var=Companies_Frame_Var))
    
    # Build look of Widget
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=10, pady=10)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="x", expand=False, padx=10, pady=10)

    NUS_Version_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    NUS_Version_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    Environment_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Environment_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    NOC_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    NOC_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    Button_Download_Company.pack(side="left", fill="none", expand=False, padx=(5, 5), pady=5)
    Companies_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Companies_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)

    Progress_Bar.pack(side="top", fill="x", expand=True, padx=5, pady=(5,0))
    Frame_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    TabView_PO.pack(side="top", fill="both", expand=False, padx=10, pady=5)
    Generate_Conf_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_CPDI_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PREA_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_DEL_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_IAL_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    TabView_One_PO.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    PO_Selected_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PO_One_Generate_Var.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    TabView_Multi_PO.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    PO_MUL_LOG_PROC_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PO_Show_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)
    Button_PO_Multi_Generate_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)

    TabView_BB.pack(side="top", fill="y", expand=True, padx=10, pady=5)
    Generate_BB_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_BB_INV_PDF_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Generate_BB.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    TabView_PRO.pack(side="top", fill="y", expand=True, padx=10, pady=10)
    Generate_PRO_Conf_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PRO_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PRO_INV_PDF_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PRO_Selected_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PRO_Generate_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)
    Button_PRO_Show_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)
    