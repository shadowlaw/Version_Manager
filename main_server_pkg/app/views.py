from app import app
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
def home():
    return render_template('home.html')
    

@app.route('/login')
def login():
    pass