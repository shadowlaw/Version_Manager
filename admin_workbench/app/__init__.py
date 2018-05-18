from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db_config import db_config
from utils.fileDistrib import *
from utils.fileManager import read

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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # necessary to tell Flask-Login what the default route is for the login page
login_manager.login_message_category = "info"  # customize the flash message category

APP_LIST_LOCATION = "./app/node_app_list"
APP_LIST_ZIP_NAME = "app_list.zip"
APP_LIST_ZIP = APP_LIST_LOCATION+"/"+APP_LIST_ZIP_NAME

SERVER_LIST = "./app/static/server_list.txt"

SERVER_LIST_ARRAY = read(SERVER_LIST).split(",")

file_sender = FileDistrib(SERVER_LIST_ARRAY, fileName = APP_LIST_ZIP)

app.config.from_object(__name__)

from app import views