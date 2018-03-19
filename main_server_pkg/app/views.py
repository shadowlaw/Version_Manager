#app, sqlalchemy database object and login manager object imports
from app import app, db, login_manager, cwd, application_list_location

#basic flask imports
from flask import render_template, request, redirect, url_for, flash, jsonify

#login manager imports
from flask_login import login_user, logout_user, current_user, login_required

#form imports
from forms import LoginForm, PasswordForm

#model imports for user and network nodes (machines for version control)
from models import User, Node, AppList

#password hashing checking functions
from werkzeug.security import check_password_hash, generate_password_hash

#secure filename import
from werkzeug.utils import secure_filename

#imports for authentication value random generation
from random import randrange
from uuid import uuid1

init_node_auth_code = None #global value to use to initialize a node

#default python package imports
import json
import os

#user made modules
import fileManager

################# web views #####################
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
		

	return render_template("login.html", loginForm = loginForm)

#main server dashboard route
@app.route('/dashboard')
@login_required
def dash():
	return render_template('dash.html')
	


#api route for main server user to generate a 
@app.route('/add_node', methods=["POST"])
@login_required
def rando_gen():
	'''Generates a random number between 1000000 and 10000000. Returns the number as json to a loged in requester.'''
	
	global init_node_auth_code
	
	init_node_auth_code = randrange(1000000, 10000000)
	return jsonify(auth_key=init_node_auth_code)

@app.route('/node_management', methods=["GET", "POST"])
@login_required
def list_nodes():
	nodes = None
	
	
	if request.method == "POST":
		data = request.json
		group_name = data["name"]
		
		for node in data["nodes"]:
			if node["value"] == "on":
				node = Node.query.filter_by(name = node["name"]).first()
				node.group = group_name
				try:
					db.session.commit()
				except Exception as e:
					pass
		
		return "List Added"
		
	nodes = Node.query.order_by(Node.name).all()
	
	return render_template("manage_nodes.html", nodes = nodes)

@app.route("/app_list_mgmt", methods=["GET", "POST"])
@login_required
def app_list():
	
	if request.args.to_dict() != dict():
		if request.args["atn"] == "crt" and request.method == "POST":
			list_data = request.get_json()["app_data"]
			list_name = secure_filename(request.get_json()["list_name"])
			new_app_list = dict()
			
			new_app_list["apps"] = {}
			
			for items in list_data:
				new_app_list["apps"][items["app_name"]] = items["version"]
			
			try:
				appObj = AppList(list_name)
				
				db.session.add(appObj)
				db.session.commit()
				
				absolute_path = generate_app_list_path(list_name)
				json.dump(new_app_list, open(absolute_path, "w"), indent=2)
				return "List Created"
			except Exception as e:
				db.session.rollback()
				print e.args
				return "List could not be created"
				
		elif request.args["atn"] == "crt":
			return render_template("create_app_list.html")
		
		if request.args["atn"] == "del" and request.method == "POST":
			pass
	
	app_lists = AppList.query.order_by(AppList.list_id).all()
	
	return render_template("display_app_list.html", app_lists = app_lists)

##############################################################

################### Client api routes ########################
@app.route('/node_init_auth', methods=['POST', 'GET'])
def init_node_auth():
	'''Route to setup a new node. This route allows a node to associate with the main server and retrieves an api key once the correct
	auth code is provided.
	
	@return Api key on successful association; False if auth_key is incorrect 
	and a blank json object on unathorized attempt to authenticate
	'''
	
	if request.method == 'GET':
		init_node_auth_code = None
		return jsonify()
	
	global init_node_auth_code
	node_name = request.args['machine_name']
	node_auth_code = int(request.args['node_auth_code'])
	node_pass = request.args['new_pass']
	
	
	if init_node_auth_code is None:
		return jsonify()
	
	if init_node_auth_code != node_auth_code:
		init_node_auth_code = None
		return jsonify(key=False)
	
	api_key = key_gen()
	
	## add check for already existing node
	node = Node.query.filter_by(node_name = node_name).first()
	
	if node != None:
		return jsonify(key=None)
		
	node = Node(node_name, node_pass, api_key) # creates new node object for database insertion
	
	try:
		#attempt to add node to database
		db.session.add(node)
		db.session.commit()
		init_node_auth_code = None
		return jsonify(key=api_key)
	except Exception as e:
		db.session.rollback()
		return jsonify(key="error")
		

	
@app.route('/app_valid', methods = ["GET", "POST"])
def validate_cli_app():
	request_key = request.json[0]['key']
	
	node = Node.query.filter_by(api_key = request_key).first()
	
	if node is None:
		return jsonify()
		
	set_app_list = AppList.query.filter_by(list_id = node.app_list_id).first()
	
	if set_app_list is None:
		return jsonify(response='no list')
	
	rec_app_list = request.json[1]["apps"]
	
	file_path = generate_app_list_path(set_app_list.name)
	curr_app_list = json.loads(fileManager.read_file(file_path))['apps']  #loads list of apps from server FS
	print (curr_app_list)
	curr_names = curr_app_list.keys()
	change = dict()
	to_install = dict()

	for name in curr_names:
		if rec_app_list.has_key(name): #check if the response has app key that we're looking for
			if not rec_app_list[name] == curr_app_list[name]: #if it does then it'll check the version
				change[name] = curr_app_list[name]
		else:
			to_install[name] = curr_app_list[name]
	
	return jsonify(install = to_install, changes=change) # will return new apps and versions to install and corrections to already installed applications
	
	
	
##########################################################################

def generate_app_list_path(list_name):
	return os.path.join(cwd,application_list_location, list_name+".json")

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