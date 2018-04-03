from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_config import db_config
import os

app = Flask(__name__)

#application configuration
app.config["SECRET_KEY"]="123456789"

#setting up db config
DB_URI = db_config['driver'] +'://'+ db_config['user'] +':'+ \
db_config['password']+'@'+db_config['location']+':'+db_config['port']+'/'+ \
db_config['db_name']

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning

#creating connection
db = SQLAlchemy(app)

cwd = os.path.join(os.getcwd(),"app")
application_list_location = "node_app_list"

app.config.from_object(__name__)

from app import views