from os import getenv

db_config = dict()

db_config['driver'] = 'mysql'
#db_config['user'] = getenv('C9_USER')
db_config['user'] = "root"
db_config['password'] = 'crimzon7'
db_config['db_name'] = 'vm_main_server'
db_config['location'] = 'localhost'
db_config['port'] = '3306'