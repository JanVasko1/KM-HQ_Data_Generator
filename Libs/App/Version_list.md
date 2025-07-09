### Contact
**Author**: Jan Vaško<br>
**Email**: Jan.Vasko@konicaminolta.eu<br>
**Mobile**: +420 601 383 301<br>

### Version List
#### 1.1.0
- Buttons not possible to press when action triggered, release it after action finished
- API rebuild from FastAPI to Azure Functions

#### 1.0.4
- Widget Entry Field save to list enabled validation
- General_Usage template is not overwritten with every program start issue corrected
- Python: Request library upgrade, because found vulnerability
- Information page height adjusted
- BHN Invoice Exchange Rate integration
- Plant list reduced to be only [1000, 1004] as Plant=1002 is no more existing

#### 1.0.3
- Correct Function assignment for Button Widget Class
- Correct Entry Field Widget Class Validation for Integer, Float and Percentage not allowing empty 
- General Usage Template added as default

#### 1.0.2
- Program is remembering last used NUS Version, Environment and NOC on Download page
- Upload to empty template issue corrected

#### 1.0.1
- Prompt page height - added one line to secure nicer look

## 1.0.0
- Official Application Release (Beta testing finished, thank you Karolina)

#### 0.8.7
- TopUp window max height corrected when content is smaller that max_height parameter
- return Company_Logo.png

#### 0.8.6
- BackBoneBilling lines segment corrected, Key/Value pair "Order_Reference"/"line_item_id" deleted
- Block to open multiple same Pickers for one Field

#### 0.8.5
- Settings loads change because of API
- issue related template visibility and save solved
- limits Tariffs list to 10 and Country of Origin to 9 (4 major + 5 random)

#### 0.8.4
- multi Purchase Document and Purchase Return Documents issue correction
- Correction of issues found in Beta Testing
- freezing operation buttons on Download page when no company selected

#### 0.8.3
- when template change the GUI is updated

#### 0.8.2
- automatically delete unnecessary files with installation
- delete whole app folder after uninstallation

#### 0.8.1
- Information page created
- markdown color based on theme issue corrected

### 0.8.0
- Purchase Return Order Confirmation and Invoice PDF

### 0.7.0
- GUI optimization

#### 0.6.1
- SideBar as Class

### 0.6.0
- API Endpoint integrated

### 0.5.0
- Purchase Order Invoice files process integrated
- Slight application speed-up

### 0.4.0
- Purchase Order PreAdvice files process integrated
- Random Date interval --> Holidays(GE) and weekends are skipped

#### 0.3.1
- Pop-Up message box shows always in the middle of main window

### 0.3.0
- Purchase Order Delivery files process integrated

#### 0.2.1
- threading implemented for all major processes of Download and process 
    * Purchase Order
    * BackBone Billing
    * Purchase Return Order
    * Download Companies
    * Company Select
- Better Authorization secure

### 0.2.0
- Purchase Order Confirmation files process integrated

#### 0.1.1
- Generate Invoice.json issue with lines Overwrite when transferring to json template from DataFrame
- dynamic PopUp Windows height according content with maximal parameter
- delete value in EntryField when validation unsuccessful

### 0.1.0
- BackBoneBilling files process integrated

#### 0.0.7
- multiple file Drag&Drop
- SideBar and Header on own page
- template application issue correction
- Exchange Authorization information stored in binary file format (not readable from outside)
- OAuth2 status in program header

#### 0.0.6
- Settings Tables, nut the "Update" button is available
- Drag&Drop into local settings (tables) updates the values in tables in GUI not only on Backend
- Re-distribute local libraries to separate files to speed-up 

#### 0.0.5
- DatePicker Issue correction for get() during download
- ColorPicker Issue with save value to Configuration.json
- Settings import split by 2 methods
    * Overwrite --> overwrite all and use only imported information
    * Add --> Add new and keep unique values only
- Pop-Up windows are always "OnTop"
- Join Events corrected one issue with missing data
- Join Events joining decision based on Busy status

#### 0.0.4
- DatePicker correction to react to Theme
- DatePicker show Today Day
- ColorPicker button harmonize look with DatePicker - in-line
- Icons sets set to fixed "Lucide"
- created .json with application detail -> transferred from Settings.json
- All pop-up messages always wait for User response to continue
- Drag&Drop crash issue solved

#### 0.0.3
- For Save into Settings "Drag&Drop" function available
- Whole Settings file can be exported and imported back (used for Software updates)
- All tables can be exported and saved (Drag&Drop) into program
- DatePicker introduced for fields represents dates
- correct position of Pop-Up pages (right below button pressed)
- Exchange Change Color oc Category for non-Active Project

#### 0.0.2
- Logo picture change position from bottom side of SideBar into Tom of SideBar
- SideBar prints Application Version

### 0.0.1
- Start

## Fun facts
### Setup Combination for Document
- Confirmation - 19 440 possible setup combination
- CPDI - 2 possible setup combination
- PreAdvice - 4 possible setup combination
- Delivery - 2 834 352 possible setup combination
- Invoice - 8 640 possible setup combination
- BB Invoice - 27 648 possible setup combination