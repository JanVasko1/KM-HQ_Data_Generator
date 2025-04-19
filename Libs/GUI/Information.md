# <u>HQ Data Generator</u>
## <u>General Information</u>
- Save value is done by existing field entry field
- Random methods usually create interval and then randomly pick from interval
- numbers and dates Entry Fields always check proper format
- Fields are available from editing only when needed (defined method is selected)

# <u>Header</u>
- display status of Connection (Authorization) right after program start (top right circle)
- display status of Exports folders (bottom right circle) - can be changed in Settings/Authorization widget
- Theme change
- Application version list
- **Templates**
    * Save Template - save current settings under name (can be recall later)
    * Actual Template - shows actual template used 
    * Export All Templates - function will export all templates to "Download folder", from which templates can be shared with others
    * Import Templates - Function to import one / multiple templates at once (Drag&Drop)
    * Delete Templates - Function to delete templates from my list of Templates

# <u>Side Bar</u>
- KM logo
- used for orientation in the program (pages select)
- drag&move, program can be moved only from this area
- version 

# <u>Setup Pages</u>
## <u>Download</u>
- page designed for connection to NAV / Business Central and download and process data according to setup
### Connect
- connection the desired NAV / Business Central is done through top bar on the page (not Header)
- you have to select all parts of connection string and confirm by  **Get Companies**:
    1. NUS Version
    2. Environment
    3. NOC
- Company list is updated and you can select it in the right dropdown button 
- after selection of Company 2 additional information are automatically downloaded
    * Logistic Process list - is used for as filtering option for multiple Purchase Order select
    * HQ Vendors - is used for selection of Vendor for BackBone Billing Invoice

#### Download and process areas
##### Purchase Order
- contains checkbox fields defining if program will generate document or not
- selection of Purchase Order is done by 2 possible ways 
1. One Purchase Order
- place **1** Purchase Order Number into Field and press button **Generate**
- you have to leave field by "Tabulator" or any other way so PO will be taken into account (as General information describe about Entry field)
2. Multiple POs
- this option can be used for generation one or multiple POs
- here you can pre-filter list of Purchase Order by Logistic Process --> to make list shorter
- in the list you have checkbox next to each Purchase Order, by selecting of one or multiple you confirm your choice and press button **Generate**
##### BackBone Billing
- contains checkbox fields defining if program will generate document or not
- you have to select Vendor from who you expect to receive BackBone Billing Invoice and press button **Generate**
##### Purchase Return Order
- contains checkbox fields defining if program will generate document or not
- you have 2 possibilities how to select desired Purchase Return Order as in Purchase Order, just this option is shrink to fit the size of widget
* **Options**:
    1. One Purchase Return Order
        - place **1** Purchase Return Oder Number into Field and press button **Generate**
        - you have to leave field by "Tabulator" or any other way so PO will be taken into account (as General information describe about Entry field)
    2. Multiple POs
        - in the list you have checkbox next to each Purchase Return Order, by selecting of one or multiple you confirm your choice and press button **Generate**

## <u>Confirmation</u>
### <u>Purchase Order</u>
#### Numbers
- define how program will choose number for Confirmation
1. **Method**
    * Fixed - Uses only one Confirmation Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - Confirmation Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Price and Currency
1. **Price**
    * Price List - Use active price of Item related to the Vendor 
    * Purchase Line - takes Direct unit Cost from Purchase Line
    * Prompt - program request input from user when it is needed
2. **Currency**
    * Fixed - Uses only one Currency selected field "Fixed Currency"
    * Purchase Order - Takes Currency from Purchase Header
3. **Fixed Currency** - Currency for all Confirmations created will be used when **Method** = Fixed

#### Unit of Measure
- always should be used International ISO code for UoM
- Methods **Purchase Line**, **HQ Item Transport Export** always recalculate found Business Central value into ISO Code
1. **Unit of Measure**
    * Fixed - Uses only one UoM selected field "Fixed Unit of Measure"
    * Purchase Line - Takes "Unit of Measure Code" from Purchase line and calculate ISO code according to it
    * HQ Item Transport Export - Takes "Unit of Measure Code" from HQ Item Transport Register, when Vendor Document Type = Export and calculate ISO code according to it
    * Prompt - program request input from user when it is needed
2. **Fixed Unit of Measure** - UoM for all Confirmations created will be used when **Method** = Fixed

