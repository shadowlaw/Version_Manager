from os import getenv

db_config=dict()
db_config["db_type"] = "mysql"
db_config["user"] = getenv("C9_USER")
db_config["password"] = ""
db_config["db_name"] = "vm_db"
db_config["location"] = getenv("IP")
db_config["port"] = 3306