# Using Docker - Tested for MySQL - Testing for Oracle

Download Oraclient ***DPI-1047***: https://download.oracle.com/otn_software/linux/instantclient/2112000/instantclient-basic-linux.x64-21.12.0.0.0dbru.zip

Oracle Docker image: https://hub.docker.com/r/gvenzl/oracle-xe

- Mount Checklist Folder to /app. Example: ```/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22```
- Mount Report Folder to /report
- Edit variable in ```connect_db_cx.py``` for Oracle or ```connect_db_mysql.py``` for MySQL
- Edit and Replace ```import report``` and ```report.create_report(get_checklist.sql_scripts, args.module_name, args.sub_module_name, args.feature_name, is_standalone)``` for Oracle
- Edit and Replace ```import report_mysql``` and ```report_mysql.create_report(get_checklist.sql_scripts, args.module_name, args.sub_module_name, args.feature_name)``` and ```line 64: report_mysql.dict_to_csv(dict_drb_csv, args.checklist, False)``` for MySQL
```
python main.py --help
usage: main.py [-h] [-rpath PATH] [-prj PROJECT] [-chl CHECKLIST] {list,detail,exec,report} ...

Checklist report for Golive - Test

options:
  -h, --help            show this help message and exit
  -rpath PATH, --path PATH
                        Root path, default: /app
  -prj PROJECT, --project PROJECT
                        Project name, default: project_name
  -chl CHECKLIST, --checklist CHECKLIST
                        Golive date, default: Current date follwing format YYYY.MM.DD or YYYYMMDD

Subcommand:
  Get script details, dry run, v.v....

  {list,detail,exec,report}
    list                List of script and Module
    detail              Details of script, searching by Index
    exec                Execute script and create report
    report              ...
```

## ***list***
- Group script by Module and export to xlsx file with ***-o/--out-put*** option: ``` docker run -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.08 --project=project_name --path=/app list -o xlsx ```
- Group script by Module, Sub-module, Feature and export to json format: ``` docker run -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.08 --project=project_name --path=/app list ```
- Group script by Module and export to json format include index with ***-ii/-include-index*** option : ``` docker run -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.08 --project=project_name --path=/app list -ii y ```
## ***detail***
- Read file script files by index : Must have ***-i/--index*** option
  - List all DDL/DML statement which will modify data in database: ``` docker run --rm  -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.08 --project=project_name --path=/app detail -i 03.2.0 ```
  - List all content with ***-a/--all*** optione: ``` docker run --rm  -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.08 --project=project_name --path=/app detail -i 03.2.0 -a y ```
## ***exec***
- ``` docker run --rm  -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.22 --project=project_name --path=/app exec --module-name="01. MySQL" ```

Output:
```
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/03. Module B/05. Scripts/01. Sub-Module BA/01. Feature BAA/01. Insert Data.sql-----------
Database Update Failed: 1050 (42S01): Table 'test_employees' already exists
Database Update Failed: 1136 (21S01): Column count doesn't match value count at row 1
Script Error: INSERT INTO employees.test_employees (FirstName, LastName, Email, Phone, HireDate, Salary)
VALUES ('John', 'Doe', 'helloworld0@email.com', '123-456-7890', 2000); in Script file: /app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/03. Module B/05. Scripts/01. Sub-Module BA/01. Feature BAA/01. Insert Data.sql
Rollback ...
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/03. Module B/05. Scripts/01. Sub-Module BA/02. Feature BAB/01. Insert Data.sql-----------
Database Update Failed: 1050 (42S01): Table 'test_customers' already exists
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/03. Module B/05. Scripts/02. Sub-Module BB/01. Update Data.sql-----------
Database Update Failed: 1054 (42S22): Unknown column '5ABC' in 'field list'
Script Error: UPDATE employees.salaries SET salary=5ABC WHERE emp_no=10005 AND from_date="1989-09-12" AND to_date="1990-09-12"; in Script file: /app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/03. Module B/05. Scripts/02. Sub-Module BB/01. Update Data.sql
Rollback ...
Saved to XLSX File

```
- ``` docker run --rm  -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.22 --project=project_name --path=/app exec --module-name="02. Module A" ```

Output:
```
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/02. Module A/05. Scripts/01. Sub-Module AA/01. Insert Data.sql-----------
Database Update Failed: 1062 (23000): Duplicate entry 'Marketing' for key 'dept_name'
Script Error: INSERT INTO `departments` VALUES
('AA1','Marketing'),
('AA2','Finance'),
('AA3','Human Resources'),
('AA4','Production'),
('AA5','Development'),
('AA6','Quality Management'),
('AA7','Sales'),
('AA8','Research'),
('AA9','Customer Service'); in Script file: /app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/02. Module A/05. Scripts/01. Sub-Module AA/01. Insert Data.sql
Rollback ...
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/02. Module A/05. Scripts/02. Sub-Module AB/01. Update Data.sql-----------
Database Update Failed: 1054 (42S22): Unknown column '5ABC' in 'field list'
Script Error: UPDATE employees.salaries SET salary=5ABC WHERE emp_no=10005 AND from_date="1989-09-12" AND to_date="1990-09-12"; in Script file: /app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/02. Module A/05. Scripts/02. Sub-Module AB/01. Update Data.sql
Rollback ...
Saved to XLSX File

```
- ``` docker run --rm  -v D:\DS_IT_2537\app:/app -v D:\DS_IT_2537\report:/report -it tool --checklist=2023.12.22 --project=project_name --path=/app exec --module-name="03. Module B" ```

Output:
```
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/01. MySQL/05. Scripts/01. Create dept_emp_latest_date view.sql-----------
----------/app/Checklists/project_name/Checklist-2023/2023.12/2023.12.22/01. MySQL/05. Scripts/02. Create current_dept_emp view.sql-----------
Saved to XLSX File
```
