from fastapi import FastAPI
from pydantic import BaseModel
import json

import Libs.Data_Functions as Data_Functions
import Libs.Defaults_Lists as Defaults_Lists
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

# TODO --> API --> ErrorHandler
# TODO --> API --> Response structure


# Purchase Order
@app.post("/v1/data/global/purchase-order/")
async def Generate_Purchase_Order(Request_PO: PurchaseOrder):
    if Request_PO.Environment == "PRD":
        # TODO --> API vrátit chybu
        pass
    else:
        # Load selected Template to Settings
        File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\{Request_PO.Template}.json"), mode="r", encoding="UTF-8", errors="ignore")
        Settings = json.load(fp=File)

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
@app.post("/v1/data/global/bb-invoice/")
async def Generate_BB_Invoice(Request_BB_INV: BBInvoice):
    if Request_BB_INV.Environment == "PRD":
        # TODO --> API vrátit chybu
        pass
    else:
        # Load selected Template to Settings
        File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\{Request_BB_INV.Template}.json"), mode="r", encoding="UTF-8", errors="ignore")
        Settings = json.load(fp=File)

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
@app.post("/v1/data/global/purchase-return-order/")
async def Generate_Purchase_Return_Order(Request_PRO: PurchaseReturnOrder):
    if Request_PRO.Environment == "PRD":
        # TODO --> API vrátit chybu
        pass
    else:
    # Load selected Template to Settings
        File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\API\\Templates\\{Request_PRO.Template}.json"), mode="r", encoding="UTF-8", errors="ignore")
        Settings = json.load(fp=File)

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