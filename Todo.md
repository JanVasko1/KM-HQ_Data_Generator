Information:
Microsoft Entra Application: 	HQ_Data_Generator
Permission Set: NUS_HQ_Data_WS



# Globální funkce:
1) Randomizátor přiřazení Itemů a Qty do delivery
2) Randomiztor datumů
3) BOM Ites --> automaticky předřadit Label Item do Confirmace, tak aby simuloval texts (přidat fixní texty)
4) Definice Free Of Charge  --> je potřeba definovat z Connected Items a nebo poskytnout 2 fixní Itemy (to by bylo jako ulechčení pro generování), nebo že pokud neexistuje "Connected Item - Free of Charge", tak použít Defaultně nastavený
5) Unikátní Vendor Document No --> funkce která zajistá unikátnost čísel (Pre Fix + Time Stamp + Postfix - A, B, C, D ...) (možná si poslední uložit do Settings.json -->)
6) Delivery Dates 
    --> funkce na posunutí  datumů o -1D na delivery kromě víkendů (podle Holidays lib )
7) Ceník --> asi přebírat UnitPrice z ceníku 
8) Stahovat tabulky jen jendou (nestahovat tabulky pro každý běh PO zvlášť) --> ať to trvá co možná nejkratší dobu

# Templates:
- asi by bylo dobrý kdyby page Setup se dala vyexportovat jako template a pak při procesování použít
- na SEtup page mít možnost "Create Template" --> uložit do složky Template
- na Process page mít možnost "Appy Templace" --> výět z uložených
- tenhle setup by měl být nějak oddělený od aplikačního Setupu (protoze má mít v sobě pouze aktuálně zvolené hodnoty a né listy / Dictionary ...)

# Ideas: 
# Confirmation
- ConfirmationID:
    - Methods:
        * Manual: umožnit manuální zadání čísla confiermation --> to protože budu chtít třeba přegenerovat znova
        * Automatic(default): složenina z Prefixu a DAte time
            * Prefix: CON
            * DateTime: 20250215154516

- Line Flags 
    - Nechat to tak že Popup se objeví pouze pokud bude "Manual Line Flag assignment" = True
    - Vždy by si uživatel měl mít možnost nastavit vlastní Line Flag hned po tom co se zpraciuje "Confirmation", ale jen pokud budou zapnutý
(metoda random (prostě náhodně vybrat každý line flag), nebo pevně určit --> načíst řádk, které budou použity v Confirmation a nechat uživatele zvolit jaký line flag chce k jendotlivým řádkům )
    - Substitution --> když manuálně vyberu, tak musím i manuálně vybrat 
    - Label --> pozor musí být pro všechny mašiny automaticky, protože BEU to dělá automaticky (ale pokud mám manual, tak by měl ten label automaticky označit tam kde je použitý i když byl vygenerovaný automaticky)
    Příklad:
                    Substitution    New Item No        Cancel      Finished        Lable       To Parent
        Item 1                                                                       X
        Item 2             X          Item3                          X
        Item 3                                            X
        Item 4
        Item 5
        Item 6                                                                       X

- ATP Check - schedules
    - zapínač: to jestli má program generovat dané řádky
    - pozor funguje tak že můžeme mít sice vícero ONH a ONB statusů ale pouze jeden BACK (to ale znamená že je tam nějaký QTY nevyllněný)
    - vytvořit setup jak se mají uřčovat datumy pro každý typ:
        ONH date range: "CD + 1D" - "CD + 10D" 
        ONB date range: "CD + 2W" --> BEU posílá jen týden v roce 
    - dotaz jestli a jak chci procesovat ATP check:
        * Full Random: plný random pro každý řádek a qty řádku zvlášť (neměl by mít stejné datumy) -->je to option kdy opravdu může jeden řádek mít víc záznamů
        * Line Random: random datumy pro každou lines
    - Field: Max ATP Records : parametr který omezi počet záznamů v ATP na maximálně 5

- Prices (použít stejné pak na Invoice)
    - Price Source MEthods:
        * Purchase Line: vezme Direct Unt Cost z exportované PO Line 
        * Price List: vzít si přémo u NAV price list jednotlivým Itemům a k Free Of Charge doplnit fiktivní, nějakou malou, a pokud chybí tak pop-up Window s dotazem na doplnění ceny
        * Manual
            --> popup page která se objevá kde u každého řádku budu moci specifikovat cenu za UoM
                Item        Desctiption     Qty         Unit Price
                Item1       MAšina          5             1200
                ITem2       FreeOfCharge    3             5
                Item3       FreeOfCharge    1             3
                Item4       Pořadač         3             250
                ....  
