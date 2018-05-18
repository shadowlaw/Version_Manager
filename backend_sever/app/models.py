from . import db

class Node(db.Model):
    
    __tablename__ = 'nodes'
    
    node_id = db.Column(db.Integer, primary_key=True)
    app_list_id = db.Column(db.Integer)
    name = db.Column(db.String(255), unique=True)
    api_key = db.Column(db.String(225))
    node_group = db.Column(db.String(80))
    
    
    def __init__(self, name, key):
        self.name = name
        self.api_key = key
    

class AppList(db.Model):
    
    __tablename__ = 'application_list'
    
    list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    
    def __init__(self, name):
        self.name = name