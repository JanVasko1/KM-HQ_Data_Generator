# Import Libraries
from customtkinter import CTk, CTkFrame, StringVar, BooleanVar
from CTkMessagebox import CTkMessagebox

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Azure.Authorization as Authorization
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Downloader.NAV_OData_API as NAV_OData_API
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
        User_Password = Defaults_Lists.Dialog_Window_Request(Configuration=Configuration, title="Navision Login", text="Write your password", Dialog_Type="Password")
        
        if User_Password == None:
            Error_Message = CTkMessagebox(title="Error", message="Cannot download, because of missing Password.", icon="cancel", fade_in_duration=1)
            Error_Message.get()
        else:
            client_id, client_secret, tenant_id = Defaults_Lists.Load_Exchange_env()
            access_token = Authorization.Azure_OAuth(Settings=Settings, client_id=client_id, client_secret=client_secret, tenant_id=tenant_id, User_Password=User_Password)
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'}

            Companies_list = NAV_OData_API.Get_Companies(headers=headers, tenant_id=tenant_id, NUS_version=NUS_Version_Variable.get(), NOC=NOC_Variable.get(), Environment=Environment_Variable.get())

            if len(Companies_list) > 0:
                # Update Option List
                Companies_Frame_Var.configure(values=Companies_list)

                Success_Message = CTkMessagebox(title="Success", message="Companies downloaded.", icon="check", option_1="Thanks", fade_in_duration=1)
                Success_Message.get()
            else:
                pass

    def Generate_Purchase_Orders() -> None:
        print("Generate_Purchase_Orders")
        pass

    def Generate_BackBone_Billing() -> None:
        print("Generate_Purchase_Orders")
        pass

    def Generate_Purchase_Return_Orders() -> None:
        print("Generate_Purchase_Orders")
        pass

    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Download_State_Area.pack_propagate(flag=False)

    Frame_Download_Sub_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Download_Sub_State_Area.pack_propagate(flag=False)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- State Area -------------------------#
    # NUS Version
    NUS_Version_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    NUS_Version_Text.configure(text="NUS Version: ")

    NUS_Version_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    NUS_Version_Frame.configure(width=140)
    NUS_Version_Frame.configure(variable=NUS_Version_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=NUS_Version_Frame, values=NUS_Version_List, command=None)

    # Environment
    Environment_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Environment_Text.configure(text="Environment: ")

    Environment_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    Environment_Frame.configure(width=140)
    Environment_Frame.configure(variable=Environment_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Environment_Frame, values=Environment_List, command=None)

    # NOCs
    NOC_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    NOC_Text.configure(text="NOC: ")

    NOC_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    NOC_Frame.configure(width=140)
    NOC_Frame.configure(variable=NOC_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=NOC_Frame, values=NOC_List, command=None)

    # Button - Download Company
    Button_Download_Company = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Download_State_Area, Button_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download_Company, message="Download Companies list based on selected NUS Version, Environment and NOC.", ToolTip_Size="Normal")

    # EnCompanies List
    Companies_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Companies_Text.configure(text="Companies: ")

    Companies_Frame = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Download_State_Area)
    Companies_Frame.configure(width=200)
    Companies_Frame.configure(variable=Company_Variable)
    Companies_Frame_Var = Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Companies_Frame, values=Companies_List, command=None)
    

    Button_Download_Company.configure(text="Get Companies", command = lambda:Download_Companies(Companies_Frame_Var=Companies_Frame_Var))


    # ------------------------- Sub State Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Frame_Download_Sub_State_Area, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.set(value=0)

    Progress_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_Sub_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Progress_text.configure(text=f"Download progress", width=200)

    # ------------------------- Work Area -------------------------#
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
    TabView_PO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Download")
    TabView_PO.pack_propagate(flag=False)
    Tab_PO = TabView_PO.add("Purchase Order")
    TabView_PO.set("Purchase Order")
    Tab_PO_ToolTip_But = TabView_PO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Purchase Order .json generator.", ToolTip_Size="Normal")
    
    # Field - Use Confirmation
    Generate_Conf_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Confirmation", Field_Type="Input_CheckBox") 
    Generate_Conf_Frame_Var = Generate_Conf_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_Conf_Frame_Var.configure(variable=Generate_CON_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_CON_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Purchase_Order", "Use"], Information=Generate_CON_Variable))

    # Field - Use PreAdvice
    Generate_PREA_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="PreAdvice", Field_Type="Input_CheckBox") 
    Generate_PREA_Frame_Var = Generate_PREA_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PREA_Frame_Var.configure(variable=Generate_PRA_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRA_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "PreAdvice", "Use"], Information=Generate_PRA_Variable))

    # Field - Use CPDI
    Generate_CPDI_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="CPDI", Field_Type="Input_CheckBox") 
    Generate_CPDI_Frame_Var = Generate_CPDI_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_CPDI_Frame_Var.configure(variable=Generate_CPD_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_CPD_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "CPDI", "Use"], Information=Generate_CPD_Variable))

    # Field - Use Delivery
    Generate_DEL_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Delivery", Field_Type="Input_CheckBox") 
    Generate_DEL_Frame_Var = Generate_DEL_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_DEL_Frame_Var.configure(variable=Generate_DEL_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_DEL_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Delivery", "Use"], Information=Generate_DEL_Variable))

    # Field - Use Invoice
    Generate_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Invoice", Field_Type="Input_CheckBox") 
    Generate_INV_Frame_Var = Generate_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_INV_Frame_Var.configure(variable=Generate_INV_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "Use"], Information=Generate_INV_Variable))

    # Field - Use Invoice PDF
    Generate_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="Invoice .pdf", Field_Type="Input_CheckBox") 
    Generate_INV_PDF_Frame_Var = Generate_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_INV_PDF_Frame_Var.configure(variable=Generate_INV_PDF_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Purchase_Order", "PDF", "Generate"], Information=Generate_INV_PDF_Variable))

    # Field - Use IAL
    Generate_IAL_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PO, Field_Frame_Type="Half_size" , Label="IAL", Field_Type="Input_CheckBox") 
    Generate_IAL_Frame_Var = Generate_IAL_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_IAL_Frame_Var.configure(variable=Generate_IAL_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_IAL_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "IAL", "Use"], Information=Generate_IAL_Variable))


    # Button - Generate Purchase Orders
    Button_Generate_PO = Elements.Get_Button(Configuration=Configuration, Frame=Tab_PO, Button_Size="Normal")
    Button_Generate_PO.configure(text="Generate", command = lambda:Generate_Purchase_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Generate_PO, message="Generate marked documents for selected POs.", ToolTip_Size="Normal")

    # -------- BackBone Billing Tab -------- #
    Generate_BB_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Use"]
    Generate_BB_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["PDF"]["Generate"]

    Generate_BB_INV_Variable = BooleanVar(master=Frame, value=Generate_BB_Invoice, name="Generate_BB_INV_Variable")
    Generate_BB_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_BB_Invoice_PDF, name="Generate_BB_INV_PDF_Variable")

    # Tab View - BackBone Billing
    TabView_BB = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Download")
    TabView_BB.pack_propagate(flag=False)
    Tab_BB = TabView_BB.add("BackBone Billing")
    TabView_BB.set("BackBone Billing")
    Tab_BB_ToolTip_But = TabView_BB.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_BB_ToolTip_But, message="BackBone Billing invoice .json generator.", ToolTip_Size="Normal")

    # Field - Use BackBone Billing Invoice
    Generate_BB_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Invoice", Field_Type="Input_CheckBox") 
    Generate_BB_INV_Frame_Var = Generate_BB_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_BB_INV_Frame_Var.configure(variable=Generate_BB_INV_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_BB_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "Use"], Information=Generate_BB_INV_Variable))

    # Field - Use Invoice PDF
    Generate_BB_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_BB, Field_Frame_Type="Half_size" , Label="Invoice .pdf", Field_Type="Input_CheckBox") 
    Generate_BB_INV_PDF_Frame_Var = Generate_BB_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_BB_INV_PDF_Frame_Var.configure(variable=Generate_BB_INV_PDF_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_BB_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "BackBone_Billing", "PDF", "Generate"], Information=Generate_BB_INV_PDF_Variable))


    # Button - Generate BAckBone Billing Invoice
    Button_Generate_BB = Elements.Get_Button(Configuration=Configuration, Frame=Tab_BB, Button_Size="Normal")
    Button_Generate_BB.configure(text="Generate", command = lambda:Generate_BackBone_Billing())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Generate_BB, message="Generate marked documents for selected BackBoneBilling Invoice.", ToolTip_Size="Normal")

    # -------- Purchase Return Order Tab -------- #
    Generate_PRO_Confirmation = Settings["0"]["HQ_Data_Handler"]["Confirmation"]["Return_Order"]["Use"]
    Generate_PRO_Invoice = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["Use"]
    Generate_PRO_Invoice_PDF = Settings["0"]["HQ_Data_Handler"]["Invoice"]["Credit_Memo"]["PDF"]["Generate"]

    Generate_PRO_CON_Variable = BooleanVar(master=Frame, value=Generate_PRO_Confirmation, name="Generate_PRO_CON_Variable")
    Generate_PRO_INV_Variable = BooleanVar(master=Frame, value=Generate_PRO_Invoice, name="Generate_PRO_INV_Variable")
    Generate_PRO_INV_PDF_Variable = BooleanVar(master=Frame, value=Generate_PRO_Invoice_PDF, name="Generate_PRO_INV_PDF_Variable")

    # Tab View - Purchase Return Order
    TabView_PRO = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Download")
    TabView_PRO.pack_propagate(flag=False)
    Tab_PRO = TabView_PRO.add("Return Order")
    TabView_PRO.set("Return Order")
    Tab_PRO_ToolTip_But = TabView_PRO.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PRO_ToolTip_But, message="Purchase Return Order .json generator.", ToolTip_Size="Normal")

    # Field - Use Confirmation
    Generate_PRO_Conf_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Confirmation", Field_Type="Input_CheckBox") 
    Generate_PRO_Conf_Frame_Var = Generate_PRO_Conf_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_Conf_Frame_Var.configure(variable=Generate_PRO_CON_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRO_CON_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Confirmation", "Return_Order", "Use"], Information=Generate_PRO_CON_Variable))

    # Field - Use Credit Memo
    Generate_PRO_INV_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Credit Memo", Field_Type="Input_CheckBox") 
    Generate_PRO_INV_Frame_Var = Generate_PRO_INV_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_INV_Frame_Var.configure(variable=Generate_PRO_INV_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRO_INV_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "Use"], Information=Generate_PRO_INV_Variable))

    # Field - Use Invoice PDF
    Generate_PRO_INV_PDF_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, Frame=Tab_PRO, Field_Frame_Type="Half_size" , Label="Invoice .pdf", Field_Type="Input_CheckBox") 
    Generate_PRO_INV_PDF_Frame_Var = Generate_PRO_INV_PDF_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Generate_PRO_INV_PDF_Frame_Var.configure(variable=Generate_PRO_INV_PDF_Variable, text="", command=lambda : Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=Generate_PRO_INV_PDF_Variable, File_Name="Settings", JSON_path=["0", "HQ_Data_Handler", "Invoice", "Credit_Memo", "PDF", "Generate"], Information=Generate_PRO_INV_PDF_Variable))

    # Button - Generate Purchase Return Orders
    Button_Generate_PRO = Elements.Get_Button(Configuration=Configuration, Frame=Tab_PRO, Button_Size="Normal")
    Button_Generate_PRO.configure(text="Generate", command = lambda:Generate_Purchase_Return_Orders())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Generate_PRO, message="Generate marked documents for selected PROs.", ToolTip_Size="Normal")


    # Build look of Widget
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Download_Sub_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    NUS_Version_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    NUS_Version_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    Environment_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Environment_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    NOC_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    NOC_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)
    Button_Download_Company.pack(side="left", fill="none", expand=False, padx=(5, 5), pady=5)
    Companies_Text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Companies_Frame.pack(side="left", fill="none", expand=False, padx=(0, 5), pady=5)

    Progress_text.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)
    Progress_Bar.pack(side="left", fill="none", expand=False, padx=(5, 0), pady=5)

    TabView_PO.grid(row=1, column=0, padx=5, pady=0, sticky="n")
    Generate_Conf_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PREA_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_CPDI_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_DEL_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_IAL_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Generate_PO.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    
    TabView_BB.grid(row=1, column=1, padx=5, pady=0, sticky="n")
    Generate_BB_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_BB_INV_PDF_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Generate_BB.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    TabView_PRO.grid(row=1, column=2, padx=5, pady=0, sticky="n")
    Generate_PRO_Conf_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PRO_INV_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Generate_PRO_INV_PDF_Frame.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Button_Generate_PRO.pack(side="top", fill="none", expand=False, padx=5, pady=5)