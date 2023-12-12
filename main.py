# import report
import get_statements
import sys
import get_checklist
import argparse
from datetime import datetime
import validate
# import connect_db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Checklist report for Golive - Test")
    subparsers = parser.add_subparsers(title='Subcommand', description='Get script details, dry run, v.v....')
    parser_list=subparsers.add_parser('list', description="List of script and Module", help="List of script and Module")
    parser_list.add_argument('-ii','--include-index', help="List of script and Module with Index. Set y|n", default= "y")
    parser_list.add_argument('-o','--out-put', help="List of script and Module with Index. Example: xlsx, json, ... Defautl: json", default= "json")
    parser_detail=subparsers.add_parser('detail', description="Details of script, searching by Index", help="Details of script, searching by Index")
    parser_detail.add_argument('-i','--index', help='Index of script file, default: 0.0.0', default= "0.0.0")
    parser_detail.add_argument('-a','--all', help='Read all script in file, default: y. Set y|n', default= "n")
    parser.add_argument('-rpath', '--path', help='Root path, default: /tmp', default="/tmp")
    parser.add_argument('-prj','--project', help='Project name, default: pmbibe_project', default = "pmbibe_project")
    parser.add_argument('-chl','--checklist', help="Golive date, default: Current date follwing format YYYY.MM.DD or YYYYMMDD", default=datetime.today().strftime('%Y.%m.%d'))
    
    args = parser.parse_args()
    checklist_path = ""

    is_match_1 = validate.validate_date_1("Checklist {}".format(args.checklist))
    if validate.validate_date(args.checklist) or is_match_1 :
        if validate.validate_date(args.checklist): checklist_path = "{}/Checklists/{}/Checklist-{}/{}/{}/".format(args.path, 
                                                                                                                  args.project, 
                                                                                                                  args.checklist.split(".")[0], 
                                                                                                                  ".".join(args.checklist.split(".")[0:2]), 
                                                                                                                  ".".join(args.checklist.split("."))
                                                                                                                  )
   
        if is_match_1: checklist_path = "{}/Checklists/{}/Checklist-{}/{}/Checklist {}/".format(args.path, 
                                                                                                args.project, 
                                                                                                is_match_1.group(2), 
                                                                                                ".".join([is_match_1.group(2), is_match_1.group(4)]),
                                                                                                is_match_1.group(1)
                                                                                                )
        get_checklist.find_SQL(checklist_path)
        dict_drb = get_checklist.deploy_rollback_backup_ver2(checklist_path)
        dict_drb_csv = get_checklist.deploy_rollback_backup_csv(checklist_path)

        if "list" in sys.argv and validate.validate_include_index(args.include_index.upper()):
            if args.out_put == "xlsx":
                get_checklist.dict_to_csv(dict_drb_csv, args.checklist)
            else:
                    if args.include_index.upper() == "Y":
                        dict_drb_index = get_checklist.deploy_rollback_backup_index(checklist_path)
                        index_dict = get_checklist.set_file_index(dict_drb_index)
                        print(get_checklist.json_format(index_dict))
                    elif args.include_index.upper() == "N":
                        print(get_checklist.json_format(dict_drb))
        elif "detail" in sys.argv and validate.validate_index(args.index):
            file_name = get_checklist.get_file_by_index(args.index, dict_drb)
            if args.all.upper() == "Y":
                get_checklist.read_checklist_script(checklist_path + file_name)
                data = get_checklist.read_checklist_script(checklist_path + file_name)
                print(data)
            else:
                statements = get_statements.get_statements(checklist_path + file_name)
                for statement in statements:
                    print(statement.strip())
                    print("---------------------------------")
    else:
        print("Check you input format. For more information, use -h or --help")
