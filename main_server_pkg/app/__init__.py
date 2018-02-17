from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db_config import db_config

app = Flask(__name__)

#application configuration
app.config["SECRET_KEY"]="123456789"

#creating databse url string to use with sql alchemy
DB_URL = db_config["db_type"]+"://"+ db_config["user"] +":"+ \
            db_config["password"] +"@"+ db_config["location"] +":"+ \
            str(db_config["port"]) +"/"+ db_config["db_name"]
            
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

#creating connection
db_connect = SQLAlchemy(app)

#setting up login manager for flask login
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"  # customize the flash message category

from app import views