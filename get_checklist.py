# YYYY.MM/YYYY.MM.DD/Module_Name/Script
import copy
import pathlib
import re
import json  

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
            dict[module_name(sql_script_file)]["Rollback"].append(sub_path_file(sql_script_file, full_path))
        elif "BACKUP" in sub_path:
            dict[module_name(sql_script_file)]["Backup"].append(sub_path_file(sql_script_file, full_path))
        else:
            dict[module_name(sql_script_file)]["Deploy"].append(sub_path_file(sql_script_file, full_path))
    return dict

def json_format(dict):
    return json.dumps(dict, indent = 4) 

def get_file_by_index(index, dict):
    i = index.split(".")
    i_module = int(i[0])
    i_rbd = int(i[1])
    i_file = int(i[2])
    return list(dict[list(dict)[i_module]][list(dict[list(dict)[i_module]])[i_rbd]])[i_file].split("---")[1]

def set_file_index(dict):
    index_module = ""
    index_rbd = ""
    index_file = ""
    for key, value in dict.items():
        index_module = str(list(dict).index(key))
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
