from app import app
from flask import render_template, request, redirect, url_for, flash
from forms import LoginForm

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/login', methods=["GET","POST"])
def login():
	loginForm = LoginForm()

	if request.method == 'POST' and loginForm.validate_on_submit():		
		return redirect(url_for('home'))

	return render_template("login.html", loginForm = loginForm)