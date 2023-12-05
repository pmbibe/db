import report
import get_checklist
import connect_db
import json

root_path = ""
project_path = ""
sub_path = ""
folder_name = ""
full_path = root_path + project_path + sub_path + folder_name

if __name__ == "__main__":
    get_checklist.find_SQL(full_path)
    dict_drb = get_checklist.deploy_rollback_backup(full_path)
    # print(get_checklist.json_format(dict_drb))
    index = get_checklist.set_file_index(dict_drb)
    # print(get_checklist.json_format(index))
    file_name = get_checklist.get_file_by_index("1.2.0", dict_drb)
    data = get_checklist.get_statement(full_path + file_name)
    for d in data:
        print(d.strip())
    # print(file_name)