- Price Currency:
    - výběr z listu Currencies (3 digits) --> list udělat jako pevný v kodu
- "Order_Unti: "C62" --> tohle asi budu muset nějak domyslet agenerovat podle toho co bylo skutečně objednáno

- Other Keys:
    * Header
        * generation_date
        * order_date --> take it from Export
        * orderresponse_date --> same as "generation_date"
        * buyer_party --> informaiton from Company Info + HQ Communication Setup
        * invoice_party = buyer_party
        * delivery_party = buyer_party
    * Lines 
        - Remarks --> ????
            * item_category --> ????
            * discontinued
            * set
            * bom
            * bom_with_delivery_group



# CPDI Status
- zde by bylo dobrý mít možnost zaškrtnout kkterý status chci exportovat 
- samozřejmně ho musí program vytvořit pouze pro Objednávky který mají CPDI 



# PreAdvice
- musí použít stejné číslo delivery
- musí být dělaný stejně jako Delviery jen se může vybírat "Delivery Date" samostatně od delivery
- Delviery Date
    - Delviery date range: "CD + 1D" - "CD + 10D"  (dostupný když něni manual!!!) (můsí umožnovat aby vytvořil datumy jak do minulosti tak do budoucnosti)
    - Methods:
        * Fixed: Manuálně vybrané datum jen jedno jediné
        * Random: pro každou delivery si vybere vlastní datum (právě z range)
        * Delivery Date Minus: kde by bylo možno zadat třeba -1D od delivery Date dané delivery
        * Manual: pro každou delivery si bude moci uživatel zvolit vlastní datum
            - zde bude potřeba asi nějaká pop-up page (možná na té popup page zobrazit ten kalendář: https://github.com/maxverwiebe/CTkDatePicker)
                    Delviery    Delviery Date
                    DEL1        2025-02-15
                    DEL2        2025-02-19
                    ....  


# Delviery
- DelvieryID:
    - Methods:
        * Manual: umožnit manuální zadání čísla confiermation --> to protože budu chtít třeba přegenerovat znova
        * Automatic (default): složenina z Prefixu a Date time
            * Prefix: DEL
            * DateTime: 20250215154516
- nastavení které řekne když mám zapnutý randomizátor Delviery zda Free of charge mají být doručeny s mašinou a nebo můžou být zvlášť (jenom boolean)
- Delivery Count 
    --> počet Delviery které se vytvoří Inetger
    - Methods:
        * Fixed --> zadat i na Downlaod page
        * Random (Option 1): 
            * Random Entity: 
                - Lines only: random vybere jen mezi lines a plný Qty
                - Lines and Qty: random jak lines tak i Qty on Line --> tzv. plný random
        * Prompt (Option 1) (pouze pro celé řádky)
            --> popup page která se objevá kde u každého řádku budu moci specifikovat Delivery ke které patří
                    **Item**    **Description**     **Qty**     **Delviery**
                    Item1       MAšina              5           DEL1
                    ITem2       Pořadač             3           DEL1
                    Item3       Accesory            1           DEL2
                    ....  

- Serial numbers (NUS Cloud má 50 znaků, NUS3 má 20 znaků)
    Method:
        
    - musím zajistit, aby byli 100% unikátní
    - Složenina:
        * Prefix: SN
        * DateTime: 20250215154516
        * Pořadí: Counter
        * Celkem: SN_20250215154516_1
- Delviery Date
    - Delviery date range: "CD + 1D" - "CD + 10D"  (dostupný když něni manual!!!) (můsí umožnovat aby vytvořil datumy jak do minulosti tak do budoucnosti)
    - Methods:
        * Fixed: Manuálně vybrané datum jen jedno jediné
        * Random: pro každou delivery si vybere vlastní datum (právě z range)
        * Prompt: pro každou delivery si bude moci uživatel zvolit vlastní datum
            - zde bude potřeba asi nějaká pop-up page (možná na té popup page zobrazit ten kalendář: https://github.com/maxverwiebe/CTkDatePicker)
                    Delviery    Delviery Date
                    DEL1        2025-02-15
                    DEL2        2025-02-19
                    ....  

- Tracking Information (Delviery + Package)
    - BEU Carrier ID
        - Methods:
            * Manual: MAnuálně vybraný "BEU Carrier ID"
            * Randam: Náhodný vývběr z listu "Shipping Agents" kteřá mají "BEU Carrier ID"
    - Package No: Nějaký Prefix + random číslo (z intervalu)
    - EXIDV2: random číslo (z intervalu)
    - Packages:
        - vytvořit metodu random přiřazení Itemů a qty do pakage
         


# IAL



# Invoice
- InvoiceID:
    - Methods:
        * Manual: umožnit manuální zadání čísla Invoice --> to protože budu chtít třeba přegenerovat znova
        * Automatic (default): složenina z Prefixu a Date time
            * Prefix: INV
            * DateTime: 20250215154516
- List Itemů je přesně podle develiry
- Plant mít možnost vyběru pland ze který přišlo zboží
    - Methods:
        * Random: vybere random z listu pro každou fakturu
        * Prompt: 
            Invoice     Plant    
            INV1        1000
            INV1        1004
            ....  
- Posting Date (Document Date)
    - Posting Date range: "CD + 1D" - "CD + 10D"  (dostupný když něni manual!!!) (můsí umožnovat aby vytvořil datumy jak do minulosti tak do budoucnosti)
    - Methods:
        * Fixed: Manuálně vybrané datum jen jedno jediné
        * Random: pro každou delivery si vybere vlastní datum (právě z range)
        * Prompt: pro každou delivery si bude moci uživatel zvolit vlastní datum
            - zde bude potřeba asi nějaká pop-up page (možná na té popup page zobrazit ten kalendář: https://github.com/maxverwiebe/CTkDatePicker)
                Invoice    Posting Date
                INV1        2025-02-15
                INV2        2025-02-19
                ....  
- Prices
    - použít z Confirmation


# Standalone Invoice
- InvoiceID:
    - Methods:
        * Manual: umožnit manuální zadání čísla Invoice --> to protože budu chtít třeba přegenerovat znova
        * Automatic (default): složenina z Prefixu a Date time
            * Prefix: BBINV
            * DateTime: 20250215154516
- List Itemů:
    - Počet řádků (int): maximálně počet jako je počet rekordů ve "Vendor Service Function" patřící k Vendorovi 
    - vždy Qty = 1
    - Price:
        * Random: nechat ke každému řádku nagenerovat cenu v random intervalu (vytvořit 2 pole "From" / "To")
        * Fixed: prostě použit fixní cenu pro všechny řádky










# Purchase REturn Order
## Confiramtion

- Number --> stejna jako u Invoice
- Price and Currency --> stejně jako u Invoice
- Qty --> 
	Metoda:
        * Promt: Zeptat se kolik chci z původního množství Exportovaného potvrdit
        * All Exported: vzít 1:1
        * Reduce %: prostě procentuální random podíl že se neodsouhlasí všechno












# Others Ideas
-> možná udělat i templaty na výběr nastavení (jako pro Tendry, Consumables ... prsotě jakoby hlavní logistický procesy a k nim definovyný setupový .json, který by si uživatel měl možnost načíst --> pro rychlejší nasttavování)


-> umožnit dodávat Free of Chart / Documentation společně s mašinou --> jinými slovy zajistit, aby randomizátor do Delivery vždy dodadl Free Of Charge Qty stejné jako mašina
-> vyběrač toho co vlastně chci nagenerovat (užmonit třeba jen Confirmation )
    Confirmation
    Pre-Advice
    Delviery
    CPDI
    Invoice
    Invoice.pdf
    Invoice - Stand Alone --> tady budu muset vybrat Vendora a podle toho postavit Faktur (a stáhnoiut z Vendor Service Function info)
    Whole --> zatrhnout když chci generovat všechno

  

# Download from NAV
1) T38 - Purchase Header (Web Service: P50)
	-> Field List: 
        - No. --> k použití na dokumentech jako Purchase Order No
        - HQ Identification No. --> kvůli tomu abych ho použil v generovaných dokumentech
        - ShippingConditionFieldNUS --> abych věděl jaký condition použity --> míožná nebude potřeba
        - HQ Complete Delviery --> abych věděl jestli dodat vše najednou nebo mohu rozdělit Deliveries
        - PDI Center --> abych věděl jestli mám generovat i CPDI fily (pokud bude BEU)
        - Expected Receipt Date --> abych věděl kvůli výpočtu datumů
        - Promiss Receipt Date --> abych věděl kvůli výpočtu datumů
        - Requested Receipt Date --> abych věděl kvůli výpočtu datumů
        - Order Date --> použít to pak ve file jako "order_date"
        - HQCPDILevelRequestedFieldNUS --> abych věděl jestli o jaký Level mají zájem

1.1) T39 - Purchase Lines (Web Service: P54)
    -> Field List: 
        - Type --> abych věděl jetli je to Item nebo ne
        - No. --> prostě seznam Itemů
        - Description --> kvůli použijí v .json jako "description_long" a dalších
        - Quantity --> prostě abych věděl s kolika Qty se má počítat
        - Direct Unit Cost Exct. VAT --> jen ro jistotu abych věděl jakou jednotkovou cenu použít
        - Unit Of Measure Code

2) T27 - Items (Web Service: P31)
    - pouze fitrováno pro Itemy, které jsou na Nákupní objednávce
    -> Field List: 
        - BEU Set --> abych věděl jestli je Item BEUSET and nebo ne (pak by měl mít vypněný i BOM)
        - Vendor Item No. --> možná jen pro jistutu ale bylo by dobrý to pa použít v .json v poli "buyer_aid"
        - Item Tracking Code --> kvůli tomu jestli mám generovat Seriová čísla pro daný Item nebo ne (zjistit si pokaždé ze stažené tabulky Tracking Codes)
        - BEU End of Live --> protože bych pak na Confirmation mohl nastavit "Line Flag = Finish"
        - Substitutes Exist --> protože bych pak na Confirmation mohl nastavit "Line Flag = Substituted", a dal tam nové číslo Itemu
            --> pokud ano musím stáhnout i informace o náhradním Itemu z "5715 - Item Substitution"
        - Assembly BOM --> k použití a získání informací ohledně struktury BOMu
            --> pokud ano musím stáhnout i informace o náhradním Itemu z "5715 - Item Substitution"

