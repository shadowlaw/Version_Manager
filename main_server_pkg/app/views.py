from app import app
from flask import render_template, request, redirect, url_for, flash, session
from forms import LoginForm, PasswordForm
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/login', methods=["GET","POST"])
def login():
	password = file_reader('pass.txt')
	
	print password
		
	if password == "":
		passwordForm = PasswordForm()
		
		if change_password(passwordForm):
			flash('Password created. Please Login', 'success')
			return redirect(url_for('login'))
		else:
			flash("Password does not match", "danger")
			
		
		return render_template('login.html', initial = True, passwordForm = passwordForm)
	
	loginForm = LoginForm()
	
	if request.method == 'POST' and loginForm.validate_on_submit():
		
		if check_password_hash(password, loginForm.password.data):
			
			session['logged_in'] = True
			flash('Logged in successfully.', 'success')
			
			next_page = request.args.get('next')
			
			return redirect(next_page or url_for('home'))
		else:
			flash('Username or Password is incorrect.', 'danger')
		

	return render_template("login.html", initial = False, loginForm = loginForm)


@app.route('/logout')
def logout():
	if session['logged_in']:
		session['logged_in'] = False
	
	return redirect(url_for('home'))
	


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
    
  
def file_reader(filename):
	with open(filename,"r") as fp:
		return fp.read()
		

def file_writer(filename, data):
	with open(filename,"w") as fp:
		fp.write(data)
		
def change_password(passwordForm):
	if passwordForm.validate_on_submit():
		if passwordForm.password.data==passwordForm.confirm.data:
			file_writer('pass.txt', generate_password_hash(passwordForm.password.data))
			return True
		else:
			return False
				
