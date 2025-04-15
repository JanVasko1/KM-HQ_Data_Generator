from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

import Libs.Data_Functions as Data_Functions
import Libs.File_Manipulation as File_Manipulation
import Libs.Downloader.Downloader as Downloader

app = FastAPI()

# -------------------------------------------------------------------------- Base Models -------------------------------------------------------------------------- #
class PurchaseOrder(BaseModel):
    client_id: str
    client_secret: str
    tenant_id: str
    NUS_version: str
    NOC: str
    Environment: str
    Company: str
    Template: str
    Purchase_Order_list: list

class BBInvoice(BaseModel):
    client_id: str
    client_secret: str
    tenant_id: str
    NUS_version: str
    NOC: str
    Environment: str
    Company: str
    Template: str
    Buy_from_Vendor_No: str

class PurchaseReturnOrder(BaseModel):
    client_id: str
    client_secret: str
    tenant_id: str
    NUS_version: str
    NOC: str
    Environment: str
    Company: str
    Template: str
    Purchase_Return_Orders_List: list

class NewTemplate(BaseModel):
    Template_Name: str
    Content: dict

# Return Models
class Templates_list(BaseModel):
    Templates: list

# Get templates list
@app.get("/v1/list/active-templates/")
async def Generate_Purchase_Order(Area: str) -> Templates_list:
    Allowed_Area = ["PO", "PRO", "BB"]
    if Area in Allowed_Area:
        files = File_Manipulation.Get_All_Files_Names(file_path=Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\{str(Area)}"))
        Return_files = Templates_list(Templates=files)
        return Return_files
    else:
        raise HTTPException(status_code=400, detail="Area is not Allowed.") 

# Upload new template
@app.put("/v1/upload/new-templates/")
async def Generate_Purchase_Order(Template: NewTemplate):
    try:
        with open(Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\{Template.Template_Name}"), "w") as outfile: 
            json.dump(Template.Content, outfile)
        return True
    except:
        raise HTTPException(status_code=500, detail="Not possible to upload Template.") 

# Purchase Order
@app.post("/v1/create-doc/purchase-order/")
async def Generate_Purchase_Order(Request_PO: PurchaseOrder):
    if Request_PO.Environment == "PRD":
        raise HTTPException(status_code=405, detail="Testing on PRD environment strictly forbidden.")
    else:
        # Load selected Template to Settings
        File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
        Settings = json.load(fp=File)
        try:
            Template_path = Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\PO\\{Request_PO.Template}.json")
        except:
            raise HTTPException(status_code=405, detail=f"Template: {Request_PO.Template} not found.")
        Template_path_list = [Template_path]
        Data_Functions.Import_Data(Settings=Settings, Configuration=None, window=None, import_file_path=Template_path_list, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")

        # Process Data
        Downloader.Download_Data_Purchase_Orders(Settings=Settings, 
                                                Configuration=None, 
                                                window=None, 
                                                Progress_Bar=None, 
                                                NUS_version=Request_PO.NUS_version, 
                                                NOC=Request_PO.NOC, 
                                                Environment=Request_PO.Environment, 
                                                Company=Request_PO.Company, 
                                                Purchase_Order_list=Request_PO.Purchase_Order_list,
                                                client_id=Request_PO.client_id,
                                                client_secret=Request_PO.client_secret,
                                                tenant_id=Request_PO.tenant_id,
                                                GUI=False)

        return True

# BB Invoice
@app.post("/v1/create-doc/bb-invoice/")
async def Generate_BB_Invoice(Request_BB_INV: BBInvoice):
    if Request_BB_INV.Environment == "PRD":
        raise HTTPException(status_code=405, detail="Testing on PRD environment strictly forbidden.")
    else:
        # Load selected Template to Settings
        File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
        Settings = json.load(fp=File)
        try:
            Template_path = Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\BB\\{Request_BB_INV.Template}.json")
        except:
            raise HTTPException(status_code=405, detail=f"Template: {Request_BB_INV.Template} not found.")
        Template_path_list = [Template_path]
        Data_Functions.Import_Data(Settings=Settings, Configuration=None, window=None, import_file_path=Template_path_list, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")

        # Process Data
        Downloader.Download_Data_BackBoneBilling(Settings=Settings, 
                                                Configuration=None, 
                                                window=None, 
                                                Progress_Bar=None, 
                                                NUS_version=Request_BB_INV.NUS_version, 
                                                NOC=Request_BB_INV.NOC, 
                                                Environment=Request_BB_INV.Environment, 
                                                Company=Request_BB_INV.Company, 
                                                Buy_from_Vendor_No=Request_BB_INV.Buy_from_Vendor_No,
                                                client_id=Request_BB_INV.client_id,
                                                client_secret=Request_BB_INV.client_secret,
                                                tenant_id=Request_BB_INV.tenant_id,
                                                GUI=False)

        return True

# Purchase Return Order
@app.post("/v1/create-doc/purchase-return-order/")
async def Generate_Purchase_Return_Order(Request_PRO: PurchaseReturnOrder):
    if Request_PRO.Environment == "PRD":
        raise HTTPException(status_code=405, detail="Testing on PRD environment strictly forbidden.")
    else:
    # Load selected Template to Settings
        File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
        Settings = json.load(fp=File)
        try:
            Template_path = Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\PRO\\{Request_PRO.Template}.json")
        except:
            raise HTTPException(status_code=405, detail=f"Template: {Request_PRO.Template} not found.")
        Template_path_list = [Template_path]
        Data_Functions.Import_Data(Settings=Settings, Configuration=None, window=None, import_file_path=Template_path_list, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")

        # Process Data
        Downloader.Download_Data_Purchase_Orders(Settings=Settings, 
                                                Configuration=None, 
                                                window=None, 
                                                Progress_Bar=None, 
                                                NUS_version=Request_PRO.NUS_version, 
                                                NOC=Request_PRO.NOC, 
                                                Environment=Request_PRO.Environment, 
                                                Company=Request_PRO.Company, 
                                                Purchase_Return_Orders_List=Request_PRO.Purchase_Return_Orders_List,
                                                client_id=Request_PRO.client_id,
                                                client_secret=Request_PRO.client_secret,
                                                tenant_id=Request_PRO.tenant_id,
                                                GUI=False)

        return True