2.1) T5715 - Item Substitution (Web Service: P5716)
    -  stahovat pouze pokud je jeden z Itemů na PO Line označen jako "Substitutes Exist = True"
    -> Field List: 
        - Substitute Type --> jen pro kontrolu abych věděl že jde o Item
        - Substitute No. --> thenhle Item bude nahrazovat starý pokud má Substituci (+ musí se k němu stáhnout data z Item)

2.2) T6502 - Item Tracking Code (Web Service: P6502)
    -> Field List: 
        - Code --> pro vyhledávání 
        - SN Purchase Inbound Tracking --> právě podle tohoto pole rozhodovat jestli budeme 

2.3) T90 - BOM Component (Web Service: P36)
    -  stahovat pouze pokud je jeden z Itemů na PO Line označen jako "Assembly BOM = True"
    -> Field List: 
        Type --> jen pro jistutu abych věděl, že jde o Item, který se může dát do .json (vynechat Resource a ostatní typy)
        Parrent Item No. --> kvůli tomu abych pam mohl filtrovat d DataFrame
        No. --> právě Item který je sčástí BOMU (pozor pro tyto Itemy se musí stáhnout nastavení Itemů taky)
        Quantyty per --> je to prvě množství se kterým musím počítat
        Unit of Measure Code --> asi budu s tím muset něco dělat, protože pak musím správně aplikovat na PO Line

