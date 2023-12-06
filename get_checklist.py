# YYYY.MM/YYYY.MM.DD/Module_Name/Script
import copy
import pathlib
import re
import json
import pandas as pd
# import xlsxwriter

sql_scripts = []

def find_SQL(full_path):
    try:
        list_dir = pathlib.Path(full_path)
        for dir in list_dir.iterdir():
            if dir.suffix == ".sql":
                sql_scripts.append(dir)
            if dir.is_dir():
                find_SQL(dir)
    except Exception as e:
        print(str(e))

def get_statement(file_name):
    statements = []
    statement = ""
    i = 0
    # regex = r"^(CREATE|INSERT|SELECT|UPDATE|ALTER)"
    regex = r"^(CREATE|INSERT|UPDATE|ALTER)"
    regex2 = r".+;$"
    with open(file_name, encoding="utf8") as f:
        for line in f:
            if re.match(regex, line.strip().split(" ")[0].upper()):                
                if re.match(regex2, line.strip()):
                    statements.append(line)
                else:
                    i=1
            if not re.match(regex2, line.strip()) and i > 0 and "--" not in line.strip():
                statement = statement + '{}'.format(line)
            elif i > 0 and "--" not in line.strip():
                statement = statement + '{}'.format(line)
                statements.append(statement)
                statement = ""
                i = 0
    return statements
         
def sub_path_file(file_name, full_path):
    return format(pathlib.PureWindowsPath(file_name).as_posix().replace(full_path, ""))

def module_name(file_name):
    return pathlib.PureWindowsPath(file_name).parts[6]

def deploy_rollback_backup(full_path):
    modules = []
    dict = {}
    empty_dict = {"Rollback":[], "Backup":[], "Deploy":[]}
    for sql_script_file in sql_scripts:
        if module_name(sql_script_file) not in modules:
            modules.append(module_name(sql_script_file))
            dict[module_name(sql_script_file)] = copy.deepcopy(empty_dict)
        sub_path = sub_path_file(sql_script_file, full_path).upper().split("/")
        if "ROLLBACK" in sub_path:
            dict[module_name(sql_script_file)]["Rollback"].append("/".join(sub_path_file(sql_script_file, full_path).split("/")[1:]))
        elif "BACKUP" in sub_path:
            dict[module_name(sql_script_file)]["Backup"].append("/".join(sub_path_file(sql_script_file, full_path).split("/")[1:]))
        else:
            dict[module_name(sql_script_file)]["Deploy"].append("/".join(sub_path_file(sql_script_file, full_path).split("/")[1:]))
    return dict

def deploy_rollback_backup_csv(full_path):
    modules = []
    dict = {}
    empty_dict = {"Rollback":"", "Backup":"", "Deploy":""}
    for sql_script_file in sql_scripts:
        if module_name(sql_script_file) not in modules:
            modules.append(module_name(sql_script_file))
            dict[module_name(sql_script_file)] = copy.deepcopy(empty_dict)
        sub_path = sub_path_file(sql_script_file, full_path).upper().split("/")
        if "ROLLBACK" in sub_path:
            dict[module_name(sql_script_file)]["Rollback"]="\n".join(["/".join(sub_path_file(sql_script_file, full_path).split("/")[1:]),dict[module_name(sql_script_file)]["Rollback"]])
        elif "BACKUP" in sub_path:
            dict[module_name(sql_script_file)]["Backup"]="\n".join(["/".join(sub_path_file(sql_script_file, full_path).split("/")[1:]),dict[module_name(sql_script_file)]["Backup"]])
        else:
            dict[module_name(sql_script_file)]["Deploy"]="\n".join(["/".join(sub_path_file(sql_script_file, full_path).split("/")[1:]),dict[module_name(sql_script_file)]["Deploy"]])
    return dict

def json_format(dict):
    return json.dumps(dict, indent = 4) 

def get_file_by_index(index, dict):
    i = index.split(".")
    i_module = int(i[0])
    i_rbd = int(i[1])
    i_file = int(i[2])
    return list(dict[list(dict)[i_module]][list(dict[list(dict)[i_module]])[i_rbd]])[i_file]

def set_file_index(dict):
    index_module = ""
    index_rbd = ""
    index_file = ""
    for key, value in dict.items():
        index_module = key.split(".")[0]
        for v_key, v_value in value.items():
            index_rbd = str(list(value).index(v_key))
            if v_value:
                for vv in v_value:
                    index_file = str(v_value.index(vv))
                    dict[key][v_key][v_value.index(vv)] = "{}.{}.{}---{}".format(index_module, index_rbd, index_file, dict[key][v_key][v_value.index(vv)])
                    index_file = ""
            index_rbd = ""
        index_module = ""
    return dict
def dict_to_csv(dict):
    df = pd.DataFrame.from_dict(dict)
    writer = pd.ExcelWriter('Module.xlsx', engine='xlsxwriter')
    df.style.set_properties(**{'vertical-align': 'top'}).to_excel(writer, sheet_name='Sheet1')
    writer.close()
