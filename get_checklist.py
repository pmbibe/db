# YYYY.MM/YYYY.MM.DD/Module_Name/Script
import copy
import pathlib
import re
# import os
import json


sql_scripts = []

# find all .sql extension in directory
def find_SQL(checklist_path):
    try:
        list_dir = pathlib.Path(checklist_path)
        for dir in list_dir.iterdir():
            if dir.suffix == ".sql":
                sql_scripts.append(dir)
            if dir.is_dir():
                find_SQL(dir)
    except Exception as e:
        print(str(e))

# print all script, include SQLPlus Command
def read_checklist_script(file_name):
    with open(file_name, encoding="utf8") as f:
        return f.read()    

# get sub path 
def sub_path_file(file_name, checklist_path):
    return format(pathlib.PureWindowsPath(file_name).as_posix().replace(checklist_path, "")) # Windows
    # return pathlib.Path(file_name).as_posix().replace(checklist_path, "") # Linux

# get module name
def module_name(file_name):
    return pathlib.PureWindowsPath(file_name).parts[6] # Windows
    # return pathlib.Path(file_name).parts[3] # Linux

# Get module and scripts's module with json format
def deploy_rollback_backup(checklist_path, is_csv):
    modules = []
    dict = {}
    empty_dict = {"Rollback":"", "Backup":"", "Deploy":""} if is_csv else {"Rollback":[], "Backup":[], "Deploy":[]}
    for sql_script_file in sql_scripts:
        if module_name(sql_script_file) not in modules:
            modules.append(module_name(sql_script_file))
            dict[module_name(sql_script_file)] = copy.deepcopy(empty_dict)
        sub_path = sub_path_file(sql_script_file, checklist_path).upper().split("/")
        if "ROLLBACK" in sub_path:
            dict[module_name(sql_script_file)]["Rollback"]="\n".join(["/".join(sub_path_file(sql_script_file, checklist_path).split("/")[1:]),dict[module_name(sql_script_file)]["Rollback"]]) if is_csv else dict[module_name(sql_script_file)]["Rollback"] + ["/".join(sub_path_file(sql_script_file, checklist_path).split("/")[1:])]
        elif "BACKUP" in sub_path:
            dict[module_name(sql_script_file)]["Backup"]="\n".join(["/".join(sub_path_file(sql_script_file, checklist_path).split("/")[1:]),dict[module_name(sql_script_file)]["Backup"]]) if is_csv else dict[module_name(sql_script_file)]["Backup"] + ["/".join(sub_path_file(sql_script_file, checklist_path).split("/")[1:])]
        else:
            dict[module_name(sql_script_file)]["Deploy"]="\n".join(["/".join(sub_path_file(sql_script_file, checklist_path).split("/")[1:]),dict[module_name(sql_script_file)]["Deploy"]]) if is_csv else dict[module_name(sql_script_file)]["Deploy"] + ["/".join(sub_path_file(sql_script_file, checklist_path).split("/")[1:])]
            
    return dict

# Retrun json format with dictionary
def json_format(dict):
    return json.dumps(dict, indent = 4) 

# Get script name by index
def get_file_by_index(index, dict):
    i = index.split(".")
    r = r"^\d+"
    module_name = ""
    i_module = 0
    for key in dict.keys():
        if i[0] == re.findall(r, key)[0]:
            i_module = list(dict.keys()).index(key)
            module_name = key
    i_rbd = int(i[1])
    i_file = int(i[2])
    return "{}/{}".format(module_name, list(dict[list(dict)[i_module]][list(dict[list(dict)[i_module]])[i_rbd]])[i_file])

# Set index for seraching script
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


# Get sub module, features Script - BPM - ....

def deploy_rollback_backup_ver2(checklist_path, is_csv):
    dict = {}
    modules = []
    empty_dict = {"Rollback":{}, "Backup":{}, "Deploy":{}}

    def sub_module_feature_script(sub_module_path):
        sub_path_elements = sub_module_path.split("/")     

        # Sub module without feature
        def append_to_sm_dict_without_feature(type):
            def append():
                dict[sub_path_elements[0]][type][sub_path_elements[-2]] = "\n".join([dict[sub_path_elements[0]][type][sub_path_elements[-2]], sub_path_elements[-1]]) if is_csv else dict[sub_path_elements[0]][type][sub_path_elements[-2]] + [sub_path_elements[-1]]
            try:
                append()
            except:
                dict[sub_path_elements[0]][type][sub_path_elements[-2]] = "" if is_csv else []
                append()

        # Sub module with feature    
        def append_to_sm_dict_with_feature(type):
            def append():
                dict[sub_path_elements[0]][type][sub_path_elements[-3]][sub_path_elements[-2]] = "\n".join([dict[sub_path_elements[0]][type][sub_path_elements[-3]][sub_path_elements[-2]], sub_path_elements[-1]]) if is_csv else dict[sub_path_elements[0]][type][sub_path_elements[-3]][sub_path_elements[-2]] + [sub_path_elements[-1]]
            def append_feature():
                dict[sub_path_elements[0]][type][sub_path_elements[-3]][sub_path_elements[-2]] = "" if is_csv else []
                append()
            try:
                append()
            except:
                try:
                    append_feature()
                except:
                    dict[sub_path_elements[0]][type][sub_path_elements[-3]] = {}
                    append_feature()

        # Module_Name/Scripts/Deploy/Sub Module/SQL_Scripts
        # Module_Name/Scripts/Deploy/Sub Module/Feature/SQL_Scripts
        # 5. Currently path without Deploy/Script. Use 3. Will be optimized later
        if "ROLLBACK" in sub_module_path.upper():
            append_to_sm_dict_without_feature("Rollback") if len(sub_path_elements) == 3 else append_to_sm_dict_with_feature("Rollback")
        elif "BACKUP" in sub_module_path.upper():
            append_to_sm_dict_without_feature("Backup") if len(sub_path_elements) == 3 else append_to_sm_dict_with_feature("Backup")
        else:
            append_to_sm_dict_without_feature("Deploy") if len(sub_path_elements) == 3 else append_to_sm_dict_with_feature("Deploy")

    # Init empty dict for Module
    for sql_script_file in sql_scripts:
        if module_name(sql_script_file) not in modules:
            modules.append(module_name(sql_script_file))
            dict[module_name(sql_script_file)] = copy.deepcopy(empty_dict)
        sub_module_feature_script(sub_path_file(sql_script_file, checklist_path)) 
           
    return dict