2.4) T5404 - Item Unit of Measure (Web Service: P5404)
    -  stahovat pouze pro Itemy v SEznamu Itemů (po tom co si stáhnu opravdu kompletní seznam abych znal přepočet na PCS pro všechny Itemy)
    -> Field List: 
        - Item No. --> primární klíč společně s Code
        - Code --> primární klíč společně s Item No.
        - Qty per Unit of Measure --> je to právě přepočet na hlavní UoM

2.5) T204 - Unit of Measure (Web Service: P209)
    -> Field List: 
        - Code --> tohle je code který se používá v NAV 
        - International Standard Code --> tohle je kod který se používá v komunikaci

3) T51050 - HQ Communication Setup NUS (Web Service: P51050)
	-> Field List: 
        - HQ Vendor Type --> kvůli filtru na "KMBS"|"DEVELOP" 
        - HQ Vendor No. --> abych správně přidělil "HQ Identification No" do .json
        - HQ Identification No --> kvůli použití na dokumentech
        - Zero Date --> použití pro ATP pro BackOrders
        - HQ Confirm-File Path --> kvůli ukládání souborů do sprvávné cesty
        - HQ PreAdvice-File Path --> kvůli ukládání souborů do sprvávné cesty
        - HQ CPDI Import Path --> kvůli ukládání souborů do sprvávné cesty
        - HQ Delivery-File Path --> kvůli ukládání souborů do sprvávné cesty
        - HQ Invoice-File Path --> kvůli ukládání souborů do sprvávné cesty
        - File Connector Code --> kvůli ukládání souborů do sprvávné cesty

