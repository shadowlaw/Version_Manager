from . import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(225))
    
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' %  self.username
        
        
class Node(db.Model):
    
    __tablename__ = 'nodes'
    
    node_id = db.Column(db.Integer, primary_key=True)
    app_list_id = db.Column(db.Integer)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(225))
    api_key = db.Column(db.String(225))
    node_group = db.Column(db.String(80))
    
    
    def __init__(self, name, password, key):
        self.name = name
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.api_key = key
        
class AppList(db.Model):
    
    __tablename__ = 'application_list'
    
    list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    
    def __init__(self, name):
        self.name = name