from app import app
from flask import render_template, request, redirect, url_for, flash

@app.route('/login')
def login():
    pass