3.1) T4060864 - NVR LFS Local FS Con. Setup (Web Service: P4060864)
    -> Field List: 
        - Code --> kdyby jich bylo více
        - Root Path --> kvůli ukládání souborů do sprvávné cesty

3.2) T51064 - HQ Item Transport Register NUS (Web Service: P51064)
    - vždy jen exportovat pro "Docuemnt Type = Order", "Document No. = POs", "Vendor Document Type = Export"
    -> Field List: 
        - Document type --> jen pro kontrolu asi
        - Document No. --> abych mohl filtrovat při dohledávání polí
        - Document Line no --> mohlo by se hodit
        - Exported Line No. --> určitě se bude hodit v .json filech
        - Vendor Document Type --> jen pro kontrolu
        - Line Type --> Pro kontrolu, že jde o Item
        - Item No. --> abych věděl pro jaký Item připravovat dokumenty
        - Quantity --> abych věděl jaký množství bylo objednáno
        - Unit of Measure --> abych věděl jaká měrná jednotka byla objednána

3.3) T51016 - HQ CPDI Levels NUS (Web Service: P51016)
    - jen kvůli tomu abych měl 
    -> Field List: 
        - Level --> bude použit v CPDI.json jako (order_reason)

3.4) T51015 - HQ CPDI Status NUS (Web Service: P51015)
    - jen kvůli tomu abych měl 
    -> Field List: 
        - Status Code --> bude použit v CPDI.json jako (status)

4) T291 - Shipping Agent (Web Service: P428)
	-> Field List:
        - BEU Carrier ID --> k použití na Delivery jako dopravce  (filtrovat na neprázdný)

5) T10 - Shipment Method (Web Service: P11)
    - možná zde nbude potřebovat stahovat vůbec, možná bude stačit pouze jedna, když se zeptám v BEU a zjistím jak to je 
    -> Field List:
        - Code --> bude použito jako "incoterms1" .json

6) T260 - Tariff Number (Web Service: P310)
	-> Field List:
        - No. --> je to kvůli tomu abych byl schopen dát reálné Tarif No. do faktury

7) T9 - Country/Region (Web Service: P10)
	-> Field List:
        - Code --> asi jen protože je to primární klíč
        - ISO Code --> bude použit v .json

8) T51121 - Plant No./VAT NUS (Web Service: P51121)
    -> Field List:
        - Code --> bude použit v Delivery .json
        - VAT --> bude pole Plantu použito na Invoice .json

9) T51452 - Vendor Service Function NUS (Web Service: P51452)
    - kvůli "Invoice Stand Alone" fakturám a filtrovat pouze na Vendora
    -> Field List:
        - Vendor --> Asi jen kvůli filrtrování podle toho jakou 
        - Vendor Service ID --> bude použito jako Item v .json
        - Vendor Service Name --> bude použito jako Item Description v .json 

10) T79 - Company Information (Web Service: P1)
    -> Field List: 
        - Name --> k použití v .json jako "name2"
        - Address --> k použití v .json jako "street"
        - Post Code --> k použití v .json jako "zip"
        - City --> k použití v .json jako "city"
        - Country/Region Code --> k použití v .json jako "country"

Documents:
    Confirmation
        HQ ATP Check --> jak plnit informace pro ATP? 
        Remarks -> jak plnit Remarks
            - 
            BOM Item --> první musí být textový pole
            set
            Item_category

        Speciály:
            --> udělat Confirmace pro cancelation všech řádků --> tak aby se dalo otestovat to, že se zcanceluje celý dokument
            --> BOMy 

    Pre-Advice

    CPDI

    Delivery

    Invoice

    Invoice.pdf

    Invoice-Stand Alone
