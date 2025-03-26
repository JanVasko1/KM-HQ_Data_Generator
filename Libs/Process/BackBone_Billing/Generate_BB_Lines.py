# Import Libraries
import random
from pandas import DataFrame, Series
from fastapi import HTTPException

import Libs.Defaults_Lists as Defaults_Lists
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups

from customtkinter import CTk, CTkFrame, StringVar

def Generate_BB_Lines(Settings: dict, 
                      Configuration: dict|None, 
                      window: CTk|None, 
                      Vendor_Service_Function_df: DataFrame,
                      Plants_df: DataFrame,
                      Country_ISO_Code_list: list,
                      Tariff_Number_list: list,
                      BB_Number: str, 
                      BB_Order_ID: str, 
                      BB_supplier_order_id: str,
                      BB_Order_Date: str,
                      GUI: bool=True) -> list:
    # --------------------------------------------- Defaults --------------------------------------------- #
    Can_Continue = True
    Lines_df = DataFrame(columns=["line_item_id", "supplier_aid", "description_short", "quantity", "order_unit", "price_amount", "price_line_amount", "order_id", "order_date", "supplier_order_id", "supplier_order_item_id", "delivery_note_id", "tariff_number", "origin", "plant"])
    
    BB_Items_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Method"]
    BB_Fixed_Items = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Items"]["Fixed_Options"]["Fix_Item"]

    BB_Quantity_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Quantity"]["Method"]

    BB_Price_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Method"]
    BB_Fixed_Price = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Prices"]["Fixed_Options"]["Fix_Price"]

    BB_Inv_Plant_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Method"]
    BB_Inv_Fixed_Plant = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Fixed_Options"]["Fixed_Plant"]
    
    BB_Count_Origin_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Method"]
    BB_Fixed_Count_Origin = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Country_Of_Origin"]["Fixed_Options"]["Fix_Country_Of_Origin"]

    BB_Tariff_Method = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Method"]
    BB_Fixed_Tariff = Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Tariff"]["Fixed_Options"]["Fix_Tariff"]

    # --------------------------------------------- Items --------------------------------------------- #
    if Can_Continue == True:
        if BB_Items_Method == "Fixed":
            Lines_df["supplier_aid"] = [BB_Fixed_Items]
        elif BB_Items_Method == "All":
            Items_List = Vendor_Service_Function_df["Vendor_Service_ID"].to_list()
            Items_Description_List = Vendor_Service_Function_df["Vendor_Service_Name"].to_list()
            Lines_df["supplier_aid"] = Items_List
            Lines_df["description_short"] = Items_Description_List
        elif BB_Items_Method == "Prompt":
            if GUI == True:
                def Select_BB_Items(Frame_Body: CTkFrame, Lines_No: int):
                    Items_List = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkCheck = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkcheckbox"]
                        Value_CTkCheck_Value = Value_CTkCheck.get()
                        if Value_CTkCheck_Value == True:
                            Selected_Item_No_label = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe"].children["!ctklabel"]
                            Selected_Item_No = str(Selected_Item_No_label.cget("text"))
                            Selected_Item_No = Selected_Item_No.replace(":", "")
                            Items_List.append(Selected_Item_No)
                        else:
                            pass
                    Lines_df["supplier_aid"] = Items_List
                    BB_Items_Variable.set(value="Selected")
                    BB_Item_Window.destroy()

                # TopUp Window
                BB_Items_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Items_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Items_Window_geometry[1] //2
                BB_Item_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Service ID.", max_width=BB_Items_Window_geometry[0], max_height=BB_Items_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=BB_Item_Window, Name="Select BackBone Billing Service ID.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select Service ID of BackBone Billing Invoice.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Vendor_Service_ID
                Lines_No = len(Vendor_Service_Function_df)
                for row in Vendor_Service_Function_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["Vendor_Service_ID"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_CheckBox") 
                    Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
                    Fields_Frame_Var.configure(text="")

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > BB_Items_Window_geometry [1]:
                    content_height = BB_Items_Window_geometry [1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                BB_Items_Variable = StringVar(master=BB_Item_Window, value="", name="BB_Items_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Items(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Service ID selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(BB_Items_Variable)

                # Items Description
                for row in Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]
                    result = Vendor_Service_Function_df.loc[Vendor_Service_Function_df["Vendor_Service_ID"] == Item_No, "Vendor_Service_Name"].values[0]
                    Lines_df.at[row[0], "description_short"] = result
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_BB_Lines:Items_Selection")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items Method selected: {BB_Items_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items Method selected: {BB_Items_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass
    
    # Number of Lines in Document
    Lines_No = len(Lines_df)

    # --------------------------------------------- Quantity --------------------------------------------- #
    if Can_Continue == True:
        if BB_Quantity_Method == "One":
            Lines_df["quantity"] = 1
        elif BB_Quantity_Method == "Prompt":
            if GUI == True:
                def Select_BB_Quantity(Frame_Body: CTkFrame, Lines_No: int):
                    Quantity_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkentry"]
                        try:
                            Value_Quantity = int(Value_CTkEntry.get())
                        except:
                            Value_Quantity = 0
                        Quantity_list.append(Value_Quantity)

                    Lines_df["quantity"] = Quantity_list
                    BB_Quantity_Variable.set(value="Selected")
                    BB_Quantity_Window.destroy()

                # TopUp Window
                BB_Quantity_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Quantity_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Quantity_Window_geometry[1] //2
                BB_Quantity_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Qty for selected Items.", max_width=BB_Quantity_Window_geometry[0], max_height=BB_Quantity_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=BB_Quantity_Window, Name="Select BackBone Billing Qty for selected Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Qty for each Item of BackBone Billing Invoice.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Quantities
                for row in Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal", Validation="Integer") 
                    BB_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    BB_Fields_Frame_Var.configure(placeholder_text="Manual Quantity", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > BB_Quantity_Window_geometry[1]:
                    content_height = BB_Quantity_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                BB_Quantity_Variable = StringVar(master=BB_Quantity_Window, value="", name="BB_Quantity_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Quantity(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Quantity selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(BB_Quantity_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_BB_Lines:Quantity")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items quantity Method selected: {BB_Quantity_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items quantity Method selected: {BB_Quantity_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Price --------------------------------------------- #
    if Can_Continue == True:
        if BB_Price_Method == "Fixed":
            Lines_df["price_amount"] = BB_Fixed_Price
        elif BB_Price_Method == "Prompt":
            if GUI == True:
                def Select_BB_Price(Frame_Body: CTkFrame, Lines_No: int):
                    Price_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkentry"]
                        try:
                            Value_Price = float(Value_CTkEntry.get())
                        except:
                            Value_Price = 0
                        Value_Price = round(number=Value_Price, ndigits=2)
                        Price_list.append(Value_Price)

                    Lines_df["price_amount"] = Price_list
                    BB_Price_Variable.set(value="Selected")
                    BB_Price_Window.destroy()
                
                # TopUp Window
                BB_Price_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Price_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Price_Window_geometry[1] //2
                BB_Price_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Price for selected Items.", max_width=BB_Price_Window_geometry[0], max_height=BB_Price_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=BB_Price_Window, Name="Select BackBone Billing Price for selected Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Price for each Item of BackBone Billing Invoice.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Prices
                for row in Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_Normal", Validation="Float") 
                    BB_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkentry"]
                    BB_Fields_Frame_Var.configure(placeholder_text="Manual Price", placeholder_text_color="#949A9F")
                    
                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > BB_Price_Window_geometry[1]:
                    content_height = BB_Price_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                BB_Price_Variable = StringVar(master=BB_Price_Window, value="", name="BB_Price_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Price(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Price selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(BB_Price_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_BB_Lines:Prices")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Items price Method selected: {BB_Price_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Items price Method selected: {BB_Price_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Price Line Amount --------------------------------------------- #
    Lines_df["price_line_amount"] = Lines_df["quantity"]*Lines_df["price_amount"]

    Total_Line_Amount = float(Lines_df["price_line_amount"].sum(axis=0))

    # --------------------------------------------- Plants --------------------------------------------- #
    if Can_Continue == True:
        if BB_Inv_Plant_Method == "Fixed":
            Lines_df["plant"] = BB_Inv_Fixed_Plant
        elif BB_Inv_Plant_Method == "Random":
            Plants_List = Plants_df["Code"].to_list()
            Lines_df["plant"] = Lines_df.apply(lambda row: random.choice(Plants_List), axis=1)
        elif BB_Inv_Plant_Method == "Empty":
            Lines_df["plant"] = ""
        elif BB_Inv_Plant_Method == "Prompt":
            if GUI == True:
                BB_Inv_Fixed_Plants_List = list(Settings["0"]["HQ_Data_Handler"]["Invoice"]["BackBone_Billing"]["Plants"]["Fixed_Options"]["Plants_List"])
                def Select_BB_Plant(Frame_Body: CTkFrame, Lines_No: int):
                    Plant_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkoptionmenu"]
                        try:
                            Value_Plant = Value_CTkEntry.get()
                        except:
                            Value_Plant = "1000"
                        Plant_list.append(Value_Plant)

                    Lines_df["plant"] = Plant_list
                    BB_Plant_Variable.set(value="Selected")
                    BB_Plant_Window.destroy()
                
                # TopUp Window
                BB_Plant_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Plant_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Plant_Window_geometry[1] //2
                BB_Plant_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Plant for selected Items.", max_width=BB_Plant_Window_geometry[0], max_height=BB_Plant_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=BB_Plant_Window, Name="Select BackBone Billing Plant for selected Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Plant for each Item of BackBone Billing Invoice.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Plants
                for row in Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    BB_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Fields_Frame_Var, values=BB_Inv_Fixed_Plants_List, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > BB_Plant_Window_geometry[1]:
                    content_height = BB_Plant_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                BB_Plant_Variable = StringVar(master=BB_Plant_Window, value="", name="BB_Plant_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Plant(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Plant selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(BB_Plant_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_BB_Lines:Plants")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Plants Method selected: {BB_Inv_Plant_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Plants Method selected: {BB_Inv_Plant_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Country of Origin --------------------------------------------- #
    if Can_Continue == True:
        if BB_Count_Origin_Method == "Fixed":
            Lines_df["origin"] = BB_Fixed_Count_Origin
        elif BB_Count_Origin_Method == "Random":
            Lines_df["origin"] = Lines_df.apply(lambda row: random.choice(Country_ISO_Code_list), axis=1)
        elif BB_Count_Origin_Method == "Empty":
            Lines_df["origin"] = ""
        elif BB_Count_Origin_Method == "Prompt":
            if GUI == True:
                def Select_BB_Country_Origin(Frame_Body: CTkFrame, Lines_No: int):
                    Country_Origin_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkoptionmenu"]
                        try:
                            Value_Country_Origin = Value_CTkEntry.get()
                        except:
                            Value_Country_Origin = "JP"
                        Country_Origin_list.append(Value_Country_Origin)

                    Lines_df["origin"] = Country_Origin_list
                    BB_Country_Origin_Variable.set(value="Selected")
                    BB_Country_Origin_Window.destroy()

                # TopUp Window
                BB_Country_Origin_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Country_Origin_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Country_Origin_Window_geometry[1] //2
                BB_Country_Origin_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Country of Origin  for selected Items.", max_width=BB_Country_Origin_Window_geometry[0], max_height=BB_Country_Origin_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=BB_Country_Origin_Window, Name="Select BackBone Billing Country of Origin  for selected Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Country for each Item of BackBone Billing Invoice.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Country of Origin
                for row in Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    BB_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Fields_Frame_Var, values=Country_ISO_Code_list, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > BB_Country_Origin_Window_geometry[1]:
                    content_height = BB_Country_Origin_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                BB_Country_Origin_Variable = StringVar(master=BB_Country_Origin_Window, value="", name="BB_Country_Origin_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Country_Origin(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Country of Origin selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(BB_Country_Origin_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_BB_Lines:Country_of_Origin")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Country of Origin Method selected: {BB_Count_Origin_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Country of Origin Method selected: {BB_Count_Origin_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Tariff --------------------------------------------- #
    if Can_Continue == True:
        if BB_Tariff_Method == "Fixed":
            Lines_df["tariff_number"] = BB_Fixed_Tariff
        elif BB_Tariff_Method == "Random":
            Lines_df["tariff_number"] = Lines_df.apply(lambda row: random.choice(Tariff_Number_list), axis=1)
        elif BB_Tariff_Method == "Empty":
            Lines_df["tariff_number"] = ""
        elif BB_Tariff_Method == "Prompt":
            if GUI == True:
                def Select_BB_Tariff(Frame_Body: CTkFrame, Lines_No: int):
                    Tariff_list = []
                    for i in range(0, Lines_No + 1):
                        if i == 0:
                            i = ""
                        elif i == 1:
                            continue
                        else:
                            pass
                        
                        Value_CTkEntry = Frame_Body.children[f"!ctkframe{i}"].children["!ctkframe3"].children["!ctkoptionmenu"]
                        try:
                            Value_Tariff = Value_CTkEntry.get()
                        except:
                            Value_Tariff = ""
                        Tariff_list.append(Value_Tariff)

                    Lines_df["tariff_number"] = Tariff_list
                    BB_Tariff_Variable.set(value="Selected")
                    BB_Tariff_Window.destroy()

                # TopUp Window
                BB_Tariff_Window_geometry = (520, 500)
                Main_Window_Centre = CustomTkinter_Functions.Get_coordinate_Main_Window(Main_Window=window)
                Main_Window_Centre[0] = Main_Window_Centre[0] - BB_Tariff_Window_geometry[0] //2
                Main_Window_Centre[1] = Main_Window_Centre[1] - BB_Tariff_Window_geometry[1] //2
                BB_Tariff_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Select BackBone Billing Tariff  for selected Items.", max_width=BB_Tariff_Window_geometry[0], max_height=BB_Tariff_Window_geometry[1], Top_middle_point=Main_Window_Centre, Fixed=True, Always_on_Top=True)

                # Frame - General
                Frame_Main = Elements_Groups.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=BB_Tariff_Window, Name="Select BackBone Billing Tariff  for selected Items.", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="To select proper Qty for each Item of BackBone Billing Invoice.", GUI_Level_ID=3)
                Frame_Body = Frame_Main.children["!ctkframe2"]

                # Tariff
                for row in Lines_df.iterrows():
                    # Dataframe
                    row_Series = Series(row[1])
                    Item_No = row_Series["supplier_aid"]

                    # Fields
                    Fields_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label=f"{Item_No}", Field_Type="Input_OptionMenu") 
                    BB_Fields_Frame_Var = Fields_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
                    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=BB_Fields_Frame_Var, values=Tariff_Number_list, command=None, GUI_Level_ID=3)

                # Dynamic Content height
                content_row_count = len(Frame_Body.winfo_children())
                content_height = content_row_count * 35 + 30 + 50    # Lines multiplied + button + Header if needed (50)
                if content_height > BB_Tariff_Window_geometry[1]:
                    content_height = BB_Tariff_Window_geometry[1]
                Frame_Main.configure(bg_color = "#000001", height=content_height)

                # Buttons
                BB_Tariff_Variable = StringVar(master=BB_Tariff_Window, value="", name="BB_Tariff_Variable")
                Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
                Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
                Button_Confirm_Var.configure(text="Confirm", command = lambda: Select_BB_Tariff(Frame_Body=Frame_Body, Lines_No=Lines_No))
                Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm BB Tariff selection.", ToolTip_Size="Normal", GUI_Level_ID=3)   
                Button_Confirm_Var.wait_variable(BB_Tariff_Variable)
            else:
                raise HTTPException(status_code=500, detail=f"Any Prompt method is not allowed in API calls. Issue in Generate_BB_Lines:Tariff")
        else:
            if GUI == True:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Tariff Method selected: {BB_Tariff_Method} which is not supporter. Cancel File creation.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                raise HTTPException(status_code=500, detail=f"Tariff Method selected: {BB_Tariff_Method} which is not supporter. Cancel File creation.")
            Can_Continue = False
    else:
        pass

    # --------------------------------------------- Apply Header information --------------------------------------------- #
    Lines_df["supplier_order_id"] = BB_supplier_order_id
    Lines_df["delivery_note_id"] = BB_Number
    Lines_df["order_id"] = BB_Order_ID
    Lines_df["order_date"] = BB_Order_Date

    # --------------------------------------------- Apply Lines functions --------------------------------------------- #
    # line_item_id
    line_item_id_list= []
    for i in range(1, Lines_No + 1):
        line_item_id = i * 10
        line_item_id_list.append((f"{line_item_id :06d}"))
    Lines_df["line_item_id"] = line_item_id_list
    Lines_df["supplier_order_item_id"] = line_item_id_list

    # Prepare Json for each line of DataFrame
    BB_Invoice_Lines = []
    for row in Lines_df.iterrows():
        row_Series = Series(row[1])
        Current_line_json = Defaults_Lists.Load_Template(NUS_Version="NUS_Cloud", Template="BB_Invoice_Line")

        # Assign Values
        Current_line_json["line_item_id"] = row_Series["line_item_id"]
        Current_line_json["article_id"]["supplier_aid"] = row_Series["supplier_aid"]
        Current_line_json["article_id"]["description_short"] = row_Series["description_short"]

        Current_line_json["quantity"] = row_Series["quantity"]
        Current_line_json["order_unit"] = "C62"

        Current_line_json["article_price"]["price_amount"] = row_Series["price_amount"]
        Current_line_json["article_price"]["price_line_amount"] = row_Series["price_line_amount"]

        Current_line_json["order_reference"]["order_id"] = row_Series["order_id"]
        Current_line_json["order_reference"]["line_item_id"] = row_Series["line_item_id"]
        Current_line_json["order_reference"]["order_date"] = row_Series["order_date"]

        Current_line_json["supplier_order_reference"]["supplier_order_id"] = row_Series["supplier_order_id"]
        Current_line_json["supplier_order_reference"]["supplier_order_item_id"] = row_Series["supplier_order_item_id"]

        Current_line_json["delivery_reference"]["delivery_note_id"] = row_Series["delivery_note_id"]
        Current_line_json["delivery_reference"]["line_item_id"] = row_Series["line_item_id"]

        Current_line_json["tariff_number"] = row_Series["tariff_number"]

        Current_line_json["remarks"]["origin"] = row_Series["origin"]
        Current_line_json["remarks"]["plant"] = row_Series["plant"]

        BB_Invoice_Lines.append(Current_line_json)
        del Current_line_json

    # --------------------------------------------- PDF Table_Data --------------------------------------------- #
    Table_Data = []
    Table_Data.append(["Item No", "Description", "Quantity", "Price", "Line Amount"])
    for row in Lines_df.iterrows():
        row_Series = Series(row[1])
        Line_Data_List = []
        Line_Data_List.append(str(row_Series["supplier_aid"]))
        Line_Data_List.append(str(row_Series["description_short"]))
        Line_Data_List.append(str(row_Series["quantity"]))
        Line_Data_List.append(str(row_Series["price_amount"]))
        Line_Data_List.append(str(row_Series["price_line_amount"]))
        Table_Data.append(Line_Data_List)
  
    return BB_Invoice_Lines, Lines_No, Total_Line_Amount, Table_Data