from subprocess import Popen, PIPE
import subprocess

def connection_string(username, password, host, port,service_name):
    return "{}/{}@//{}:{}/{}".format(username, password, host, port, service_name)
def open_connection(username, password, host, port,service_name, script_path):
    connection = connection_string(username, password, host, port, service_name)
    # script_path = @script_file.sql
    session = Popen(['sqlplus', connection, script_path], stdout=PIPE, stderr=PIPE)
    if session.returncode > 0:
        print(script_path)
