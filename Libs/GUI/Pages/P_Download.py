# Import Libraries
import threading

from customtkinter import CTk, CTkFrame, CTkButton, CTkScrollableFrame, StringVar, BooleanVar

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Downloader.Downloader as Downloader
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 
from Libs.GUI.Widgets.Widgets_Class import WidgetRow_CheckBox


def Page_Download(Settings: dict, Configuration: dict|None, window: CTk|None, Documents: dict, Frame: CTkFrame):
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

    Last_Used_NUS_Version = Settings["0"]["Connection"]["Last_Used_NUS_Version"]
    NUS_Version_Variable = StringVar(master=Frame, value=Last_Used_NUS_Version, name="NUS_Version_Variable")
    Last_Used_Environment = Settings["0"]["Connection"]["Last_Used_Environment"]
    Environment_Variable = StringVar(master=Frame, value=Last_Used_Environment, name="Environment_Variable")
    Last_Used_NOC = Settings["0"]["Connection"]["Last_Used_NOC"]
    NOC_Variable = StringVar(master=Frame, value=Last_Used_NOC, name="NOC_Variable")
    Company_Variable = StringVar(master=Frame, value="-", name="Company_Variable")
    Logistic_Process_Variable = StringVar(master=Frame, value="-", name="Logistic_Process_Variable")

    # ------------------------- Local Functions ------------------------#
    def Disable_buttons():
        Button_PO_One_Generate_Var.configure(state="disabled")
        Button_PO_Show_Var.configure(state="disabled")
        Button_PO_Multi_Generate_Var.configure(state="disabled")
        Button_Generate_BB.configure(state="disabled")
        Button_PRO_Show_Var.configure(state="disabled")
        Buttons_list = [Button_PO_One_Generate_Var, Button_PO_Show_Var, Button_PO_Multi_Generate_Var, Button_Generate_BB, Button_PRO_Show_Var]
        return Buttons_list

    def Download_Companies(Companies_Frame_Var: CTkScrollableDropdown) -> None:
        Companies_thread = threading.Thread(target=Downloader.Get_Companies_List, args=(Configuration, window, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Companies_Frame_Var))
        Companies_thread.start()
        Companies_thread.join(timeout=0.1) 

    def Select_Company(PO_MUL_LOG_PROC_Frame: CTkFrame, BB_Vendor_Used_Frame: CTkFrame, Selected_Company: str) -> list:
        # Buttons - disable
        Buttons_list = Disable_buttons()

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

        # Function Company Select --> because multiple thread (in previous version was wrong)
        Company_Select_thread = threading.Thread(target=Downloader.Select_Company_Process, args=(Configuration, window, Documents, NUS_Version, NOC, Environment, Selected_Company, Log_Proc_Used_Variable, PO_MUL_LOG_PROC_Frame, BB_Vendor_Used_Variable, BB_Vendor_Used_Frame, Buttons_list))
        Company_Select_thread.start()
        Company_Select_thread.join(timeout=0.1) 
        
    def Generate_Purchase_Orders() -> None:
        Purchase_Order_list = Documents["Purchase_Order"]["Purchase_Order_List"]
        if len(Purchase_Order_list) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no Purchase Order selected, you have to put one or select multiple to Download and Process.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            # Buttons - disable
            Buttons_list = Disable_buttons()

            Generate_PO_thread = threading.Thread(target=Downloader.Download_Data_Purchase_Orders, args=(Settings, Configuration, window, Progress_Bar, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Company_Variable.get(), Purchase_Order_list, Buttons_list))
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
            # Buttons - disable
            Buttons_list = Disable_buttons()
            
            Generate_BB_Invoice_thread = threading.Thread(target=Downloader.Download_Data_BackBoneBilling, args=(Settings, Configuration, window, Progress_Bar, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Company_Variable.get(), Buy_from_Vendor_No, Buttons_list))
            Generate_BB_Invoice_thread.start()
            Generate_BB_Invoice_thread.join(timeout=0.1) 

    def Generate_Purchase_Return_Orders() -> None:
        Purchase_Return_Orders_List = Documents["Purchase_Return_Order"]["Purchase_Return_Order_List"]
        if len(Purchase_Return_Orders_List) == 0:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"There is no Purchase Order selected, you have to put one or select multiple to Download and Process.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            # Buttons - disable
            Buttons_list = Disable_buttons()

            Generate_PRO_thread = threading.Thread(target=Downloader.Download_Data_Return_Order, args=(Settings, Configuration, window, Progress_Bar, NUS_Version_Variable.get(), NOC_Variable.get(), Environment_Variable.get(), Company_Variable.get(), Purchase_Return_Orders_List, Buttons_list))
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
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=NUS_Version_Frame, values=NUS_Version_List, command=lambda Actual_NUS_Version: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=NUS_Version_Variable, File_Name="Settings", JSON_path=["0", "Connection", "Last_Used_NUS_Version"], Information=Actual_NUS_Version), GUI_Level_ID=1)

    # Environment
    Environment_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Environment_Text.configure(text="Environment: ")

    Environment_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    Environment_Frame.configure(width=140)
    Environment_Frame.configure(variable=Environment_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Environment_Frame, values=Environment_List, command=lambda Actual_Environment: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=Environment_Variable, File_Name="Settings", JSON_path=["0", "Connection", "Last_Used_Environment"], Information=Actual_Environment), GUI_Level_ID=1)

    # NOCs
    NOC_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    NOC_Text.configure(text="NOC: ")

    NOC_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    NOC_Frame.configure(width=140)
    NOC_Frame.configure(variable=NOC_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=NOC_Frame, values=NOC_List, command=lambda Actual_NOC: Data_Functions.Save_Value(Settings=Settings, Configuration=None, Documents=None, window=window, Variable=NOC_Variable, File_Name="Settings", JSON_path=["0", "Connection", "Last_Used_NOC"], Information=Actual_NOC), GUI_Level_ID=1)

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
    
    def Block_Invoice_PDF() ->  None:
        if Generate_INV_Variable.get() == False:
            Generate_INV_PDF_Variable.set(value=False)
            Generate_INV_PDF_Row.Change_Value()
        else:
            pass

    def Block_Preadvice() ->  None:
        if Generate_DEL_Variable.get() == False:
            Generate_PRA_Variable.set(value=False)
            Generate_PREA_Row.Change_Value()
        else:
            pass

    # Fields
    Generate_Conf_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PO, window=window, Field_Frame_Type="Half_size", Label="Confirmation", Variable=Generate_CON_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Use"])
    Generate_CPDI_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PO, window=window, Field_Frame_Type="Half_size", Label="CPDI", Variable=Generate_CPD_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "CPDI", "Use"])
    Generate_PREA_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PO, window=window, Field_Frame_Type="Half_size", Label="PreAdvice", Variable=Generate_PRA_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "PreAdvice", "Use"])
    
    DEL_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=[True, False], Freeze_fields=[[],[Generate_PREA_Row]])
    Generate_DEL_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PO, window=window, Field_Frame_Type="Half_size", Label="Delivery", Variable=Generate_DEL_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Delivery", "Use"], Field_list=[Generate_PREA_Row], Field_Blocking_dict=DEL_Fields_Blocking_dict)
    Generate_DEL_Row.Local_function_list = [Block_Preadvice]

    Generate_INV_PDF_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PO, window=window, Field_Frame_Type="Half_size", Label="Invoice PDF", Variable=Generate_INV_PDF_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "PDF", "Generate"])

    INV_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=[True, False], Freeze_fields=[[],[Generate_INV_PDF_Row]])
    Generate_INV_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PO, window=window, Field_Frame_Type="Half_size", Label="Invoice", Variable=Generate_INV_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Use"], Field_list=[Generate_INV_PDF_Row], Field_Blocking_dict=INV_Fields_Blocking_dict)
    Generate_INV_Row.Local_function_list = [Block_Invoice_PDF]

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
    Button_PO_One_Generate_Var.configure(text="Generate", command = lambda: Generate_Purchase_Orders(), state="disabled")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_One_Generate_Var, message="Generate selected documents for one Purchase Order.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # -------- Select Multiple -------- #
    TabView_Multi_PO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Tab_PO, Tab_size="Download", GUI_Level_ID=3)
    TabView_Multi_PO.pack_propagate(flag=False)
    Tab_Multi_PO = TabView_Multi_PO.add("Multiple Purchase Orders")
    TabView_Multi_PO.set("Multiple Purchase Orders")
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
    Button_PO_Show_Var.configure(text="List", command = lambda: Start_Order_Show_Thread(Button=Button_PO_Show_Var, PO_MUL_LOG_PROC_Frame_Var=PO_MUL_LOG_PROC_Frame_Var, Document_Type="Order"), state="disabled")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_Show_Var, message="Show Listbox with all available Purchase Orders for selection.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # Buttons - Generate
    Button_PO_Multi_Generate_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_Multi_PO, Button_Size="Normal")
    Button_PO_Multi_Generate_Var.configure(text="Generate", command = lambda: Generate_Purchase_Orders(), state="disabled")
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

    def Block_BB_Invoice_PDF() ->  None:
        if Generate_BB_INV_Variable.get() == False:
            Generate_BB_INV_PDF_Variable.set(value=False)
            Generate_BB_IAL_Variable.set(value=False)
            Generate_BB_INV_PDF_Row.Change_Value()
            Generate_IAL_Row.Change_Value()
        else:
            pass

    # Fields
    Generate_BB_INV_PDF_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_BB, window=window, Field_Frame_Type="Half_size", Label="Invoice PDF", Variable=Generate_BB_INV_PDF_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "PDF", "Generate"])
    Generate_IAL_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_BB, window=window, Field_Frame_Type="Half_size", Label="IAL", Variable=Generate_BB_IAL_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "IAL", "Use"])
    Use_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=[True, False], Freeze_fields=[[],[Generate_BB_INV_PDF_Row, Generate_IAL_Row]])
    Generate_BB_INV_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_BB, window=window, Field_Frame_Type="Half_size", Label="Invoice", Variable=Generate_BB_INV_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Use"], Field_list=[Generate_BB_INV_PDF_Row, Generate_IAL_Row], Field_Blocking_dict=Use_Fields_Blocking_dict)
    Generate_BB_INV_Row.Local_function_list = [Block_BB_Invoice_PDF]

    Generate_BB_INV_Row.Show()
    Generate_BB_INV_PDF_Row.Show()
    Generate_IAL_Row.Show()

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
    Button_Generate_BB.configure(text="Generate", command = lambda:Generate_BackBone_Billing(), state="disabled")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Generate_BB, message="Generate marked documents for selected BackBoneBilling Invoice.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # ---------------- Purchase Return Order Tab ---------------- #
    Generate_PRO_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Use"]
    Generate_PRO_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["Use"]
    Generate_PRO_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Return_Order"]["PDF"]["Generate"]

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

    def Block_PRO_Invoice() ->  None:
        if Generate_PRO_INV_Variable.get() == True:
            Generate_PRO_CON_Variable.set(value=False)
            Generate_PRO_Conf_Row.Change_Value()
        else:
            Generate_PRO_INV_PDF_Variable.set(value=False)
            Generate_PRO_INV_PDF_Row.Change_Value()
            
    def Block_PRO_Confirmation() ->  None:
        if Generate_PRO_CON_Variable.get() == True:
            Generate_PRO_INV_Variable.set(value=False)
            Generate_PRO_INV_Row.Change_Value()
        else:
            pass

    # Fields
    Generate_PRO_Conf_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PRO, window=window, Field_Frame_Type="Half_size", Label="Confirmation", Variable=Generate_PRO_CON_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Confirmation", "Return_Order", "Use"])
    Generate_PRO_INV_PDF_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PRO, window=window, Field_Frame_Type="Half_size", Label="Credit Memo PDF", Variable=Generate_PRO_INV_PDF_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "PDF", "Generate"])
    Use_Fields_Blocking_dict = CustomTkinter_Functions.Fields_Blocking(Values=[True, False], Freeze_fields=[[],[Generate_PRO_INV_PDF_Row]])
    Generate_PRO_INV_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Tab_PRO, window=window, Field_Frame_Type="Half_size", Label="Credit Memo", Variable=Generate_PRO_INV_Variable, Save_To="Settings", Save_path=["0", "HQ_Data_Handler", "Invoice", "Return_Order", "Use"], Field_list=[Generate_PRO_INV_PDF_Row], Field_Blocking_dict=Use_Fields_Blocking_dict)
    Generate_PRO_Conf_Row.Local_function_list = [Block_PRO_Confirmation]
    Generate_PRO_INV_Row.Local_function_list = [Block_PRO_Invoice]

    Generate_PRO_Conf_Row.Show()
    Generate_PRO_INV_Row.Show()
    Generate_PRO_INV_PDF_Row.Show()

    # Selected Purchase Orders List
    PRO_Selected_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Purchase Ret. Order", Field_Type="Input_Normal")  
    PRO_Selected_Frame_Var = PRO_Selected_Frame.children["!ctkframe3"].children["!ctkentry"]
    PRO_Selected_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=None, Documents=Documents, window=window, Variable=None, File_Name="Documents", JSON_path=["Purchase_Return_Order", "Purchase_Return_Order_List"], Information=[str(PRO_Selected_Frame_Var.get()).replace(" ", "")]))
    PRO_Selected_Frame_Var.configure(placeholder_text="Purchase Ret. Order", placeholder_text_color="#949A9F")

    # Buttons - Generate
    Button_PRO_Show_Var = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_PRO, Button_Size="Normal")
    Button_PRO_Show_Var.configure(text="Generate", command = lambda: Generate_Purchase_Return_Orders(), state="disabled")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PRO_Show_Var, message="Generate marked documents for selected PROs.", ToolTip_Size="Normal", GUI_Level_ID=3)

    # Must be at the end !!!
    Companies_Frame_Var = Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Companies_Frame, values=Companies_List, command = lambda Selected_Company: Select_Company(PO_MUL_LOG_PROC_Frame=PO_MUL_LOG_PROC_Frame, BB_Vendor_Used_Frame=BB_Vendor_Used_Frame, Selected_Company=Selected_Company) , GUI_Level_ID=1)
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
    Frame_Column_A.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
    Frame_Column_B.pack(side="left", fill="both", expand=True, padx=(5, 5), pady=5)

    TabView_PO.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    Generate_Conf_Row.Show()
    Generate_CPDI_Row.Show()
    Generate_PREA_Row.Show()
    Generate_DEL_Row.Show()
    Generate_INV_Row.Show()
    Generate_INV_PDF_Row.Show()
   
    TabView_One_PO.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    PO_Selected_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PO_One_Generate_Var.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    TabView_Multi_PO.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    PO_MUL_LOG_PROC_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PO_Show_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)
    Button_PO_Multi_Generate_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)

    TabView_BB.pack(side="top", fill="y", expand=True, padx=10, pady=5)
    BB_Vendor_Used_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Generate_BB.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    TabView_PRO.pack(side="top", fill="y", expand=True, padx=10, pady=5)
    PRO_Selected_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PRO_Show_Var.pack(side="left", fill="none", expand=True, padx=5, pady=5)
    