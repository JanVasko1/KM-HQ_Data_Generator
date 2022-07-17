# General principle
"""
1) Copy template into varialbe
2) update values
3) Safe file into import folders (file name take as pořadové čislo + Vendor Document No.)
4) Zkontrolovat jestli existují importní složky
"""

#-------- Confirmaiton --------#
with open("./Lib/NUS3_Template_Confirmation.xml", "r") as f:
    temp_Header_file_lines = f.readlines()
f.close()
for line in temp_Header_file_lines:
    line = line.replace("<GENERATION_DATE>HERE</GENERATION_DATE>", f"<GENERATION_DATE>JVA</GENERATION_DATE>")
#-------- PreAdvice --------#
#-------- Delivery --------#
#-------- Invoice --------#