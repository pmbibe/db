# import report
import sys
import get_checklist
import argparse
from datetime import datetime
import validate
# import connect_db
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Checklist report for Golive - Test")
    subparsers = parser.add_subparsers(title='Subcommand', description='Get script details, dry run, v.v....')
    parser_list=subparsers.add_parser('list', description="List of script and Module", help="List of script and Module")
    parser_list.add_argument('-ii','--include-index', help="List of script and Module with Index. Set Yes|No", default= "Yes")
    parser_detail=subparsers.add_parser('detail', description="Details of script, searching by Index", help="Details of script, searching by Index")
    parser_detail.add_argument('-i','--index', help='Index of script file, default: 0.0.0', default= "0.0.0")
    parser.add_argument('-rpath', '--path', help='Root path, default: /tmp', default="/tmp")
    parser.add_argument('-prj','--project', help='Project name, default: pmbibe', default = "pmbibe")
    parser.add_argument('-chl','--checklist', help="Golive date, default: Current date follwing format YYYY.MM.DD", default=datetime.today().strftime('%Y.%m.%d'))
    

    args = parser.parse_args()
    
    if validate.validate_date(args.checklist):
        checklist_path = "{}/Checklists/{}/Checklist-{}/{}/{}/".format(args.path, args.project, args.checklist.split(".")[0], ".".join(args.checklist.split(".")[0:2]), ".".join(args.checklist.split(".")))
        get_checklist.find_SQL(checklist_path)
        dict_drb = get_checklist.deploy_rollback_backup(checklist_path)
        dict_drb_csv = get_checklist.deploy_rollback_backup_csv(checklist_path)
        if "list" in sys.argv and validate.validate_include_index(args.include_index.upper()):
            if args.include_index.upper() == "YES":
                index_dict = get_checklist.set_file_index(dict_drb)
                print(get_checklist.json_format(index_dict))
            else:
                print(get_checklist.json_format(dict_drb))
        get_checklist.dict_to_csv(dict_drb_csv)
        # file_name = get_checklist.get_file_by_index(args.index, dict_drb)
        # data = get_checklist.get_statement(checklist_path + file_name)
        # for d in data:
        #     print(d.strip())
    else:
        print("Check you input format. For more information, use -h or --help")
    
    
    # index = get_checklist.set_file_index(dict_drb)
    # # print(get_checklist.json_format(index))
    # file_name = get_checklist.get_file_by_index("1.2.0", dict_drb)
    # data = get_checklist.get_statement(full_path + file_name)
    # for d in data:
    #     print(d.strip())
    # # print(file_name)
