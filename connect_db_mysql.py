import validate
import mysql.connector
import get_statements

successed_script_file = []
failed_script_file = []
err = 0
username = "pmbibe"
password = 'Abc@12314455'
host = "127.0.0.1"
port = 3306
db = "employees"

def run_sql_script(file_path): 
    ddl_define_modify_scripts = []
    ddl_define_modify_scripts_vpf = []
    normal_scripts = []   
    
    

    # Group DDL statements implicit COMMIT: DDL statements implicit COMMIT include/exclude VIEW, PROCEDURE, FUNCTION, ... 
    def pre_run_sql_script(scripts):
        for script in scripts:
            if validate.validate_ddl_inc_vpf(script):
                ddl_define_modify_scripts_vpf.append(script) 
            elif validate.validate_ddl_exc_vpf(script):
                ddl_define_modify_scripts.append(script) 
            else:
                normal_scripts.append(script)

    # Excute implicit COMMIT scripts
    def ddl_define_modify_script(scripts):
        connection = connect_with_standalone()
        cursor = connection.cursor()
        for script in scripts:
            try:
                cursor.execute(script)
            except mysql.connector.Error as e:
                print("Database Update Failed: {}".format(e))
                failed_script_file.append(file_path)
                break
        connection.close()
        

    # Excute other scripts
    def normal_script(scripts):
        connection = connect_with_standalone()

        # DISABLED AUTOCOMMIT
        connection.autocommit = False         # type: ignore
        cursor = connection.cursor()
        for script in scripts:
            try:
                cursor.execute(script)
            except mysql.connector.Error as e:
                print("Database Update Failed: {}".format(e))
                print("Script Error: {} in Script file: {}".format(script, file_path))
                print("Rollback ...")
                connection.rollback()
                if file_path not in failed_script_file: failed_script_file.append(file_path)
                if file_path in successed_script_file: successed_script_file.remove(file_path)
                break

        connection.commit()
        # ENABLED AUTOCOMMIT
        connection.autocommit = True # type: ignore
        connection.close()
        

    # Execute the SQL script
    sql_scripts = get_statements.get_statements(file_path)
    pre_run_sql_script(sql_scripts)    
    ddl_define_modify_script(ddl_define_modify_scripts)
    ddl_define_modify_script(ddl_define_modify_scripts_vpf)
    normal_script(normal_scripts)
    if file_path not in failed_script_file:
        successed_script_file.append(file_path)

    
def connect_with_standalone():
    # Connect to the MySQL database
    connection = mysql.connector.connect(user=username, 
                                   password=password,
                                   host=host, port = port, database = db)
    return connection
