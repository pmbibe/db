# from pathlib import WindowsPath
# import get_checklist
import connect_db_cx
import pandas as pd
import validate

# Find script with modules name

def is_in(a,b):
    if validate.validate_m_sm_f(a) and a.upper() in b.upper(): return True
    return False

# Convert list to string
def list2string(list):
    return '\n'.join(list)

# 
def verify_input(module_name, sub_module_name, feature_name, file_path):
    if is_in(module_name, file_path):
        if sub_module_name != "":
            if not is_in(sub_module_name, file_path):
                return False # Sub module not found
            elif feature_name != "" and not is_in(feature_name, file_path):
                    return False # Feature not found
    else:
        return False
    return True
# Retrun xlsx format with dictionary
def dict_to_csv(dict, file_name, is_ver2): 
    try:
        df = pd.DataFrame.from_dict(dict).transpose() if not is_ver2 else pd.json_normalize(dict).transpose()
        with pd.ExcelWriter('/report/{}.xlsx'.format(file_name), engine='xlsxwriter') as writer:
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

def write2file(file_name, scripts):
    with open(file_name, "w") as f:
        for script in scripts:
            f.write(script + "\n")
    f.close()
def read_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    f.close()
    return lines

def create_report(all_scripts, enum_folder, module_name, sub_module_name, feature_name, is_standalone):
    # all_scripts = [x.as_posix() for x in all_scripts]
    all_scripts = [x.as_posix() for x in all_scripts if verify_input(module_name, sub_module_name, feature_name, x.as_posix()) ]
    # write2file("{}/allScriptsFile".format(enum_folder), all_scripts)
    
    try:
        for file_path in all_scripts:
            if verify_input(module_name, sub_module_name, feature_name, file_path): 
                print(file_path)
                connect_db_cx.run_sql_script(file_path, is_standalone)
    except Exception as e:
        print(str(e))          
    if all_scripts != []:
        # successed_scripts = read_file("{}/successedScriptFile".format(enum_folder))
        successed_scripts = connect_db_cx.successed_script_file
        failed_scripts = connect_db_cx.failed_script_file 
        # failed_scripts = read_file("{}/failedScriptsFile".format(enum_folder))
        not_run_yet_scripts = [x for x in all_scripts if x not in successed_scripts and x not in failed_scripts]
        dict = {"All": list2string(all_scripts), "Successed": list2string(successed_scripts), "Failed": list2string(failed_scripts), "Not run yet": list2string(not_run_yet_scripts)}
        dict_to_csv(dict, "{}-{}-{}".format(module_name, sub_module_name, feature_name), True)
    else:
        print("Not found module {} - sub-module {} - feature {}".format(module_name, sub_module_name, feature_name))

