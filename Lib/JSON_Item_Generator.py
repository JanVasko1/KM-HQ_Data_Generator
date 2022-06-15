import pyodbc
import pandas
import json
import os

import PO_Line_Donwload
Items_Dict = PO_Line_Donwload.Get_Lines(pandas, pyodbc)
Items_df = pandas.DataFrame(Items_Dict, columns=Items_Dict.keys())

# Prepare JSON helper file
JSON_help_path = os.path.dirname(os.path.abspath(__file__))
json_object = json.dumps(Items_Dict, separators=(',', ':'), indent="") 
Json_list = json_object.split("\n")

# Export JSON Helper to Setup Dataframe 
with open(f"{JSON_help_path}/Items_df.json", mode="tw") as file:
    for line in Json_list:
        founded = line.find("{") 
        if line.find("{") == 0:
            file.write(str("    ")+line+str("\n"))
        elif line.find("],") == 0: 
            file.write(line+str("\n"))
        elif line.find("]") == 0: 
            file.write(line)
        elif line.find(":[") > 0:
            file.write(str("\t\t")+line)
        elif line.find("}") == 0:
            file.write(str("\n    ")+line)
            file.write(str("\n"))
        else:
            file.write(line)