import azure.functions as func

from pydantic import BaseModel
import json

from Libs.Azure.API_Error_Handler import APIError
import Libs.Data_Functions as Data_Functions
import Libs.File_Manipulation as File_Manipulation
import Libs.Downloader.Downloader as Downloader

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

# Return Models
class Templates_list(BaseModel):
    Templates: list

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Get templates list
@app.function_name(name="active-templates")
@app.route("v1/list/active-templates/", methods=["GET"])
async def Get_Template_list(req: func.HttpRequest) -> func.HttpResponse:
    Allowed_Area = ["PO", "PRO", "BB"]
    try:
        req_body = req.get_json()
        Area = req_body.get('Area')
        # process area...
    except Exception as Error:
        raise APIError(message=f"Error: {str(Error)}", status_code=400, charset="utf-8")
    
    try:
        if Area in Allowed_Area:
            files = File_Manipulation.Get_All_Files_Names(file_path=Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Templates\\{str(Area)}"))
            Return_files = Templates_list(Templates=files)
            return func.HttpResponse(body=Return_files.json(), mimetype="application/json", status_code=200)
        else:
            raise APIError(message="Area is not Allowed.", status_code=400, charset="utf-8")
        
    except APIError as Error:
        return func.HttpResponse(body=json.dumps({"error": Error.message}), status_code=Error.status_code, mimetype="application/json", charset=Error.charset)

    except Exception as Error:
        return func.HttpResponse(body=json.dumps({"error": "Internal Server Error"}), status_code=500, mimetype="application/json", charset="utf-8")



# Purchase Order
@app.function_name(name="purchase-order")
@app.route("v1/create-doc/purchase-order/", methods=["POST"])
async def Generate_Purchase_Order(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        Request_PO = PurchaseOrder(**body)
        # Now you can use po.client_id, po.Company, etc.
    except Exception as Error:
        raise APIError(message=f"Error: {str(Error)}", status_code=400, charset="utf-8")

    if Request_PO.Environment == "PRD":
        raise APIError(message="Testing on PRD environment strictly forbidden.", status_code=405, charset="utf-8")
    else:
        try:
            # Load selected Template to Settings
            File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
            Settings = json.load(fp=File)
            try:
                Template_path = Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Templates\\PO\\{Request_PO.Template}.json")
            except:
                raise APIError(message=f"Template: {Request_PO.Template} not found.", status_code=405, charset="utf-8")
            Template_path_list = [Template_path]
            try:
                Data_Functions.Import_Data(Settings=Settings, Configuration=None, window=None, import_file_path=Template_path_list, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")
            except:
                raise APIError(message=f"Template: {Request_PO.Template} is not applicable.", status_code=405, charset="utf-8")

            # Update Settings to upload file to server instantly
            Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"] = True

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

            return func.HttpResponse(body=json.dumps({"success": "All files for selected Purchase Order/s created."}), mimetype="application/json", status_code=200)
        
        except APIError as Error:
            return func.HttpResponse(body=json.dumps({"error": Error.message}), status_code=Error.status_code, mimetype="application/json", charset=Error.charset)

        except Exception as Error:
            return func.HttpResponse(body=json.dumps({"error": "Internal Server Error"}), status_code=500, mimetype="application/json", charset="utf-8")



# BB Invoice
@app.function_name(name="bb-invoice")
@app.route("v1/create-doc/bb-invoice/", methods=["POST"])
async def Generate_BB_Invoice(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        Request_BB_INV = BBInvoice(**body)
        # Now you can use po.client_id, po.Company, etc.
    except Exception as Error:
        raise APIError(message=f"Error: {str(Error)}", status_code=400, charset="utf-8")

    if Request_BB_INV.Environment == "PRD":
        raise APIError(message="Testing on PRD environment strictly forbidden.", status_code=405, charset="utf-8")
    else:
        try:
            # Load selected Template to Settings
            File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
            Settings = json.load(fp=File)
            try:
                Template_path = Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Templates\\BB\\{Request_BB_INV.Template}.json")
            except:
                raise APIError(message=f"Template: {Request_BB_INV.Template} not found.", status_code=405, charset="utf-8")
            Template_path_list = [Template_path]
            try:
                Data_Functions.Import_Data(Settings=Settings, Configuration=None, window=None, import_file_path=Template_path_list, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")
            except:
                raise APIError(message=f"Template: {Request_BB_INV.Template} is not applicable.", status_code=405, charset="utf-8")

            # Update Settings to upload file to server instantly
            Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"] = True

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

            return func.HttpResponse(body=json.dumps({"success": "All files for BackBoneBilling Invoice created."}), mimetype="application/json", status_code=200)
        
        except APIError as Error:
            return func.HttpResponse(body=json.dumps({"error": Error.message}), status_code=Error.status_code, mimetype="application/json", charset=Error.charset)

        except Exception as Error:
            return func.HttpResponse(body=json.dumps({"error": "Internal Server Error"}), status_code=500, mimetype="application/json", charset="utf-8")



# Purchase Return Order
@app.function_name(name="purchase-return-order")
@app.route("v1/create-doc/purchase-return-order/", methods=["POST"])
async def Generate_Purchase_Return_Order(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        Request_PRO = PurchaseReturnOrder(**body)
        # Now you can use po.client_id, po.Company, etc.
    except Exception as Error:
        raise APIError(message=f"Error: {str(Error)}", status_code=400, charset="utf-8")

    if Request_PRO.Environment == "PRD":
        raise APIError(message="Testing on PRD environment strictly forbidden.", status_code=405, charset="utf-8")
    else:
        try:
            # Load selected Template to Settings
            File = open(file=Data_Functions.Absolute_path(relative_path=f"Libs\\Settings.json"), mode="r", encoding="UTF-8", errors="ignore")
            Settings = json.load(fp=File)
            try:
                Template_path = Data_Functions.Absolute_path(relative_path=f"Libs\\Azure\\Templates\\PRO\\{Request_PRO.Template}.json")
            except:
                raise APIError(message=f"Template: {Request_PRO.Template} not found.", status_code=405, charset="utf-8")
            Template_path_list = [Template_path]
            try:
                Data_Functions.Import_Data(Settings=Settings, Configuration=None, window=None, import_file_path=Template_path_list, Import_Type="Template", JSON_path=["0", "HQ_Data_Handler"], Method="Overwrite")
            except:
                raise APIError(message=f"Template: {Request_PRO.Template} is not applicable.", status_code=405, charset="utf-8")

            # Update Settings to upload file to server instantly
            Settings["0"]["HQ_Data_Handler"]["Export"]["Download_Folder"] = True

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

            return func.HttpResponse(body=json.dumps({"success": "All files for selected Purchase Return Order/s created."}), mimetype="application/json", status_code=200)
        
        except APIError as Error:
            return func.HttpResponse(body=json.dumps({"error": Error.message}), status_code=Error.status_code, mimetype="application/json", charset=Error.charset)

        except Exception as Error:
            return func.HttpResponse(body=json.dumps({"error": "Internal Server Error"}), status_code=500, mimetype="application/json", charset="utf-8")
