from pathlib import WindowsPath
# import get_checklist
import mysql_db
import pandas as pd

def is_in(a,b):
    if a.upper() in b.upper(): return True  
    return False

# Convert list to string
def list2string(list):
    return '\n'.join(list)

# Retrun xlsx format with dictionary
def dict_to_csv(dict, file_name, is_ver2):
    try:
        df = pd.DataFrame.from_dict(dict).transpose() if not is_ver2 else pd.json_normalize(dict).transpose()
        with pd.ExcelWriter('Module-{}.xlsx'.format(file_name), engine='xlsxwriter') as writer:
            cell_format = writer.book.add_format() # type: ignore
            cell_format.set_font_color('red')
            cell_format.set_text_wrap()
            cell_format.set_align('top')
            df.to_excel(writer)
            worksheet = writer.sheets["Sheet1"]
            for col in range(len(df.columns)+1):
                worksheet.set_column(col, col, None, cell_format)
                worksheet.autofit()
        print("Saved to XLSX File")
    except Exception as e:
        print(e)

def create_report(all_scripts, module_name, sub_module_name, feature_name):
    all_scripts = [x.as_posix() for x in all_scripts]
    try:
        for file_path in all_scripts:
            if is_in(module_name, file_path) and is_in(sub_module_name, file_path) and is_in(feature_name, file_path):
                print("----------{}-----------".format(file_path))
                mysql_db.run_sql_script(file_path)
    except Exception as e:
        print(str(e))
        
    successed_scripts = mysql_db.successed_script_file 
    failed_scripts = mysql_db.failed_script_file     
    not_run_yet_scripts = [x for x in all_scripts if x not in successed_scripts and x not in failed_scripts]
    dict = {"All": list2string(all_scripts), "Successed": list2string(successed_scripts), "Failed": list2string(failed_scripts), "Not run yet": list2string(not_run_yet_scripts)}
    dict_to_csv(dict, "Scripts", True)

create_report([WindowsPath("D:/DS_IT_2537/employees.sql")], "", "", "")
