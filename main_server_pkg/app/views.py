#app, sqlalchemy database object and login manager object imports
from app import app, db, login_manager

#basic flask imports
from flask import render_template, request, redirect, url_for, flash, jsonify

#login manager imports
from flask_login import login_user, logout_user, current_user, login_required

#form imports
from forms import LoginForm, PasswordForm

#model imports for user and network nodes (machines for version control)
from models import User, Node

#password hashing checking functions
from werkzeug.security import check_password_hash, generate_password_hash

#imports for authentication value random generation
from random import randrange
from uuid import uuid1

init_node_auth_code = None #global value to use to initialize a node

#root route for main server view
@app.route('/')
def home():
	print current_user.is_authenticated
	if current_user.is_authenticated:
		return redirect(url_for('dash'))

	return render_template('home.html')


#login route for main server
@app.route('/login', methods=["GET","POST"])
def login():
	
	loginForm = LoginForm() #instanciates wtforms login form
	
	if current_user.is_authenticated: #uses flask login manager to check if user is already logged in
		redirect(url_for('home'))
		
	
	if request.method == 'POST' and loginForm.validate_on_submit():
		
		user = User.query.filter_by(username=loginForm.username.data).first() #using ORM to query mysql database for user
		
		if user is not None and check_password_hash(user.password, loginForm.password.data):
			
			login_user(user)
			
			flash('Logged in successfully.', 'success')
			
			next_page = request.args.get('next') #gets the url of the previous page that requires login
			
			return redirect(next_page or url_for('home')) #directs user to home page or the url retried from the next argument
		else:
			flash('Username or Password is incorrect.', 'danger')
		

	return render_template("login.html", initial = False, loginForm = loginForm)


#main server dashboard route
@app.route('/dashboard')
@login_required
def dash():
	return render_template('dash.html')
	


#api route for main server user to generate a 
@app.route('/add_node')
@login_required
def rando_gen():
	'''Generates a random number between 1000000 and 10000000. Returns the number as json to a loged in requester.'''
	
	global init_node_auth_code
	
	init_node_auth_code = randrange(1000000, 10000000)
	return jsonify(auth_key=init_node_auth_code)


@app.route('/node_init_auth', methods=['POST'])
def init_node_auth():
	'''Route to setup a new node. This route allows a node to associate with the main server and retrieves an api key once the correct
	auth code is provided.
	
	@return Api key on successful association; False if auth_key is incorrect 
	and a blank json object on unathorized attempt to authenticate
	'''
	global init_node_auth_code
	node_name = request.args['machine_name']
	node_auth_code = int(request.args['node_auth_code'])
	node_pass = request.args['new_pass']
	
	
	if init_node_auth_code is None:
		return jsonify()
	
	if init_node_auth_code != node_auth_code:
		init_node_auth_code = None
		return jsonify(result=False)
	
	api_key = key_gen()
	
	node = Node(node_name, node_pass, api_key) # creates new node object for database insertion
	
	try:
		#attempt to add node to database
		db.session.add(node)
		db.session.commit()
		print 'here'
		init_node_auth_code = None
		return jsonify(key=api_key)
	except Exception as e:
		db.session.rollback()
		return jsonify(result=False)
		
		
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def error404(error):
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

### non web based functions
def key_gen():
	'''generates api key'''
	return str(uuid1())