import cx_Oracle
import get_statements

# Replace these with your own credentials
username = "your_username"
password = "your_password"
connection_string = "your_connection_string"

# Connect to the Oracle database
connection = cx_Oracle.connect(username, password, connection_string)

# Read the SQL script into a string
def run_sql_script(file_path):
    sql_scripts = get_statements.get_statements(file_path)
    # Execute the SQL script
    cursor = connection.cursor()
    for sql_script in sql_scripts:
        try:
            cursor.execute(sql_script)
            connection.commit()
        except Exception as e:
            print("Database Update Failed: {}".format(e))
            print("Script Error: {} in Script file: {}".format(sql_script, file_path))
            print("Rollback ...")
            connection.rollback()
    cursor.close()    

# Close the connection
connection.close()
