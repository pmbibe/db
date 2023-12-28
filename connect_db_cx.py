import cx_Oracle
import validate
import get_statements

# Need DISABLED AUTOCOMMIT
# Replace these with your own credentials
def connection_string_func(host, port,service_name):
    return "{}:{}/{}".format(host, port, service_name)

def run_sql_script(file_path, is_standalone): 
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
    def ddl_define_modify_script(scripts, connection):
        cursor = connection.cursor()
        for script in scripts:
            try:
                cursor.execute(script)
            except cx_Oracle.DatabaseError as e:
                print("Database Update Failed: {}".format(e))
                print("Script Error: {} in Script file: {}".format(script, file_path))
                failed_script_file.append(file_path)  
                break

    # Excute implicit COMMIT scripts with pool
    def ddl_define_modify_script_pool(scripts):
        pool = connect_with_session_pool()    
        connection = pool.acquire()      
        ddl_define_modify_script(scripts, connection)
        pool.release(connection) 
        pool.close() 

    # Excute implicit COMMIT scripts Standalone
    def ddl_define_modify_script_standalone(scripts):
        connection = connect_with_standalone()   
              
        ddl_define_modify_script(scripts, connection)
        connection.close()

    # Excute other scripts
    def normal_script(scripts, connection):
        # DISABLED AUTOCOMMIT
        connection.autocommit = False         # type: ignore
        cursor = connection.cursor()
        for script in scripts:
            try:
                cursor.execute(script)
                # successed_script_file.append(script)
            except cx_Oracle.DatabaseError as e:
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

    # Excute other scripts with pool connection
    def normal_script_pool(scripts):        
        pool = connect_with_session_pool()    
        connection = pool.acquire()      
        normal_script(scripts, connection)
        pool.release(connection)
        pool.close() 
    
    # Excute other scripts with standalone connection
    def normal_script_standalone(scripts):
        connection = connect_with_standalone()
        normal_script(scripts, connection)
        connection.close()

    # Execute the SQL script
    sql_scripts = [validate.validate_eos(x.replace("\n", "")).group(1) for x in get_statements.get_statements(file_path)]
    pre_run_sql_script(sql_scripts)
    if is_standalone:
        ddl_define_modify_script_standalone(ddl_define_modify_scripts) 
        ddl_define_modify_script_standalone(ddl_define_modify_scripts_vpf)
        normal_script_standalone(normal_scripts)
    else:
        ddl_define_modify_script_pool(ddl_define_modify_scripts) 
        ddl_define_modify_script_pool(ddl_define_modify_scripts_vpf)
        normal_script_pool(normal_scripts)   
    if file_path not in failed_script_file:
        successed_script_file.append(file_path)   
    
def connect_with_session_pool():
    
    # Create the session pool
    pool = cx_Oracle.SessionPool(user=username, 
                                 password=password,
                                 dsn= connection_string, 
                                 min=2, max=5, increment=1, encoding="UTF-8")
    return pool


def connect_with_standalone():

    # Connect to the Oracle database
    connection = cx_Oracle.connect(user=username, 
                                   password=password,
                                   dsn= host)
    return connection

successed_script_file = []
failed_script_file = []
username = "pmbibe"
password = "Babibe2211"
host = "employees"
port = 1521
db = "employees"
connection_string = connection_string_func(host, port, db)
