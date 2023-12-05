from subprocess import Popen, PIPE

# def connection_string(username, password, host, port,service_name):
#     return "{}/{}@//{}:{}/{}".format(username, password, host, port, service_name)

# def open_connection(username, password, host, port,service_name, script_path):
#     connection = connection_string(username, password, host, port,service_name)
#     # session = Popen(['sqlplus', connection, script_path], stdout=PIPE, stderr=PIPE)
#     session = Popen(['docker exec -it some-mysql mysql -uroot -p123456', connection, script_path], stdout=PIPE, stderr=PIPE)
#     if session.returncode > 0:
#         print(script_path)

def write_file(script_path):
    with open(script_path) as f:
        return f.read()

def open_connection(script_path, database_name):
    # session = Popen(['sqlplus', connection, script_path], stdout=PIPE, stderr=PIPE, shell=True))
    command = """docker exec -it some-mysql /bin/bash -c 'mysql --user=root --password=123456 {} < {}'""".format(database_name, script_path)
    session = Popen("mysql --user=root --password=123456 {} < {}".format(database_name, script_path), stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = session.communicate()
    if stderr:
        print("Error: {}".format(stderr.decode().strip()))
    elif stdout:
        print("Output: {}".format(stdout.decode().strip()))
    return session.returncode

def copy_file_to_container(script_path):
    session = Popen('docker cp {} some-mysql:{}'.format(script_path, script_path), stdout=PIPE, stderr=PIPE, shell=True)
    session.communicate()
    return session.returncode

script_path = './employees.sql'
database_name = "employees"
# copy_file_to_container(script_path)
open_connection(script_path, database_name)
