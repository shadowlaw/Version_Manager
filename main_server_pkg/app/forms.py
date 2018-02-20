from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Passowrd: ", validators=[DataRequired()])
    
class PasswordForm(FlaskForm):
    password = PasswordField("Password: ", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password: ", validators=[DataRequired()])