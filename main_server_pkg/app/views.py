from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, PasswordForm
from models import User
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/login', methods=["GET","POST"])
def login():
	loginForm = LoginForm()
	
	if current_user.is_authenticated:
		redirect(url_for('home'))
		
	
	if request.method == 'POST' and loginForm.validate_on_submit():
		
		user = User.query.filter_by(username=loginForm.username.data).first()
		
		print loginForm.password.data
		print user.password
		
		if user is not None and check_password_hash(user.password, loginForm.password.data):
			
			login_user(user)
			
			flash('Logged in successfully.', 'success')
			
			next_page = request.args.get('next')
			
			return redirect(next_page or url_for('home'))
		else:
			flash('Username or Password is incorrect.', 'danger')
		

	return render_template("login.html", initial = False, loginForm = loginForm)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def error404():
	return render_template('404.html'), 404
	

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