#### Generation Date
- Setup which is used to put BEU Confirmation Creation Date
1. **Method**
    * Fixed - Uses only one Date selected field "Fixed Date"
    * Today - Uses only one Today Date
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Date for all Confirmations created will be used when **Method** = Fixed (Date Picker available)

#### Line Flags
- Global setup of Item special treatment related to EndOfLive, Canceled, Substitution, Labels
1. **Use** - Switch which enable Method (doesn't have any influence on Global)
2. **Method**
    * Random Cancel - randomly cancel Item (if Machine is cancelled FOCHs are not put on Confirmation)
    * Random Finished - randomly set Item as End of Life (if Machine is Finished FOCHs are not put on Confirmation)
    * Prompt - program request input from user when it is needed
3. **Label always** - when ON program will put label to all machines (Product Group = 0100)
4. **Finish EOL Item** - when there is Item with "Distribution Group marked as Blocked for Purchase", then program marked that Item as **Finished**. If Machine is Finished FOCHs are not put on Confirmation.
5. **Always Substitute** - when program found that exported Item has substitute in NAV, then uses that substitute

#### Free of Charge - Functionality
- here is description of whole tab for "Free of Charge"
1. **Method**
    * Fixed - program will use information from other widgets **Cable**, **Documentation**, **Face Sheet**, 
    * Connected Items - use connected Items from NAV if they are existing, if not then will not be use any
    * Prompt - program request input from user when it is needed
2. **FOCHs widgets**
    * Number - Use Number available in NAV as this number is used as Item No.
    * Description - Items description
    * Qty per Machine - use as Machine Qty multiplication
    * Price - Unit Cost of FOCH

#### ATP - Functionality
- here is description of whole tab for "ATP"
1. **Use** - Switch which enable Globally ATP functionality
2. **Quantity Method**
    * All On-Hand - set all lines as On Hand, every line has only 1 record of Scheduled Lines
    * All On-Board - set all lines as On Board, every line has only 1 record of Scheduled Lines
    * Line Random - Program randomly pick between "ONH" and "ONB" for each Confirmation line separately, but every time it is for full line Qty
    * Ratio - Every Confirmation line Qty is divided according to ratio between all 3 possible statuses. This method always fill only whole numbers
3. **Date Method**
    * Fixed - set all lines as On Hand, every line has only 1 record of Scheduled Lines
    * Intervals - set all lines as On Board, every line has only 1 record of Scheduled Lines
4. **Quantity Distribution - widget**
    - will be used when **Quantity Method** = Ratio
    - sum of all ratio must be equal 100 (like with percentages)
5. **Fixed Dates - widget**
    - will be used when **Date Method** = Fixed
    * ONH Date - Fixed Date used for "On-Hand" status (depends if is selected by **Quantity Method**)
    * ONB Date - Fixed week number used for "On-Board" status (depends if is selected by **Quantity Method**)
6. **Interval Dates - widget**
    - this setup create date interval for On-Hand and On-Board status only and randomly pick one date from it
    - it is allowed to to use negative numbers to create interval also to the past
    - Date interval works only with working days (keeps Global Dates Interval setup)
    - interval is created based "From - To" method, where both is defined as "Current Date +/- number of days"

### <u>Return Order</u>
#### Numbers
- define how program will choose number for Return Confirmation
1. **Method**
    * Fixed - Uses only one Confirmation Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - Confirmation Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Price and Currency
1. **Price**
    * Price List - Use active price of Item related to the Vendor 
    * Purchase Return Line - takes Direct unit Cost from Purchase Return Line
    * Prompt - program request input from user when it is needed
2. **Currency**
    * Fixed - Uses only one Currency selected field "Fixed Currency"
    * Purchase Return Order - Takes Currency from Purchase Return Header
3. **Fixed Currency** - Currency for all Confirmations created will be used when **Method** = Fixed

#### Unit of Measure
- always should be used International ISO code for UoM
- Methods **Purchase Line**, **HQ Item Transport Export** always recalculate found Business Central value into ISO Code
1. **Unit of Measure**
    * Fixed - Uses only one UoM selected field "Fixed Unit of Measure"
    * Purchase Return Line - Takes "Unit of Measure Code" from Purchase return line and calculate ISO code according to it
    * HQ Item Transport Export - Takes "Unit of Measure Code" from HQ Item Transport Register, when Vendor Document Type = Export and calculate ISO code according to it
    * Prompt - program request input from user when it is needed
2. **Fixed Unit of Measure** - UoM for all Confirmations created will be used when **Method** = Fixed

#### Generation Date
- Setup which is used to put BEU Confirmation Creation Date 
1. **Method**
    * Fixed - Uses only one Date selected field "Fixed Date"
    * Today - Uses only one Today Date
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Date for all Confirmations created will be used when **Method** = Fixed (Date Picker available)

#### Item Rejection
- this is setup used to define which Items to be Confirmed for return and which not
1. **Method**
    * Confirm All - Program will set all Items on Confirmation Canceled = False (can be returned)
    * Reject All - Program will set all Items on Confirmation Canceled = "rejected for parts return" (BEU canceled returns)
    * Random Reject - Program will randomly select count of Items (min = 0, max = sum of all Qty) and set for them Canceled = "rejected for parts return"
    * Ratio - method mark some Items Qty as not returnable according to ratio set in dedicated fields
    * Prompt - program request input from user when it is needed
2. **Ratio Confirmed** - "percentage" of Qty which will be confirmed. Will be used when **Method** = Ratio
3. **Ratio Reject** - "percentage" of Qty which will be rejected. Will be used when **Method** = Ratio

## <u>CPDI</u>
#### Generate
- setup related to the CPDI process only (Should be ON only for Towers where CPDI is requested)
1. **Method - Delivery**
    * Fixed - All CPDI statuses (json generated) will have that Fixed Delivery Number
    * All Deliveries - Program will generate CPDI statuses for all Deliveries found / generated
    * Prompt - program request input from user when it is needed
2. **Fixed Delivery** - Delivery Number for all CPDI, will be used when **Method** = Fixed
3. **Method - Level**
    * Fixed - Fixed Level will be used
    * Purchase Order -  Level will be taken from "Level Requested" from Purchase Order
    * Random - Program will randomly set Level from list of available Levels downloaded from NAV
    * Prompt - program request input from user when it is needed
4. **Fixed Level** - Fixed Level for all CPDI, will be used when **Method** = Fixed
5. **Method - Status**
    * Fixed - Fixed Status will be used
    * All Statuses - Program generates as many files as many statuses is in the NAV (taken from HQ Status table)
    * Prompt - program request input from user when it is needed
6. **Fixed Status** - Fixed Status for all CPDI, will be used when **Method** = Fixed

## <u>PreAdvice</u>
- Program creates PreAdvice always after Delivery (BEU do it opposite)
- as PreAdvice shares with Delivery all features except Dates, program take delivery file and do updates of it
- Serial numbers are always deleted from PreAdvice
#### Delivery Date
1. **Method**
    * Fixed - use fixed date
    * Random - Program will use Interval and randomly pick date from it
    * Delivery Date Shift - Dates on PreAdvice will be shifted by number of days
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Date for Preadvice created will be used when **Method** = Fixed (Date Picker available)
3. **Interval Date - Section**
    - will be used when **Method** = Random
    - this setup create date interval for Delivery Date and randomly pick one date from it
    - it is allowed to to use negative numbers to create interval also to the past
    - Date interval works only with working days (keeps Global Dates Interval setup)
    - interval is created based "From - To" method, where both is defined as "Current Date +/- number of days"
3. **Delivery Date Shift - Section**
    * Delivery date Shift by - number of date which will be used to recalculate "Delivery Date" on Preadvice from "Delivery Date" on Delivery
    * Generation date Shift by - number of date which will be used to recalculate "Generation Date" on Preadvice from "Delivery Date" on Delivery

## <u>Delivery</u>
#### Delivery Count
- define how program will select how many deliveries per Document be created
1. **Method**
    * Fixed - Uses only fixed number of Deliveries per document 
    * Random - Program calculates sum of all Qty of all Items and randomly pick (if pick > maximal count then maximal count is used)
    * Prompt - program request input from user when it is needed
2. **Fixed count** - Fixed number od Deliveries used per Document will be used when **Method** = Fixed
3. **Maximal count** - Used only when Random Pick is over the maximum used when **Method** = Random

#### Numbers
- define how program will choose number for Delivery
1. **Method**
    * Fixed - Uses only one Delivery Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - Delivery Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Item Assignment to Delivery
- Important setup to assing Items and Qty to delivery when more Deliveries per Document created
1. **Method**
    * Full random - Wil randomly put Items and Qty to delivery (means that Exported qty may be slitted per multiple deliveries)
    * Line random - Program will assign full lines Qty to delivery, but lines may be assing randomly
    * Prompt - program request input from user when it is needed (only full lines is possible to assign)
2. **FOCHs with Machines** - This setup overwrite random splitting for Free of Charge and every time put FOCHs and its Qty to the Machine

#### Delivery Date
- Setup which is used to generate "Delivery Date" and others for Delivery
1. **Method**
    * Fixed - Uses only one Date selected field "Fixed Date"
    * Random - Uses only one Today Date
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Fixed Date used for "Delivery Date", will be used when **Method** = Fixed (Date Picker available)
3. **Interval Date - Section**
    - will be used when **Method** = Random
    - this setup create date interval for Delivery Date and randomly pick one date from it
    - it is allowed to to use negative numbers to create interval also to the past
    - Date interval works only with working days (keeps Global Dates Interval setup)
    - interval is created based "From - To" method, where both is defined as "Current Date +/- number of days"

#### Serial Numbers
1. **Generate for all Machines** - Program will create Serial Numbers for all Item of "Material Group = 0100"
2. **Generate for all tracked Items** - Serial numbers be generated for Items which has "Item Tracking Code.SN Purchase Tracking = True" on inbound
3. **SN Number Creation- Section**
    * Prefix - Serial Number Prefix
    * Method:
        * Fixed - Manually selected form Manual Field
        * Item No - Item Number taken as middle part of Serial Number
        * DateTime stamp - Datetime (YYYYYMMDDHHmmss) --> suggested method as cannot create duplicates
    * Manual Middle - manual middle part
    * Suffix - non changeable part as helps to create unique number when "DateTime stamp" method Used

#### Shipment Method
1. **Method**
    * Fixed - Use manually provided Shipment Method
    * Random - Program will randomly pick Shipment Method from list downloaded from NAV
    * Empty - be empty
2. **Fixed Shp. Method** - This Shipment Method will be used when **Method** = Fixed

#### Carrier
1. **Method**
    * Fixed - Use manually provided Carrier ID
    * Random - Program will randomly pick Carrier ID from list downloaded from NAV (Shipping Agents - BEU Carrier ID)
    * Empty - be empty
2. **Fixed Carrier** - This Carrier ID will be used when **Method** = Fixed

#### Bill of Landing
1. **Method**
    * Fixed - Uses only one BOL Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - BOL Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Package Numbers
1. **Method**
    * Fixed - Uses only one Package Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
2. **Fixed Number** - Package Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic
3. **Maximal Package Count** - Maximal number of Packages for one Delivery used when **Method** = Automatic

#### EXIDV2
1. **Method**
    * Fixed - Uses only one EXIDV2 Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Empty - be empty
2. **Fixed Number** - EXIDV2 Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic
3. **Assigned Method**
    * Per Package - EXIDV2 Number will be generated for each Package
    * Per Delivery - EXIDV2 Number will be generated only for Delivery (all Packages will have same)

#### Unit of Measure
1. **Weigh - Section**
    1. **Method**
        * Fixed - Uses only one Weight unit selected field "Fixed Weight UoM"
        * Random - Program uses random UoM downloaded from NAV (be aware that it might not be weight Unit)
        * Empty - be empty
    2. **Fixed Weight UoM** - UoM which will be used when **Method** = Fixed
2. **Volume - Section**
    1. **Method**
        * Fixed - Uses only one Volume unit selected field "Fixed Volume UoM"
        * Random - Program uses random UoM downloaded from NAV (be aware that it might not be weight Unit)
        * Empty - be empty
    2. **Fixed Volume UoM** - UoM which will be used when **Method** = Fixed

#### Plants
1. **Method**
    * Fixed - Use manually provided Plant
    * Random - Program will randomly pick Plant from list downloaded from NAV (Plants No./VAT)
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Plant** - This plant will be used when **Method** = Fixed (only options available)

## <u>Invoice</u>
### <u>Purchase Order</u>
#### Numbers
- define how program will choose number for Invoice
1. **Method**
    * Fixed - Uses only one Invoice Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - Invoice Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Price and Currency
1. **Price**
    * Price List - Use active price of Item related to the Vendor 
    * Purchase Line - takes Direct unit Cost from Purchase Line
    * From Confirmation - takes price from Confirmation 
    * Prompt - program request input from user when it is needed
2. **Currency**
    * Fixed - Uses only one Currency selected int the field "Fixed Currency"
    * Purchase Order - Takes Currency from Purchase Header
    * From Confirmation - takes currency from Confirmation 
3. **Fixed Currency** - Currency for all Confirmations created will be used when **Method** = Fixed

#### Plants
1. **Method**
    * Fixed - Use manually provided Plant
    * Random - Program will randomly pick Plant from list downloaded from NAV (Plants No./VAT)
    * From Delivery - Takes plan according to plant from connected Delivery file
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Plant** - This plant will be used when **Method** = Fixed (only options available)

#### Invoice Date
- Setup which is used to put BEU Posting(Invoice) Date
1. **Method**
    * Fixed - Uses only one Date selected field "Fixed Date"
    * Random - Uses creates interval and randomly select on date from it
    * Today - Uses only one Today Date
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Date for all Confirmations created will be used when **Method** = Fixed (Date Picker available)
3. **Interval Date - Section**
    - will be used when **Method** = Random
    - this setup create date interval for Delivery Date and randomly pick one date from it
    - it is allowed to to use negative numbers to create interval also to the past
    - Date interval works only with working days (keeps Global Dates Interval setup)
    - interval is created based "From - To" method, where both is defined as "Current Date +/- number of days"

#### Country of Origin
- always takes only 5 random Country Iso Codes from Business Central and add Major JP, CN, DE, HU
1. **Method**
    * Fixed - Use manually provided Country Code
    * Random - Program will randomly pick Country Code from list downloaded from NAV
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Country Code** - This Country Code will be used when **Method** = Fixed

#### Tariffs
- always takes random 10 tariffs from Business Central
1. **Method**
    * Fixed - Use manually provided Tariff Code
    * Random - Program will randomly pick Tariff Code from list downloaded from NAV
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Tariff Code** - This Tariff Code will be used when **Method** = Fixed

### <u>BackBone billing</u>
#### Numbers
- define how program will choose number for BackBone Invoice
1. **Method**
    * Fixed - Uses only one BackBone Invoice Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - BackBone Invoice Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Vendor Service Functions
- part of functionlity responsible which Items be selected into BB Invoice
1. **Items**
    * Fixed - Uses only one BackBone Invoice Item selected field "Fixed Service ID"
    * All - uses all Service IDs (Items) related to Vendor selected
    * Prompt - program request input from user when it is needed
2. **Fixed Service ID** - BackBone Invoice Item which will be used when **Method** = Fixed

#### Price and Currency
1. **Price**
    * Fixed - Uses only one Price selected field "Fixed Service ID"
    * Prompt - program request input from user when it is needed
2. **Fixed Price** - Price for all Items on BB Invoice, will be used when **Price** = Fixed
3. **Fixed Currency** - Currency for all Items on BB Invoice

#### Quantity
1. **Items**
    * One - use 1 for all lines
    * Prompt - program request input from user when it is needed

#### Invoice Date
- Setup which is used to put BEU Posting(Invoice) Date
1. **Method**
    * Fixed - Uses only one Date selected field "Fixed Date"
    * Today - Uses only one Today Date
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Date for Back Bone Invoice created will be used when **Method** = Fixed (Date Picker available)

#### Order Reference
1. **Order ID - Section**
    1. **Method**
        * Fixed - Uses only one text selected field "Fixed Order ID"
        * Previous Month - Program calculates previous month and transfer it as text 
    2. **Fixed Order ID** - Text for Back Bone Invoice created will be used when **Method** = Fixed
2. **Order Date - Section**
    1. **Method**
        * Fixed - Uses only one Date selected field "Fixed Date"
        * Invoice Date - Program copy value from Invoice Date (previous setup)
    2. **Fixed Date** - Date for Back Bone Invoice created will be used when **Method** = Fixed (Date Picker available)

#### Plants
1. **Method**
    * Fixed - Use manually provided Plant
    * Random - Program will randomly pick Plant from list downloaded from NAV (Plants No./VAT)
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Plant** - This plant will be used when **Method** = Fixed (only options available)

#### Country of Origin
- always takes only 5 random Country Iso Codes from Business Central and add Major JP, CN, DE, HU
1. **Method**
    * Fixed - Use manually provided Country Code
    * Random - Program will randomly pick Country Code from list downloaded from NAV
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Country Code** - This Country Code will be used when **Method** = Fixed

#### Tariffs
- always takes random 10 tariffs from Business Central
1. **Method**
    * Fixed - Use manually provided Tariff Code
    * Random - Program will randomly pick Tariff Code from list downloaded from NAV
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Tariff Code** - This Tariff Code will be used when **Method** = Fixed

### <u>Credit Memo</u>
#### Numbers
- define how program will choose number for Credit Memo
1. **Method**
    * Fixed - Uses only one Credit Memo Number selected field "Fixed Number"
    * Automatic - uses timestamp with prefix
    * Prompt - program request input from user when it is needed
2. **Fixed Number** - Credit Memo Number which will be used when **Method** = Fixed
3. **Prefix** - Prefix given before timestamp used when **Method** = Automatic

#### Price and Currency
1. **Price**
    * Price List - Use active price of Item related to the Vendor 
    * Purchase Line - takes Direct unit Cost from Purchase Line
    * From Confirmation - takes price from Confirmation 
    * Prompt - program request input from user when it is needed
2. **Currency**
    * Fixed - Uses only one Currency selected int the field "Fixed Currency"
    * Purchase Order - Takes Currency from Purchase Header
    * From Confirmation - takes currency from Confirmation 
3. **Fixed Currency** - Currency for all Confirmations created will be used when **Method** = Fixed

#### Plants
1. **Method**
    * Fixed - Use manually provided Plant
    * Random - Program will randomly pick Plant from list downloaded from NAV (Plants No./VAT)
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Plant** - This plant will be used when **Method** = Fixed (only options available)

#### Credit Memo Date
- Setup which is used to put BEU Posting(Credit Memo) Date
1. **Method**
    * Fixed - Uses only one Date selected field "Fixed Date"
    * Random - Uses creates interval and randomly select on date from it
    * Today - Uses only one Today Date
    * Prompt - program request input from user when it is needed
2. **Fixed Date** - Date for all Confirmations created will be used when **Method** = Fixed (Date Picker available)
3. **Interval Date - Section**
    - will be used when **Method** = Random
    - this setup create date interval for Delivery Date and randomly pick one date from it
    - it is allowed to to use negative numbers to create interval also to the past
    - Date interval works only with working days (keeps Global Dates Interval setup)
    - interval is created based "From - To" method, where both is defined as "Current Date +/- number of days"

#### Country of Origin
- always takes only 5 random Country Iso Codes from Business Central and add Major JP, CN, DE, HU
1. **Method**
    * Fixed - Use manually provided Country Code
    * Random - Program will randomly pick Country Code from list downloaded from NAV
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Country Code** - This Country Code will be used when **Method** = Fixed

#### Tariffs
- always takes random 10 tariffs from Business Central
1. **Method**
    * Fixed - Use manually provided Tariff Code
    * Random - Program will randomly pick Tariff Code from list downloaded from NAV
    * Empty - be empty
    * Prompt - program request input from user when it is needed
2. **Fixed Tariff Code** - This Tariff Code will be used when **Method** = Fixed


## <u>Settings</u>
#### Appearance
- this setup contains base appearance settings like themes , accent color and hover color

#### Azure Authorization
- This setup authorize you for NAV to be able to use this program
- all settings here is under your own responsibility
- data are stored hiddenly 
- link: [Assigned Apps OneNote](onenote:https://connectkonicaminolta.sharepoint.com/sites/BEU_NUS_Cloud/SiteAssets/NUS%20Cloud%20Notebook/1%20NUS%20Cloud%20Delivery/Infrastructure.one#Assigned%20apps%20to%20employees&section-id=%7BF2C0C669-A8D0-4BA0-9749-8D50A51977DC%7D&page-id=%7B31979EF2-114D-4D2D-89EF-7F9D048C5BE1%7D&end)
1. **Fields**
    1. **Client Name** - App Name from link
    2. **Client ID** - Client ID from link
    3. **Client Secret** - You should have your own or ask Jiří Adamec for new one
    4. **Tenant ID** - non-changeable field 
    5. **Export NAV folders** - defines if to exports to real Fileserver/Azure or just my personal Download folder 

## <u>Business Central</u>
#### Microsoft Entra Application Card
- make sure that you have your "Microsoft Entra Application Card" created by following these steps
1. Create Card
    - App Field: **Client Name** --> Business Central Field: **Description**
    - App Field: **Client ID** --> Business Central Field: **Client ID**
    - add your email into field **Contact Information**
2. Add Permission
    - NUS_BASIC_CORE
    - NUS_BASIC_W1
    - SUPER (DATA)
3. Enable