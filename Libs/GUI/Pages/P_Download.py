# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, BooleanVar

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Data_Functions as Data_Functions
import Libs.Downloader.Downloader as Downloader
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

def Page_Download(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    NUS_Version_List = Settings["0"]["Connection"]["NUS_Version_List"]
    Environment_List = Settings["0"]["Connection"]["Environment_List"]
    NOC_List = Settings["0"]["Connection"]["NOC_List"]
    Companies_List = []
    

    NUS_Version_Variable = StringVar(master=Frame, value="Cloud", name="NUS_Version_Variable")
    Environment_Variable = StringVar(master=Frame, value="QA", name="Environment_Variable")
    NOC_Variable = StringVar(master=Frame, value="Core", name="NOC_Variable")
    Company_Variable = StringVar(master=Frame, value="-", name="Company_Variable")

    # ------------------------- Local Functions ------------------------#
    def Download_Companies(Companies_Frame_Var: CTkScrollableDropdown) -> list:
        global Companies_list
        Companies_list = Downloader.Get_Companies_List(Configuration=Configuration, NUS_version=NUS_Version_Variable.get(), NOC=NOC_Variable.get(), Environment=Environment_Variable.get())

        if len(Companies_list) > 0:
            # Update Option List
            Companies_Frame_Var.configure(values=Companies_list)

            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Companies downloaded.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

    def Generate_Purchase_Orders() -> None:
        print("Generate_Purchase_Orders")
        pass

    def Purchase_Orders_Show(Document_Type: str) -> None:
        Purchase_Orders_List = []
        print(Purchase_Orders_List)
        Purchase_Orders_List = Downloader.Get_Orders_List(Configuration=Configuration, NUS_version=NUS_Version_Variable.get(), NOC=NOC_Variable.get(), Environment=Environment_Variable.get(), Company=Company_Variable.get(), Document_Type=Document_Type)

        print(Purchase_Orders_List)

    def Generate_BackBone_Billing() -> None:
        print("Generate_BackBone_Billing")
        pass

    def Generate_Purchase_Return_Orders() -> None:
        print("Generate_Purchase_Return_Orders")
        pass


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

    # EnCompanies List
    Companies_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Companies_Text.configure(text="Companies: ")

    Companies_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    Companies_Frame.configure(width=200)
    Companies_Frame.configure(variable=Company_Variable)
    Companies_Frame_Var = Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Companies_Frame, values=Companies_List, command=None, GUI_Level_ID=1)
    
    Button_Download_Company.configure(text="Get Companies", command = lambda:Download_Companies(Companies_Frame_Var=Companies_Frame_Var))

    # ------------------------- Work Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, orientation="Horizontal", Progress_Size="Download_Process", GUI_Level_ID=1)
    Progress_Bar.set(value=0)

    # -------- Purchase Order Tab -------- #
    Generate_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Purchase_Order"]["Use"]
    Generate_PreAdvice = Settings["0"]["HQ_Data_Handler"]["PreAdvice"]["Use"]
    Generate_CPDI = Settings["0"]["HQ_Data_Handler"]["CPDI"]["Use"]
    Generate_Delivery = Settings["0"]["HQ_Data_Handler"]["Delivery"]["Use"]
    Generate_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["Use"]
    Generate_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Purchase_Order"]["PDF"]["Generate"]
    Generate_IAL = Settings["0"]["HQ_Data_Handler"]["IAL"]["Use"]

    Generate_CON_Variable = BooleanVar(master=Frame, value=Generate_Confirmation, name="Generate_CON_Variable")
    Generate_PRA_Variable = BooleanVar(master=Frame, value=Generate_PreAdvice, name="Generate_PRA_Variable")
    Generate_CPD_Variable = BooleanVar(master=Frame, value=Generate_CPDI, name="Generate_CPD_Variable")
    Generate_DEL_Variable = BooleanVar(master=Frame, value=Generate_Delivery, name="Generate_DEL_Variable")
    Generate_INV_Variable = BooleanVar(master=Frame, value=Generate_Invoice, name="Generate_INV_Variable")
    Generate_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_Invoice_PDF, name="Generate_INV_PDF_Variable")
    Generate_IAL_Variable = BooleanVar(master=Frame, value=Generate_IAL, name="Generate_IAL_Variable")

    # Tab View - Purchase Order
    TabView_PO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Download", GUI_Level_ID=2)
    TabView_PO.pack_propagate(flag=False)
    Tab_PO = TabView_PO.add("Purchase Order")
    TabView_PO.set("Purchase Order")
    Tab_PO_ToolTip_But = TabView_PO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Purchase Order .json generator.", ToolTip_Size="Normal", GUI_Level_ID=2)
    
    # Field - Use Confirmation
    Generate_Conf_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Confirmation", Field_Type="Input_CheckBox") 
    Generate_Conf_Frame_Var = Generate_Conf_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_Conf_Frame_Var.configure(variable=Generate_CON_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_CON_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Use"], Information=Generate_CON_Variable))

    # Field - Use CPDI
    Generate_CPDI_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="CPDI", Field_Type="Input_CheckBox") 
    Generate_CPDI_Frame_Var = Generate_CPDI_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_CPDI_Frame_Var.configure(variable=Generate_CPD_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_CPD_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Use"], Information=Generate_CPD_Variable))

    # Field - Use PreAdvice
    Generate_PREA_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="PreAdvice", Field_Type="Input_CheckBox") 
    Generate_PREA_Frame_Var = Generate_PREA_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PREA_Frame_Var.configure(variable=Generate_PRA_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRA_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Use"], Information=Generate_PRA_Variable))

    # Field - Use Delivery
    Generate_DEL_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Delivery", Field_Type="Input_CheckBox") 
    Generate_DEL_Frame_Var = Generate_DEL_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_DEL_Frame_Var.configure(variable=Generate_DEL_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_DEL_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Use"], Information=Generate_DEL_Variable))

    # Field - Use Invoice
    Generate_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Invoice", Field_Type="Input_CheckBox") 
    Generate_INV_Frame_Var = Generate_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_INV_Frame_Var.configure(variable=Generate_INV_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Use"], Information=Generate_INV_Variable))

    # Field - Use Invoice PDF
    Generate_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Invoice PDF", Field_Type="Input_CheckBox") 
    Generate_INV_PDF_Frame_Var = Generate_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_INV_PDF_Frame_Var.configure(variable=Generate_INV_PDF_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "PDF", "Generate"], Information=Generate_INV_PDF_Variable))

    # Field - Use IAL
    Generate_IAL_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="IAL", Field_Type="Input_CheckBox") 
    Generate_IAL_Frame_Var = Generate_IAL_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_IAL_Frame_Var.configure(variable=Generate_IAL_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_IAL_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "IAL", "Use"], Information=Generate_IAL_Variable))

    # Selected Purchase Orders List
    PO_Selected_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Selected POs", Field_Type="Input_Normal") 
    PO_Selected_Frame_Var = PO_Selected_Frame.children["!ctkframe3"].children["!ctkentry"]
    PO_Selected_Frame_Var.configure(placeholder_text="Purchase Orders", placeholder_text_color="#949A9F")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Tab_PO, Configuration=Configuration, Field_Frame_Type="Half_size" , Buttons_count=2, Button_Size="Normal") 
    Button_PO_Generate_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_PO_Generate_Var.configure(text="Generate", command = lambda: Generate_Purchase_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_Generate_Var, message="Process selected files for filtered Purchase Orders.", ToolTip_Size="Normal", GUI_Level_ID=2)

    Button_PO_Show_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_PO_Show_Var.configure(text="Select Multiple", command = lambda: Purchase_Orders_Show(Document_Type="Order"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PO_Show_Var, message="Show Listbox with all available Purchase Orders for selection.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # -------- BackBone Billing Tab -------- #
    Generate_BB_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Use"]
    Generate_BB_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["PDF"]["Generate"]

    Generate_BB_INV_Variable = BooleanVar(master=Frame, value=Generate_BB_Invoice, name="Generate_BB_INV_Variable")
    Generate_BB_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_BB_Invoice_PDF, name="Generate_BB_INV_PDF_Variable")

    # Tab View - BackBone Billing
    TabView_BB = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Download", GUI_Level_ID=2)
    TabView_BB.pack_propagate(flag=False)
    Tab_BB = TabView_BB.add("BackBone Billing")
    TabView_BB.set("BackBone Billing")
    Tab_BB_ToolTip_But = TabView_BB.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_ToolTip_But, message="BackBone Billing invoice .json generator.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # Field - Use BackBone Billing Invoice
    Generate_BB_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Invoice", Field_Type="Input_CheckBox") 
    Generate_BB_INV_Frame_Var = Generate_BB_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_BB_INV_Frame_Var.configure(variable=Generate_BB_INV_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_BB_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Use"], Information=Generate_BB_INV_Variable))

    # Field - Use Invoice PDF
    Generate_BB_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Invoice .pdf", Field_Type="Input_CheckBox") 
    Generate_BB_INV_PDF_Frame_Var = Generate_BB_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_BB_INV_PDF_Frame_Var.configure(variable=Generate_BB_INV_PDF_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_BB_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "PDF", "Generate"], Information=Generate_BB_INV_PDF_Variable))

    # Button - Generate BAckBone Billing Invoice
    Button_Generate_BB = Elements.Get_Button_Text(Configuration=Configuration, Frame=Tab_BB, Button_Size="Normal")
    Button_Generate_BB.configure(text="Generate", command = lambda:Generate_BackBone_Billing())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Generate_BB, message="Generate marked documents for selected BackBoneBilling Invoice.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # -------- Purchase Return Order Tab -------- #
    Generate_PRO_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Use"]
    Generate_PRO_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["Use"]
    Generate_PRO_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["PDF"]["Generate"]

    Generate_PRO_CON_Variable = BooleanVar(master=Frame, value=Generate_PRO_Confirmation, name="Generate_PRO_CON_Variable")
    Generate_PRO_INV_Variable = BooleanVar(master=Frame, value=Generate_PRO_Invoice, name="Generate_PRO_INV_Variable")
    Generate_PRO_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_PRO_Invoice_PDF, name="Generate_PRO_INV_PDF_Variable")

    # Tab View - Purchase Return Order
    TabView_PRO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Download", GUI_Level_ID=2)
    TabView_PRO.pack_propagate(flag=False)
    Tab_PRO = TabView_PRO.add("Return Order")
    TabView_PRO.set("Return Order")
    Tab_PRO_ToolTip_But = TabView_PRO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PRO_ToolTip_But, message="Purchase Return Order .json generator.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # Field - Use Confirmation
    Generate_PRO_Conf_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Confirmation", Field_Type="Input_CheckBox") 
    Generate_PRO_Conf_Frame_Var = Generate_PRO_Conf_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_Conf_Frame_Var.configure(variable=Generate_PRO_CON_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRO_CON_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Return_Order", "Use"], Information=Generate_PRO_CON_Variable))

    # Field - Use Credit Memo
    Generate_PRO_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Credit Memo", Field_Type="Input_CheckBox") 
    Generate_PRO_INV_Frame_Var = Generate_PRO_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_INV_Frame_Var.configure(variable=Generate_PRO_INV_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRO_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "Use"], Information=Generate_PRO_INV_Variable))

    # Field - Use Invoice PDF
    Generate_PRO_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Invoice .pdf", Field_Type="Input_CheckBox") 
    Generate_PRO_INV_PDF_Frame_Var = Generate_PRO_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_INV_PDF_Frame_Var.configure(variable=Generate_PRO_INV_PDF_Variable, text="", command=lambda : Data_Functions.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRO_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "PDF", "Generate"], Information=Generate_PRO_INV_PDF_Variable))

    # Selected Purchase Orders List
    PRO_Selected_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Selected PROs", Field_Type="Input_Normal") 
    PRO_Selected_Frame_Var = PRO_Selected_Frame.children["!ctkframe3"].children["!ctkentry"]
    PRO_Selected_Frame_Var.configure(placeholder_text="Purchase Ret. Orders", placeholder_text_color="#949A9F")

    # Buttons
    Button_PRO_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Tab_PRO, Configuration=Configuration, Field_Frame_Type="Half_size" , Buttons_count=2, Button_Size="Normal") 
    Button_PRO_Generate_Var = Button_PRO_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_PRO_Generate_Var.configure(text="Generate", command = lambda: Generate_Purchase_Return_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PRO_Generate_Var, message="Generate marked documents for selected PROs.", ToolTip_Size="Normal", GUI_Level_ID=2)

    Button_PRO_Show_Var = Button_PRO_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_PRO_Show_Var.configure(text="Select Multiple", command = lambda: Purchase_Orders_Show(Document_Type="Return Order"))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_PRO_Show_Var, message="Show Listbox with all available Purchase Orders for selection.", ToolTip_Size="Normal", GUI_Level_ID=2)

    # Build look of Widget
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=10, pady=10)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=False, padx=0, pady=0)

    NUS_Version_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    NUS_Version_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    Environment_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Environment_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    NOC_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    NOC_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    Button_Download_Company.pack(side="left", fill="none", expand=False, padx=(5, 5), pady=5)
    Companies_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Companies_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)

    Progress_Bar.pack(side="top", fill="x", expand=False, padx=5, pady=(10,5))

    TabView_PO.pack(side="left", fill="y", expand=False, padx=10, pady=10)
    Generate_Conf_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_CPDI_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PREA_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_DEL_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_IAL_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PO_Selected_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    TabView_BB.pack(side="left", fill="y", expand=False, padx=10, pady=10)
    Generate_BB_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_BB_INV_PDF_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Generate_BB.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    TabView_PRO.pack(side="left", fill="y", expand=False, padx=10, pady=10)
    Generate_PRO_Conf_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PRO_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PRO_INV_PDF_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    PRO_Selected_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_PRO_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
