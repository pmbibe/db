import cx_Oracle
import get_statements

# Need DISABLED AUTOCOMMIT
# Replace these with your own credentials
def connection_string_func(host, port,service_name):
    return "{}:{}/{}".format(host, port, service_name)

# Read the SQL script into a string
def run_sql_script(file_path, connection):    

    # DISABLED AUTOCOMMIT
    connection.autocommit = False

    sql_scripts = get_statements.get_statements(file_path)

    # Execute the SQL script
    with connection.cursor() as cursor:
        for sql_script in sql_scripts:
            try:
                cursor.execute(sql_script)            
            except Exception as e:
                print("Database Update Failed: {}".format(e))
                print("Script Error: {} in Script file: {}".format(sql_script, file_path))
                print("Rollback ...")
                connection.rollback()
                return False
    connection.commit()

    # ENABLED AUTOCOMMIT
    connection.autocommit = True
    return True

def connect_with_session_pool(file_path):
    
    # Create the session pool
    pool = cx_Oracle.SessionPool(user=username, 
                                 password=password,
                                 dsn= connection_string, 
                                 min=2, max=5, increment=1, encoding="UTF-8")
    # Acquire a connection from the pool
    connection = pool.acquire() 
    
    successed_script_file.append(file_path) if run_sql_script(file_path, connection) else failed_script_file.append(file_path)

    # Release the connection to the pool
    pool.release(connection) 

    # Close the pool
    pool.close() 

def connect_with_standalone(file_path):

    # Connect to the Oracle database
    connection = cx_Oracle.connect(user=username, 
                                   password=password,
                                   dsn= connection_string)
    successed_script_file.append(file_path) if run_sql_script(file_path, connection) else failed_script_file.append(file_path)
    connection.close()

successed_script_file = []
failed_script_file = []
username = "your_username"
password = "your_password"
host = "dbhost.example.com"
port = 1521
db = "orclpdb1"
connection_string = connection_string_func(host, port, db)
