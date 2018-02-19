from flask import Flask

app = Flask(__name__)

#application configuration
app.config["SECRET_KEY"]="123456789"

app.config.from_object(__name__)

from app import views